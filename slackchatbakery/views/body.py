from .base import BaseView
from slackchatbakery.utils.races import (
    filter_and_group_by_race,
    message_has_races,
)


class Body(BaseView):
    name = "slackchatbakery-body-all"
    path = "stubs/(?P<body>)/"

    def get_publish_path(self):
        return "stubs/{}".format(self.body)

    def get_serialized_data(self, **kwargs):
        self.channel = kwargs.get("channel")
        self.body = kwargs.get("body").lower()
        return {
            "users": self.get_users(),
            "messages": self.get_races()
        }

    def get_races(self):
        messages = self.channel["messages"]
        filtered = [
            message for message in messages if message_has_races(message)
        ]
        return filter_and_group_by_race(filtered, body=self.body)
