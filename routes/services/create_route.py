import uuid
from typing import List

from commons.dataclasses import BaseDataClass
from commons.exceptions import BadRequestException, NotFoundRequestException, UnprocessableEntityException
from commons.patterns.runnable import Runnable
from identities.models import User
from routes.constants import DUPLICATED_NAME, ROUTE_NOT_FOUND
from routes.models import Route
from services.constants import SERVICE_NOT_FOUND
from services.models import Service


class CreateRouteData(BaseDataClass):
    id: uuid.UUID
    name: str
    methods: List[str]
    hosts: List[str]
    paths: List[str]
    service_id: uuid.UUID


class CreateRouteService(Runnable):
    @classmethod
    def run(
        cls, user: User, name: str, methods: List[str], hosts: List[str], paths: List[str], service_id: uuid.UUID
    ) -> CreateRouteData:
        try:
            service = Service.objects.get(id=service_id)
        except Service.DoesNotExist:
            raise NotFoundRequestException(ROUTE_NOT_FOUND)

        if not service:
            raise BadRequestException(SERVICE_NOT_FOUND)

        if Route.objects.filter(name=name, user=user).exists():
            raise UnprocessableEntityException(DUPLICATED_NAME)

        route = Route.objects.create(name=name, methods=methods, hosts=hosts, paths=paths, service=service, user=user)

        return CreateRouteData(
            id=route.id,
            name=route.name,
            methods=route.methods,
            hosts=route.hosts,
            paths=route.paths,
            service_id=route.service.id,
        )
