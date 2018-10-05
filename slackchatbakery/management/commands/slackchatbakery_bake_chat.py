from django.core.management.base import BaseCommand
from slackchatbakery.tasks.publish import publish_slackchat


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("channel", type=str)

        parser.add_argument(
            "--stubs",
            action="store_true",
            dest="stubs",
            help="Delete poll instead of closing it",
        )

    def handle(self, *args, **options):
        publish_slackchat(options["channel"], publish_stubs=options["stubs"])
