import os

from django.conf import settings as project_settings
from django.test.client import RequestFactory
from django.utils.text import slugify
from rest_framework.renderers import JSONRenderer
from slackchatbakery.utils.aws import defaults, get_bucket
from slackchatbakery.conf import settings


class StaticsPublishingMixin(object):
    """
    Handles publishing templates, serialized context and JS/CSS bundles to S3.
    Bundles are published to a directory at paths with this pattern:
    election-results/2018/live-analysis/midterms/cdn/{bundle_file}
    """

    def get_request(self, production=False, subpath=""):
        """Construct a request we can use to render the view.
        Send environment variable in querystring to determine whether
        we're using development static file URLs or production."""
        if production:
            env = {"env": "prod"}
        else:
            env = {"env": "dev"}
        kwargs = {**{"subpath": subpath}, **env}
        return RequestFactory().get("", kwargs)

    def get_serialized_context(self):
        """OVERWRITE this method to return serialized context data.
        Use the serializer for the page you would hit.
        Used to bake out serialized context data.
        """
        return {}

    def publish_serialized_data(self, subpath="", **kwargs):
        """Publishes serialized data."""
        data = self.get_serialized_data(**kwargs)
        json_string = JSONRenderer().render(data)  # noqa
        key = os.path.join(
            settings.S3_UPLOAD_ROOT,
            self.get_publish_path(),
            os.path.join(subpath, "data.json"),
        )

        print(">>> Publish data to: ", key)
        bucket = get_bucket()
        bucket.put_object(
            Key=key,
            ACL=defaults.ACL,
            Body=json_string,
            CacheControl=defaults.CACHE_HEADER,
            ContentType="application/json",
        )

        return data
