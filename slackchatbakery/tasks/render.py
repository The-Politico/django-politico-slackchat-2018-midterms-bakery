import gc
import logging
import requests

from celery import shared_task
from slackchatbakery.conf import settings

logger = logging.getLogger(__name__)


@shared_task(acks_late=True)
def render_chat():
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
