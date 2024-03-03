from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from identities.serializers import AuthResponseSerializer, LoginRequest
from identities.services.authentication import AuthenticationService


class LoginAPI(APIView):
    permission_classes = (AllowAny,)

    def post(self, request: Request, **kwargs) -> Response:
        serializer = LoginRequest(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_login_data = AuthenticationService.run(**serializer.validated_data)

        return Response(AuthResponseSerializer(user_login_data).data)
