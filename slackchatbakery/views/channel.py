import os
import requests
from .base import BaseView
from slackchatbakery.conf import settings
from slackchatbakery.exceptions import ChannelNotFoundError


class Channel(BaseView):
    name = "slackchatbakery-channel"
    path = ""

    def get_publish_path(self):
        return ""

    def get_serialized_data(self, **kwargs):
        self.channel_id = kwargs.get("channel_id")
        self.channel_uri = os.path.join(
            settings.SLACKCHAT_CHANNEL_ENDPOINT, self.channel_id
        )
        return self.get_channel()

    def get_channel(self):
        response = requests.get(self.channel_uri)

        if response.status_code != 200:
            raise ChannelNotFoundError(
                "Could not find channel at: {}".format(self.channel_uri)
            )
        return response.json()
