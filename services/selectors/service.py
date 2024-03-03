from typing import Optional

from django.db.models import Q, QuerySet

from identities.models import User
from services.models import Service


class ServiceSelector:
    @staticmethod
    def get_service_by_id_or_name(
        user: User, service_id: Optional[str] = None, service_name: Optional[str] = None
    ) -> QuerySet[Service]:
        filter_query = Q(user_id=user.id)

        if service_id:
            filter_query &= Q(id=service_id)
        if service_name:
            filter_query &= Q(name=service_name)

        return Service.objects.get(filter_query)
