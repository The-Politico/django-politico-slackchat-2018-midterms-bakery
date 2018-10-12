from ..base import BaseView


class BaseArgument(BaseView):
    """
    Base class to extend in order to create unique lists based on arguments.
    Make sure to setup your arguments in the serializer:
    https://django-slackchat-serializer.readthedocs.io/en/latest/models.html#argument
    """
    name = None
    arg = None
    path = "stubs"

    def get_publish_path(self):
        return self.path

    def get_serialized_data(self, **kwargs):
        return {
            "users": self.get_users(),
            "messages": self.get_messages()
        }

    def filter_messages(self, messages):
        return messages

    def message_has_arg(self, message):
        return self.arg in message.get("args", [])

    def get_messages(self):
        messages = self.channel["messages"]
        filtered = self.filter_messages(messages)

        return [
            message
            for message in filtered
            if self.message_has_arg(message)
        ]
