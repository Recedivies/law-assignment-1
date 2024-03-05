import uuid
from typing import Optional

from django.db.models import Q, QuerySet

from identities.models import User
from routes.models import Route


class RouteSelector:
    @staticmethod
    def get_route_by_id_or_name(
        user: User, route_id: Optional[uuid.UUID] = None, route_name: Optional[str] = None
    ) -> QuerySet[Route]:
        filter_query = Q(user_id=user.id)

        if route_id:
            filter_query &= Q(id=route_id)
        if route_name:
            filter_query &= Q(name=route_name)

        return Route.objects.get(filter_query)
