from rest_framework import serializers

from commons.serializers import ReadOnlySerializer


class RequestSerializer(ReadOnlySerializer):
    service_id = serializers.UUIDField(required=True)
    method = serializers.CharField(required=True)
    host = serializers.CharField(required=True)
    path = serializers.CharField(required=False, default="/")
    port = serializers.IntegerField(required=False, default=443)
    request_body = serializers.DictField(required=False, read_only=True)

    def validate_methods(self, value):
        valid_methods = ["GET", "POST", "PUT", "DELETE"]
        for val in value:
            if val not in valid_methods:
                raise serializers.ValidationError("Invalid methods name. Must be one of: GET, POST, PUT, DELETE")
        return value
