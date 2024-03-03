import uuid

from django.db.models import QuerySet

from commons.dataclasses import BaseDataClass
from commons.patterns.runnable import Runnable
from services.models import Service


class ListServiceData(BaseDataClass):
    services: QuerySet[Service]

    class Config:
        arbitrary_types_allowed = True


class ListServiceDataService(Runnable):
    @classmethod
    def run(cls, user_id: uuid.UUID) -> ListServiceData:
        qs = Service.objects.filter(user_id=user_id)

        return ListServiceData(services=qs)
