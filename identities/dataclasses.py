from commons.dataclasses import BaseDataClass
from identities.models import User


class UserLoginDataClass(BaseDataClass):
    token: str
    user: User

    class Config:
        arbitrary_types_allowed = True


class UserRegisterDataClass(BaseDataClass):
    token: str
    user: User

    class Config:
        arbitrary_types_allowed = True


class LoginData(BaseDataClass):
    token: str
