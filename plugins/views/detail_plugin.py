from typing import Any

from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from plugins.serializers import PluginRequestSerializer, PluginResponseSerializer
from plugins.services.delete_plugin import DeletePluginService
from plugins.services.get_plugin import GetPluginService
from plugins.services.update_plugin import UpdatePluginService


class DetailPluginAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        plugin_id = self.kwargs.get("plugin_id")
        plugin_instance_name = self.kwargs.get("plugin_instance_name")

        route = GetPluginService.run(user=request.user, plugin_id=plugin_id, plugin_instance_name=plugin_instance_name)

        return Response(PluginResponseSerializer(route).data)

    def put(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = PluginRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        plugin_id = self.kwargs.get("plugin_id")
        plugin_instance_name = self.kwargs.get("plugin_instance_name")

        with transaction.atomic():
            response_data = UpdatePluginService.run(
                user=request.user,
                plugin_id=plugin_id,
                plugin_instance_name=plugin_instance_name,
                **serializer.validated_data
            )

            return Response(PluginResponseSerializer(response_data).data)

    @transaction.atomic
    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        plugin_id = self.kwargs.get("plugin_id")
        plugin_instance_name = self.kwargs.get("plugin_instance_name")

        DeletePluginService.run(user=request.user, plugin_id=plugin_id, plugin_instance_name=plugin_instance_name)

        return Response(
            {"message": "Successfully deleted plugin"},
            status=status.HTTP_204_NO_CONTENT,
        )
