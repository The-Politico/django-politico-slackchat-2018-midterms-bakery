from django.core.management.base import BaseCommand
from slackchatbakery.tasks.publish import publish_state
from slackchatbakery.views import Channel
from slackchatbakery.utils.stater import fips_by_slugs, slug_to_fips


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("channel", type=str)

    def handle(self, *args, **options):
        kwargs = {"channel_id": options["channel"]}
        view = Channel(**kwargs)
        channel_data = view.get_serialized_data(**kwargs)

        for state in [
            slug
            for slug in fips_by_slugs
            if slug_to_fips(slug) != '11' and int(slug_to_fips(slug)) <= 56
        ]:
            publish_state(channel_data, state)
