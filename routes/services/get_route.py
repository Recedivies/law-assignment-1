import uuid
from typing import List, Optional

from commons.dataclasses import BaseDataClass
from commons.exceptions import NotFoundRequestException
from commons.patterns.runnable import Runnable
from identities.models import User
from routes.constants import ROUTE_NOT_FOUND
from routes.models import Route
from routes.selectors.route import RouteSelector


class GetRouteData(BaseDataClass):
    id: uuid.UUID
    name: str
    methods: List[str]
    hosts: List[str]
    paths: List[str]
    service_id: uuid.UUID


class GetRouteService(Runnable):
    @classmethod
    def run(cls, user: User, route_id: Optional[uuid.UUID] = None, route_name: Optional[str] = None) -> GetRouteData:
        try:
            route = RouteSelector.get_route_by_id_or_name(user, route_id=route_id, route_name=route_name)
        except Route.DoesNotExist:
            raise NotFoundRequestException(ROUTE_NOT_FOUND)

        return GetRouteData(
            id=route.id,
            name=route.name,
            methods=route.methods,
            hosts=route.hosts,
            paths=route.paths,
            service_id=route.service.id,
        )
