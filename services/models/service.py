from django.db import models

from commons.base_model import BaseModel


class Service(BaseModel):
    name = models.CharField(max_length=64)
    host = models.CharField(max_length=128)
    port = models.PositiveIntegerField()
    path = models.CharField(max_length=32)
    enabled = models.BooleanField(default=True)
    timeout = models.PositiveIntegerField()
    user = models.ForeignKey(to="identities.User", on_delete=models.CASCADE, related_name="services")

    class Meta:
        db_table = "service"
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.name
