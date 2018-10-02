from django.apps import AppConfig


class SlackchatbakeryConfig(AppConfig):
    name = 'slackchatbakery'

    def ready(self):
        from slackchatbakery import signals  # noqa
