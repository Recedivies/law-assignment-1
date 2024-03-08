import uuid

from django.db.models import QuerySet

from commons.dataclasses import BaseDataClass
from commons.patterns.runnable import Runnable
from plugins.models import Plugin


class ListPluginData(BaseDataClass):
    plugins: QuerySet[Plugin]

    class Config:
        arbitrary_types_allowed = True


class ListPluginService(Runnable):
    @classmethod
    def run(cls, user_id: uuid.UUID) -> ListPluginData:
        qs = Plugin.objects.filter(user_id=user_id).values(
            "id", "name", "instance_name", "config", "enabled", "service__name"
        )

        return ListPluginData(plugins=qs)
