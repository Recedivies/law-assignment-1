from typing import Any

from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from routes.serializers import RouteRequestSerializer, RouteResponseSerializer
from routes.services.delete_route import DeleteRouteService
from routes.services.get_route import GetRouteService
from routes.services.update_route import UpdateRouteService


class DetailRouteAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        route_id = self.kwargs.get("route_id")
        route_name = self.kwargs.get("route_name")

        route = GetRouteService.run(user=request.user, route_id=route_id, route_name=route_name)

        return Response(RouteResponseSerializer(route).data)

    def put(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = RouteRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        route_id = self.kwargs.get("route_id")
        route_name = self.kwargs.get("route_name")

        with transaction.atomic():
            response_data = UpdateRouteService.run(
                user=request.user, route_id=route_id, route_name=route_name, **serializer.validated_data
            )

            return Response(RouteResponseSerializer(response_data).data)

    @transaction.atomic
    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        route_id = self.kwargs.get("route_id")
        route_name = self.kwargs.get("route_name")

        DeleteRouteService.run(user=request.user, route_id=route_id, route_name=route_name)

        return Response(
            {"message": "Successfully deleted route"},
            status=status.HTTP_204_NO_CONTENT,
        )
