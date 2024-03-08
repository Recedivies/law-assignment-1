from django.db import models

from commons.base_model import BaseModel


class Plugin(BaseModel):
    name = models.CharField(max_length=64)
    instance_name = models.CharField(max_length=64)
    config = models.JSONField()
    enabled = models.BooleanField(default=True)

    user = models.ForeignKey(to="identities.User", on_delete=models.CASCADE, related_name="user_plugins")
    service = models.ForeignKey(to="services.Service", on_delete=models.CASCADE, related_name="service_plugins")

    class Meta:
        db_table = "plugin"
        verbose_name = "Plugin"
        verbose_name_plural = "Plugins"

    def __str__(self):
        return self.name
