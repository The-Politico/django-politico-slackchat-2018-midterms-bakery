import gc
import logging
import time
import random

from celery import Task, shared_task
from slackchatbakery.views import Channel, State, Body, arguments
from slackchatbakery.utils.stater import fips_by_slugs, slug_to_fips

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
def publish_slackchat(channel_id, publish_args=False):
    hash = "%032x" % random.getrandbits(128)[0:5]
    logger.info("Starting task: {0}-{1}".format("publish_slackchat", hash))
    start_time = time.time()

    kwargs = {"channel_id": channel_id}
    view = Channel(**kwargs)
    channel_data = view.publish_serialized_data(**kwargs)

    if publish_args:
        for argument in arguments.keys():
            publish_argument(channel_data, argument)

    # Garbage collect after run.
    gc.collect()

    logger.info(
        "--- {0} - Task completed in {1} seconds ---".format(
            hash, time.time() - start_time
        )
    )


@shared_task(acks_late=True, base=LoggedTask)
def publish_all_states(channel):
    hash = "%032x" % random.getrandbits(128)[0:5]
    logger.info("Starting task: {0}-{1}".format("publish_all_states", hash))
    start_time = time.time()

    kwargs = {"channel_id": channel}
    view = Channel(**kwargs)
    channel_data = view.get_serialized_data(**kwargs)

    for state in [
        slug
        for slug in fips_by_slugs
        if slug_to_fips(slug) != "11" and int(slug_to_fips(slug)) <= 56
    ]:
        publish_state(channel_data, state)

    # Garbage collect after run.
    gc.collect()

    logger.info(
        "--- {0} - Task completed in {1} seconds ---".format(
            hash, time.time() - start_time
        )
    )


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
