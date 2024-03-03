from rest_framework.fields import CharField, EmailField

from commons.serializers import ReadOnlySerializer


class LoginRequest(ReadOnlySerializer):
    email = EmailField()
    password = CharField()


class RegisterRequest(ReadOnlySerializer):
    email = EmailField()
    full_name = CharField()
    password = CharField()


class UserAuthData(ReadOnlySerializer):
    full_name = CharField()
    email = CharField()


class AuthResponseSerializer(ReadOnlySerializer):
    user = UserAuthData()
    token = CharField()
