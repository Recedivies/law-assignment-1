import uuid
from typing import Optional

from commons.exceptions import NotFoundRequestException
from commons.patterns.runnable import Runnable
from identities.models import User
from plugins.constants import PLUGIN_NOT_FOUND
from plugins.models import Plugin
from plugins.selectors.plugin import PluginSelector


class DeletePluginService(Runnable):
    @classmethod
    def run(cls, user: User, plugin_id: Optional[uuid.UUID] = None, plugin_instance_name: Optional[str] = None) -> None:
        try:
            plugin = PluginSelector.get_plugin_by_id_or_name(
                user=user, plugin_id=plugin_id, plugin_instance_name=plugin_instance_name
            )
        except Plugin.DoesNotExist:
            raise NotFoundRequestException(PLUGIN_NOT_FOUND)

        plugin.delete()
