from django.core.management.base import BaseCommand
from slackchatbakery.tasks.render import render_chat


class Command(BaseCommand):
    def handle(self, *args, **options):
        render_chat()
