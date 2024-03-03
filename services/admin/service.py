from django.contrib import admin

from services.models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """Admin View for Service"""

    list_display = ("name", "host", "port", "path", "enabled")

    search_fields = ["name", "host"]
    ordering = ["-created_at"]
    sortable_by = ["created_at"]
