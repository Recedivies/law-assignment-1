from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

from commons.exceptions import BadRequestException
from commons.patterns.runnable import Runnable
from identities.constants import EMPTY_INPUT, WRONG_CREDENTIALS
from identities.dataclasses import LoginData, UserLoginDataClass
from identities.models import User


class AuthenticationService(Runnable):
    @classmethod
    def generate_login_data(cls, user: User) -> LoginData:
        token, created = Token.objects.get_or_create(user=user)
        return LoginData(token=token.key)

    @classmethod
    def run(cls, email: str, password: str) -> UserLoginDataClass:
        """
        Service for authenticating user from a combination of email & password.
        """
        if not email or not password:
            raise BadRequestException(EMPTY_INPUT)

        authenticated_user: User = authenticate(email=email, password=password)

        if not authenticated_user:
            raise BadRequestException(WRONG_CREDENTIALS)

        login_data = cls.generate_login_data(user=authenticated_user)

        return UserLoginDataClass(
            token=login_data.token,
            user=authenticated_user,
        )
