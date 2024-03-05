from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from routes.serializers import ListRouteResponseSerializer, RouteRequestSerializer, RouteResponseSerializer
from routes.services.create_route import CreateRouteService
from routes.services.list_route import ListRouteService


class RouteAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request) -> Response:
        list_route = ListRouteService.run(user_id=request.user.id)

        return Response(ListRouteResponseSerializer(list_route.dict()).data)

    def post(self, request: Request) -> Response:
        serializer = RouteRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            response_data = CreateRouteService.run(user=request.user, **serializer.validated_data)

            return Response(RouteResponseSerializer(response_data).data)
