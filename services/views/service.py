from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from services.serializers import ListServiceResponseSerializer, ServiceRequest, ServiceResponseSerializer
from services.services.create_service import CreateServiceDataService
from services.services.list_service import ListServiceDataService


class ServiceInstaceAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request) -> Response:
        list_service = ListServiceDataService.run(user_id=request.user.id)

        return Response(ListServiceResponseSerializer(list_service.dict()).data)

    def post(self, request: Request) -> Response:
        serializer = ServiceRequest(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            response_data = CreateServiceDataService.run(user=request.user, **serializer.validated_data)

            return Response(ServiceResponseSerializer(response_data).data)
