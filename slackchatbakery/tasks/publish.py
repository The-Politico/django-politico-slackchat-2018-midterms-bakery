import gc
import logging

from celery import Task, shared_task
from slackchatbakery.views import Channel, State, StateBody, Body, arguments
from slackchatbakery.utils.races import (
    get_states_in_channel,
    get_bodies_in_channel,
)

logger = logging.getLogger(__name__)

BODIES = ["senate", "house", "governor"]


class LoggedTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        logger.info("Published slackchat {}".format(task_id))

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.error(
            "Slackchat {0} failed to publish: \n{1}".format(task_id, exc)
        )


@shared_task(acks_late=True, base=LoggedTask)
def publish_slackchat(channel_id, publish_stubs=False):
    kwargs = {"channel_id": channel_id}
    view = Channel(**kwargs)
    channel_data = view.publish_serialized_data(**kwargs)

    if publish_stubs:
        states = get_states_in_channel(channel_data["messages"])
        for state in states:
            publish_state(channel_data, state)

        bodies = get_bodies_in_channel(channel_data["messages"])
        for body in bodies:
            publish_body(channel_data, body)

        for argument in arguments.keys():
            publish_argument(channel_data, argument)

    # Garbage collect after run.
    gc.collect()


@shared_task(acks_late=True, base=LoggedTask)
def publish_state(channel, state):
    kwargs = {"channel": channel, "state": state}

    all_view = State(**kwargs)
    all_view.publish_serialized_data(**kwargs)

    for body in BODIES:
        body_kwargs = {**kwargs, **{"body": body}}
        body_view = StateBody(**body_kwargs)
        body_view.publish_serialized_data(**body_kwargs)

    # Garbage collect after run.
    gc.collect()


@shared_task(acks_late=True, base=LoggedTask)
def publish_body(channel, body):
    kwargs = {"channel": channel, "body": body}

    view = Body(**kwargs)
    view.publish_serialized_data(**kwargs)

    # Garbage collect after run.
    gc.collect()


@shared_task(acks_late=True, base=LoggedTask)
def publish_argument(channel, argument):
    kwargs = {"channel": channel}

    if argument in arguments:
        view = arguments[argument](**kwargs)
        view.publish_serialized_data(**kwargs)

    # Garbage collect after run.
    gc.collect()
