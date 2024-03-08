import uuid
from typing import Optional

from commons.dataclasses import BaseDataClass
from commons.exceptions import BadRequestException, NotFoundRequestException, UnprocessableEntityException
from commons.patterns.runnable import Runnable
from identities.models import User
from plugins.constants import (
    CONFIG_TYPE,
    DUPLICATED_NAME,
    INVALID_REQUEST_METHOD,
    INVALID_REQUIRED_BODY_SCHEMA,
    INVALID_TYPE_BODY_SCHEMA,
)
from plugins.models import Plugin
from services.constants import SERVICE_NOT_FOUND
from services.models import Service


class CreatePluginData(BaseDataClass):
    id: uuid.UUID
    name: str
    instance_name: str
    config: CONFIG_TYPE
    enabled: bool
    service__name: str

    class Config:
        arbitrary_types_allowed = True


class CreatePluginService(Runnable):
    @classmethod
    def run(
        cls,
        user: User,
        name: str,
        instance_name: str,
        config: CONFIG_TYPE,
        service_id: uuid.UUID,
        enabled: Optional[bool] = True,
    ) -> CreatePluginData:
        cls._validate(config=config, name=name)

        try:
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            raise NotFoundRequestException(SERVICE_NOT_FOUND)

        if Plugin.objects.filter(instance_name=instance_name, name=name, service=service, user=user).exists():
            raise UnprocessableEntityException(DUPLICATED_NAME)

        plugin = Plugin.objects.create(
            name=name, instance_name=instance_name, config=config, enabled=enabled, service=service, user=user
        )

        return CreatePluginData(
            id=plugin.id,
            name=plugin.name,
            instance_name=plugin.instance_name,
            config=plugin.config,
            enabled=plugin.enabled,
            service__name=plugin.service.name,
        )

    @classmethod
    def _validate(cls, config: CONFIG_TYPE, name: str):
        if name == "caching":
            cls._validate_caching(config=config)

        if name == "request-validator":
            cls._validate_request_validator(config=config)

        if name == "rate-limiting":
            cls._validate_rate_limiting(config=config)

    @classmethod
    def _validate_caching(cls, config: CONFIG_TYPE):
        if not config.get("cache_ttl"):
            raise BadRequestException(INVALID_REQUEST_METHOD)

    @classmethod
    def _validate_request_validator(cls, config: CONFIG_TYPE):
        body_schema = config.get("body_schema", None)
        for item in body_schema:
            for key, _ in item.items():
                if "type" not in key:
                    raise BadRequestException(INVALID_TYPE_BODY_SCHEMA)
                if "required" not in key:
                    raise BadRequestException(INVALID_REQUIRED_BODY_SCHEMA)

    @classmethod
    def _validate_rate_limiting(cls, config: CONFIG_TYPE):
        if not config.get("second"):
            raise BadRequestException(INVALID_REQUEST_METHOD)
