from rest_framework import serializers

from commons.serializers import ReadOnlySerializer


class RouteRequestSerializer(ReadOnlySerializer):
    name = serializers.CharField(required=True)
    methods = serializers.ListSerializer(child=serializers.CharField(required=True))
    hosts = serializers.ListSerializer(child=serializers.CharField(required=True))
    paths = serializers.ListSerializer(child=serializers.CharField(required=True))
    service_id = serializers.UUIDField(required=True)


class RouteResponseSerializer(ReadOnlySerializer):
    route_id = serializers.UUIDField(source="id")
    name = serializers.CharField(required=True)
    methods = serializers.ListSerializer(child=serializers.CharField(required=True))
    hosts = serializers.ListSerializer(child=serializers.CharField(required=True))
    paths = serializers.ListSerializer(child=serializers.CharField(required=True))
    service_id = serializers.UUIDField(required=True)


class ListRouteResponseSerializer(ReadOnlySerializer):
    routes = serializers.ListField(child=RouteResponseSerializer())
