from django.contrib.postgres.fields import ArrayField
from django.db import models

from commons.base_model import BaseModel


class Route(BaseModel):
    name = models.CharField(max_length=64)
    methods = ArrayField(models.CharField(max_length=32))
    hosts = ArrayField(models.CharField(max_length=128))
    paths = ArrayField(models.CharField(max_length=32))

    user = models.ForeignKey(to="identities.User", on_delete=models.CASCADE, related_name="user_routes")
    service = models.ForeignKey(to="services.Service", on_delete=models.CASCADE, related_name="service_routes")

    class Meta:
        db_table = "route"
        verbose_name = "Route"
        verbose_name_plural = "Routes"

    def __str__(self):
        return self.name
