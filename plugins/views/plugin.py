from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from plugins.serializers import ListPluginResponseSerializer, PluginRequestSerializer, PluginResponseSerializer
from plugins.services.create_plugin import CreatePluginService
from plugins.services.list_plugin import ListPluginService


class PluginAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request) -> Response:
        list_plugin = ListPluginService.run(user_id=request.user.id)

        return Response(ListPluginResponseSerializer(list_plugin.dict()).data)

    def post(self, request: Request) -> Response:
        serializer = PluginRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            response_data = CreatePluginService.run(user=request.user, **serializer.validated_data)

            return Response(PluginResponseSerializer(response_data).data)
