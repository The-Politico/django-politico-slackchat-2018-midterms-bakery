from ..base import BaseView


class BaseReaction(BaseView):
    name = None
    reaction = None
    path = "stubs"

    def get_publish_path(self):
        return self.path

    def get_serialized_data(self, **kwargs):
        return self.get_messages()

    def filter_messages(self, messages):
        return messages

    def message_has_reactions(self, message):
        for reaction in message.get("reactions", []):
            if reaction.get("reaction", "") == self.reaction:
                return True

        return False

    def get_messages(self):
        messages = self.channel["messages"]
        filtered = self.filter_messages(messages)

        return [
            message
            for message in filtered
            if self.message_has_reactions(message)
        ]
