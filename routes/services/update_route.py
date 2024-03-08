import uuid
from typing import List, Optional

from commons.dataclasses import BaseDataClass
from commons.exceptions import NotFoundRequestException, UnprocessableEntityException
from commons.patterns.runnable import Runnable
from identities.models import User
from routes.constants import DUPLICATED_NAME, ROUTE_NOT_FOUND
from routes.models import Route
from routes.selectors.route import RouteSelector
from services.constants import SERVICE_NOT_FOUND
from services.models import Service
from services.selectors.service import ServiceSelector


class UpdateRouteData(BaseDataClass):
    id: uuid.UUID
    name: str
    methods: List[str]
    hosts: List[str]
    paths: List[str]
    service_id: uuid.UUID


class UpdateRouteService(Runnable):
    @classmethod
    def run(
        cls,
        user: User,
        name: str,
        methods: List[str],
        hosts: List[str],
        paths: List[str],
        service_id: uuid.UUID,
        route_id: Optional[uuid.UUID] = None,
        route_name: Optional[str] = None,
    ) -> UpdateRouteData:
        try:
            route = RouteSelector.get_route_by_id_or_name(user, route_id=route_id, route_name=route_name)
            service = ServiceSelector.get_service_by_id_or_name(user, service_id=service_id)
        except Route.DoesNotExist:
            raise NotFoundRequestException(ROUTE_NOT_FOUND)
        except Service.DoesNotExist:
            raise NotFoundRequestException(SERVICE_NOT_FOUND)

        if Route.objects.filter(name=name, user=user).exclude(id=route.id).exists():
            raise UnprocessableEntityException(DUPLICATED_NAME)

        route.name = name
        route.methods = methods
        route.hosts = hosts
        route.paths = paths
        route.service = service

        route.save()

        return UpdateRouteData(
            id=route.id,
            name=route.name,
            methods=route.methods,
            hosts=route.hosts,
            paths=route.paths,
            service_id=route.service.id,
        )
