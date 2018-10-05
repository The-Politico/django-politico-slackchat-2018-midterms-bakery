from django.urls import path

from .views import Endpoint

urlpatterns = [path("", Endpoint.as_view(), name="slackchatbakery-endpoint")]
