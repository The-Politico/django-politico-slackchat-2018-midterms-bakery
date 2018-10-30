import gc
import logging
import requests
import time
import random

from celery import shared_task
from slackchatbakery.conf import settings

logger = logging.getLogger(__name__)


@shared_task(acks_late=True)
def render_chat():
    hash = ("%032x" % random.getrandbits(128))[0:5]
    logger.info("Starting task: {0}-{1}".format("render_chat", hash))
    start_time = time.time()

    response = requests.get(settings.RENDERER_URL)
    logger.info("Rendering slackchat...")
    if response.status_code < 400:
        logger.info("Slackchat Renderer Response: {}".format(response.text))
    else:
        logger.error(
            "ERROR! Slackchat Renderer Response: {}".format(response.text)
        )

    # Garbage collect after run.
    gc.collect()

    logger.info(
        "--- {0} - Task completed in {1} seconds ---".format(
            hash, time.time() - start_time
        )
    )
