import uuid
from typing import Optional

from commons.dataclasses import BaseDataClass
from commons.exceptions import UnprocessableEntityException
from commons.patterns.runnable import Runnable
from identities.models import User
from services.constants import DUPLICATED_NAME
from services.models import Service


class CreateServiceData(BaseDataClass):
    id: uuid.UUID
    name: str
    host: str
    port: int
    path: str
    enabled: bool
    timeout: int


class CreateServiceDataService(Runnable):
    @classmethod
    def run(
        cls,
        user: User,
        name: str,
        host: str,
        port: Optional[int] = 80,
        path: Optional[str] = "/",
        enabled: Optional[bool] = True,
        timeout: Optional[int] = 6000,
    ) -> CreateServiceData:
        if Service.objects.filter(name=name, user=user).exists():
            raise UnprocessableEntityException(DUPLICATED_NAME)

        service = Service.objects.create(
            name=name, host=host, port=port, path=path, enabled=enabled, timeout=timeout, user=user
        )

        return CreateServiceData(
            id=service.id,
            name=service.name,
            host=service.host,
            port=service.port,
            path=service.path,
            enabled=service.enabled,
            timeout=service.timeout,
        )
