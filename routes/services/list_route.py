import uuid

from django.db.models import QuerySet

from commons.dataclasses import BaseDataClass
from commons.patterns.runnable import Runnable
from routes.models import Route


class ListRouteData(BaseDataClass):
    routes: QuerySet[Route]

    class Config:
        arbitrary_types_allowed = True


class ListRouteService(Runnable):
    @classmethod
    def run(cls, user_id: uuid.UUID) -> ListRouteData:
        qs = Route.objects.filter(user_id=user_id)

        return ListRouteData(routes=qs)
