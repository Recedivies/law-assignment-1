from rest_framework import serializers

from commons.serializers import ReadOnlySerializer


class ServiceRequestSerializer(ReadOnlySerializer):
    name = serializers.CharField(required=True)
    host = serializers.CharField(required=True)
    port = serializers.IntegerField(required=False)
    path = serializers.CharField(required=False)
    enabled = serializers.BooleanField(default=True)
    timeout = serializers.IntegerField(required=False)


class ServiceResponseSerializer(ReadOnlySerializer):
    service_id = serializers.UUIDField(source="id")
    name = serializers.CharField()
    host = serializers.CharField()
    port = serializers.IntegerField()
    path = serializers.CharField()


class ListServiceResponseSerializer(ReadOnlySerializer):
    services = serializers.ListField(child=ServiceResponseSerializer())


class UpdateServiceRequestSerializer(ReadOnlySerializer):
    name = serializers.CharField(required=True)
    host = serializers.CharField(required=True)
    port = serializers.IntegerField(required=True)
    path = serializers.CharField(required=True)
    enabled = serializers.BooleanField(required=True)
    timeout = serializers.IntegerField(required=True)


class UpdateServiceResponseSerializer(ServiceResponseSerializer):
    enabled = serializers.BooleanField()
    timeout = serializers.IntegerField()
