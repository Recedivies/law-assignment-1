from rest_framework import serializers

from commons.serializers import ReadOnlySerializer


class PluginRequestSerializer(ReadOnlySerializer):
    name = serializers.CharField(required=True)
    instance_name = serializers.CharField(required=True)
    config = serializers.JSONField(required=True)
    enabled = serializers.BooleanField(required=False, default=True)
    service_id = serializers.UUIDField()

    def validate_name(self, value):
        valid_names = ["caching", "rate-limiting", "request-validator"]
        if value not in valid_names:
            raise serializers.ValidationError(
                "Invalid plugin name. Must be one of: caching, rate-limiting, request-validator"
            )
        return value


class PluginResponseSerializer(ReadOnlySerializer):
    plugin_id = serializers.UUIDField(source="id")
    name = serializers.CharField()
    config = serializers.JSONField()
    instance_name = serializers.CharField()
    enabled = serializers.BooleanField()
    service_name = serializers.CharField(source="service__name")


class ListPluginResponseSerializer(ReadOnlySerializer):
    plugins = serializers.ListField(child=PluginResponseSerializer())
