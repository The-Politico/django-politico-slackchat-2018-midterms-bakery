from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from slackchatbakery.conf import settings


class Endpoint(APIView):
    # Open API
    authentication_classes = ()
    permission_classes = ()

    valid_request_types = [
        "url_verification",
        "update_notification",
        "republish_request",
    ]

    def get(self, request, format=None):
        return Response(200)

    def post(self, request, format=None):
        from slackchatbakery.celery import (
            publish_slackchat,
            publish_all_states,
            render_chat,
        )

        data = request.data
        request_token = data.get("token", None)
        request_type = data.get("type", None)

        if request_token != settings.WEBHOOK_VERIFICATION_TOKEN:
            return Response(status=status.HTTP_403_FORBIDDEN)

        if request_type not in self.valid_request_types:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if request_type == "url_verification":
            return Response(
                data=data.get("challenge"), status=status.HTTP_200_OK
            )

        try:
            channel = data.get("channel")
            chat_type = data.get("chat_type")
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if chat_type == "2018-midterms":
            if request_type == "update_notification":
                publish_slackchat.delay(channel, publish_args=True)
            if request_type == "republish_request":
                publish_slackchat.delay(channel, publish_args=True)
                publish_all_states.delay(channel)
                render_chat.delay()

        return Response(status=status.HTTP_200_OK)
