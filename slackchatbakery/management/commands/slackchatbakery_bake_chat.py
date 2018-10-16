from django.core.management.base import BaseCommand
from django.core.management import call_command
from slackchatbakery.tasks.publish import publish_slackchat


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("channel", type=str)

        parser.add_argument(
            "--states",
            action="store_true",
            dest="states",
            help="Also publish state pages.",
        )

        parser.add_argument(
            "--arg",
            action="store_true",
            dest="arg",
            help="Also publish args pages.",
        )

    def handle(self, *args, **options):
        publish_slackchat(options["channel"], publish_args=options["arg"])

        if(options["states"]):
            call_command("slackchatbakery_bake_all_states", options["channel"])
