from typing import Optional

from commons.exceptions import NotFoundRequestException
from commons.patterns.runnable import Runnable
from identities.models import User
from routes.constants import ROUTE_NOT_FOUND
from routes.models import Route
from routes.selectors.route import RouteSelector


class DeleteRouteService(Runnable):
    @classmethod
    def run(cls, user: User, route_id: Optional[str] = None, route_name: Optional[str] = None) -> None:
        try:
            route = RouteSelector.get_route_by_id_or_name(user, route_id=route_id, route_name=route_name)
        except Route.DoesNotExist:
            raise NotFoundRequestException(ROUTE_NOT_FOUND)

        route.delete()
