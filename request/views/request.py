from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from request.serializers import RequestSerializer
from request.services.request_handler import RequestHandlerService


class RequestAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = RequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        additional_field = request.data.get("request_body")
        ip = self._get_client_ip(request=request)

        with transaction.atomic():
            response_data = RequestHandlerService.run(
                user=request.user, **serializer.validated_data, ip=ip, request_body=additional_field
            )

            return Response(response_data)

    def _get_client_ip(cls, request: Request) -> str:
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
