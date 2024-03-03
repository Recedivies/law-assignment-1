from django.db import transaction
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from identities.serializers import AuthResponseSerializer, RegisterRequest
from identities.services.registration import RegistrationService


class RegisterAPI(APIView):
    permission_classes = (AllowAny,)

    def post(self, request: Request, **kwargs) -> Response:
        serializer = RegisterRequest(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            user_register_data = RegistrationService.run(**serializer.validated_data)

            return Response(AuthResponseSerializer(user_register_data).data)
