from django.core.management.base import BaseCommand
from slackchatbakery.tasks.publish import publish_reaction
from slackchatbakery.views import Channel


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("channel", type=str)
        parser.add_argument("reaction", type=str)

    def handle(self, *args, **options):
        kwargs = {"channel_id": options["channel"]}
        view = Channel(**kwargs)
        channel_data = view.get_serialized_data(**kwargs)

        publish_reaction(channel_data, options["reaction"])
