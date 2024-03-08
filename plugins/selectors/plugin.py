import uuid
from typing import Optional

from django.db.models import Q, QuerySet

from identities.models import User
from plugins.models import Plugin


class PluginSelector:
    @staticmethod
    def get_plugin_by_id_or_name(
        user: User, plugin_id: Optional[uuid.UUID] = None, plugin_instance_name: Optional[str] = None
    ) -> QuerySet[Plugin]:
        filter_query = Q(user_id=user.id)

        if plugin_id:
            filter_query &= Q(id=plugin_id)
        if plugin_instance_name:
            filter_query &= Q(instance_name=plugin_instance_name)

        return Plugin.objects.get(filter_query)
