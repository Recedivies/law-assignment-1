import uuid
from typing import Optional

from commons.dataclasses import BaseDataClass
from commons.exceptions import NotFoundRequestException
from commons.patterns.runnable import Runnable
from identities.models import User
from services.constants import SERVICE_NOT_FOUND
from services.models import Service
from services.selectors.service import ServiceSelector


class GetServiceData(BaseDataClass):
    id: uuid.UUID
    name: str
    host: str
    port: int
    path: str


class GetServiceDataService(Runnable):
    @classmethod
    def run(cls, user: User, service_id: Optional[str] = None, service_name: Optional[str] = None) -> GetServiceData:
        try:
            service = ServiceSelector.get_service_by_id_or_name(user, service_id=service_id, service_name=service_name)
        except Service.DoesNotExist:
            raise NotFoundRequestException(SERVICE_NOT_FOUND)

        return GetServiceData(
            id=service.id,
            name=service.name,
            host=service.host,
            port=service.port,
            path=service.path,
        )
