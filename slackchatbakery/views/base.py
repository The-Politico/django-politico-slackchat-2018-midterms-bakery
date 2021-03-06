"""
Base context for all web pages, e.g., data needed to render navigation.
"""
from datetime import datetime
from django.views.generic import DetailView
from slackchatbakery.conf import settings
from .mixins.statics.publishing import StaticsPublishingMixin


class BaseView(DetailView, StaticsPublishingMixin):
    name = None
    path = ""

    static_path = settings.S3_STATIC_ROOT

    def get_publish_path(self):
        """OVERWRITE this method to return publish path for a view."""
        return ""

    def get_users(self):
        return self.channel["users"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # In self.publish_template, we set a querystring to prod to signal
        # different static path handling
        production = self.request.GET.get("env", "dev") == "prod"
        context["production"] = production
        # When publishing, we use a subpath to determine relative paths
        context["subpath"] = self.request.GET.get("subpath", "")
        context["now"] = datetime.now()

        return context
