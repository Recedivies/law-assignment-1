from django.contrib import admin

from plugins.models import Plugin


@admin.register(Plugin)
class PluginAdmin(admin.ModelAdmin):
    """Admin View for Plugin"""

    list_display = ("name", "instance_name", "config", "enabled")

    search_fields = ["name", "instance_name"]
    ordering = ["-created_at"]
    sortable_by = ["created_at"]
