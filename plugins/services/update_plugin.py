import uuid
from typing import Optional

from commons.exceptions import NotFoundRequestException, UnprocessableEntityException
from commons.patterns.runnable import Runnable
from identities.models import User
from plugins.constants import CONFIG_TYPE, DUPLICATED_NAME, PLUGIN_NOT_FOUND
from plugins.dataclasses import DetailPluginData
from plugins.models import Plugin
from plugins.selectors.plugin import PluginSelector
from services.constants import SERVICE_NOT_FOUND
from services.models import Service
from services.selectors.service import ServiceSelector


class UpdatePluginService(Runnable):
    @classmethod
    def run(
        cls,
        user: User,
        name: str,
        instance_name: str,
        config: CONFIG_TYPE,
        service_id: uuid.UUID,
        enabled: Optional[bool] = True,
        plugin_id: Optional[uuid.UUID] = None,
        plugin_instance_name: Optional[str] = None,
    ) -> DetailPluginData:
        try:
            plugin = PluginSelector.get_plugin_by_id_or_name(
                user=user, plugin_id=plugin_id, plugin_instance_name=plugin_instance_name
            )
            service = ServiceSelector.get_service_by_id_or_name(user, service_id=service_id)
        except Plugin.DoesNotExist:
            raise NotFoundRequestException(PLUGIN_NOT_FOUND)
        except Service.DoesNotExist:
            raise NotFoundRequestException(SERVICE_NOT_FOUND)

        if (
            Plugin.objects.filter(instance_name=instance_name, service=service, user=user)
            .exclude(id=plugin.id)
            .exists()
        ):
            raise UnprocessableEntityException(DUPLICATED_NAME)

        plugin.name = name
        plugin.instance_name = instance_name
        plugin.config = config
        plugin.enabled = enabled
        plugin.service = service

        plugin.save()

        return DetailPluginData(
            id=plugin.id,
            name=plugin.name,
            instance_name=plugin.instance_name,
            config=plugin.config,
            enabled=plugin.enabled,
            service__name=plugin.service.name,
        )
