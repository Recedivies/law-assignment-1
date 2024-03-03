from typing import Any

from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from services.serializers import ServiceResponseSerializer, UpdateServiceRequest, UpdateServiceResponseSerializer
from services.services.delete_service import DeleteServiceDataService
from services.services.get_service import GetServiceDataService
from services.services.update_service import UpdateServiceDataService


class DetailServiceInstanceAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        service_id = self.kwargs.get("service_id")
        service_name = self.kwargs.get("service_name")

        service = GetServiceDataService.run(user=request.user, service_id=service_id, service_name=service_name)

        return Response(ServiceResponseSerializer(service).data)

    def put(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = UpdateServiceRequest(data=request.data)
        serializer.is_valid(raise_exception=True)

        service_id = self.kwargs.get("service_id")
        service_name = self.kwargs.get("service_name")

        with transaction.atomic():
            response_data = UpdateServiceDataService.run(
                user=request.user, service_id=service_id, service_name=service_name, **serializer.validated_data
            )

            return Response(UpdateServiceResponseSerializer(response_data).data)

    @transaction.atomic
    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        service_id = self.kwargs.get("service_id")
        service_name = self.kwargs.get("service_name")

        DeleteServiceDataService.run(user=request.user, service_id=service_id, service_name=service_name)

        return Response(
            {"message": "Successfully deleted service"},
            status=status.HTTP_204_NO_CONTENT,
        )
