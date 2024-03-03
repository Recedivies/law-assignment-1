from rest_framework import serializers

from commons.exceptions import ValidationErrorException


class ReadOnlySerializer(serializers.Serializer):
    def create(self, validated_data):
        raise ValidationErrorException(message="create is not allowed.")

    def update(self, instance, validated_data):
        raise ValidationErrorException(message="update is not allowed.")
