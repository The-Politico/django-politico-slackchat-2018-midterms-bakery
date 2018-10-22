from django.core.management.base import BaseCommand
from slackchatbakery.tasks.publish import publish_all_states


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("channel", type=str)

    def handle(self, *args, **options):
        publish_all_states(options["channel"])
