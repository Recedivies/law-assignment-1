import uuid

from commons.dataclasses import BaseDataClass
from plugins.constants import CONFIG_TYPE


class DetailPluginData(BaseDataClass):
    id: uuid.UUID
    name: str
    instance_name: str
    config: CONFIG_TYPE
    enabled: bool
    service__name: str
