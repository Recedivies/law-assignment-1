import uuid
from typing import Optional

from commons.dataclasses import BaseDataClass
from commons.exceptions import NotFoundRequestException, UnprocessableEntityException
from commons.patterns.runnable import Runnable
from identities.models import User
from services.constants import DUPLICATED_NAME, SERVICE_NOT_FOUND
from services.models import Service
from services.selectors.service import ServiceSelector


class UpdateServiceData(BaseDataClass):
    id: uuid.UUID
    name: str
    host: str
    port: int
    path: str
    enabled: bool
    timeout: int


class UpdateServiceDataService(Runnable):
    @classmethod
    def run(
        cls,
        user: User,
        name: str,
        host: str,
        port: int,
        path: str,
        enabled: bool,
        timeout: int,
        service_id: Optional[str] = None,
        service_name: Optional[str] = None,
    ) -> UpdateServiceData:
        try:
            service = ServiceSelector.get_service_by_id_or_name(user, service_id=service_id, service_name=service_name)
        except Service.DoesNotExist:
            raise NotFoundRequestException(SERVICE_NOT_FOUND)

        if Service.objects.filter(name=name, user=user).exclude(id=service.id, name=name).exists():
            raise UnprocessableEntityException(DUPLICATED_NAME)

        service.name = name
        service.host = host
        service.port = port
        service.path = path
        service.enabled = enabled
        service.timeout = timeout

        service.save()

        return UpdateServiceData(
            id=service.id,
            name=service.name,
            host=service.host,
            port=service.port,
            path=service.path,
            enabled=service.enabled,
            timeout=service.timeout,
        )
