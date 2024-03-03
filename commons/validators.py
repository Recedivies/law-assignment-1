from rest_framework import serializers

from commons.constants import NUMBER_ONLY


def number_only(value: str):
    if not value.isnumeric():
        raise serializers.ValidationError(NUMBER_ONLY)
