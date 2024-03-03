from typing import Optional

from django.db import IntegrityError

from commons.exceptions import BadRequestException
from commons.patterns.runnable import Runnable
from identities.constants import EMAIL_PHONE_ALREADY_USE
from identities.dataclasses import UserRegisterDataClass
from identities.models import User
from identities.services.authentication import AuthenticationService


class RegistrationService(Runnable):
    @classmethod
    def run(
        cls,
        full_name: Optional[str] = "",
        email: Optional[str] = None,
        password: Optional[str] = None,
    ) -> UserRegisterDataClass:
        try:
            user = User.objects.create_user(
                email=email,
                full_name=full_name,
                password=password,
                is_active=True,
            )
        except IntegrityError:
            raise BadRequestException(EMAIL_PHONE_ALREADY_USE)
        except ValueError as e:
            raise BadRequestException(str(e))

        login_data = AuthenticationService.generate_login_data(user)

        return UserRegisterDataClass(token=login_data.token, user=user)
