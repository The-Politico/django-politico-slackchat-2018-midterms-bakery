from .base import BaseView
from slackchatbakery.utils.races import (
    filter_body_and_group_by_race,
    message_in_state,
)


class State(BaseView):
    name = "slackchatbakery-state-all"
    path = "stubs/(?P<state>)/"

    def get_publish_path(self):
        return "stubs/{}".format(self.state)

    def get_serialized_data(self, **kwargs):
        self.channel = kwargs.get("channel")
        self.state = kwargs.get("state").lower()
        return self.get_races()

    def get_races(self):
        messages = self.channel["messages"]
        filtered = [
            message
            for message in messages
            if message_in_state(message, self.state)
        ]

        return {
            "house": filter_body_and_group_by_race(filtered, "house"),
            "senate": filter_body_and_group_by_race(filtered, "senate"),
            "governor": filter_body_and_group_by_race(filtered, "governor"),
        }


class StateBody(State):
    name = "slackchatbakery-state-body"
    path = "stubs/(?P<state>)/(?P<body>)/"

    def get_publish_path(self):
        return "stubs/{}/{}".format(self.state, self.body)

    def get_serialized_data(self, **kwargs):
        self.body = kwargs.get("body").lower()
        return super().get_serialized_data(**kwargs)

    def get_races(self):
        races = super().get_races()
        return races[self.body]
