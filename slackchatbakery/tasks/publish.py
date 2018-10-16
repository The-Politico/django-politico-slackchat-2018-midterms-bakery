import gc
import logging

from celery import Task, shared_task
from slackchatbakery.views import Channel, State, Body, arguments

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
def publish_slackchat(channel_id):
    kwargs = {"channel_id": channel_id}
    view = Channel(**kwargs)
    channel_data = view.publish_serialized_data(**kwargs)

    for argument in arguments.keys():
        publish_argument(channel_data, argument)

    # Garbage collect after run.
    gc.collect()


@shared_task(acks_late=True, base=LoggedTask)
def publish_state(channel, state):
    kwargs = {"channel": channel, "state": state}

    all_view = State(**kwargs)
    all_view.publish_serialized_data(**kwargs)

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
