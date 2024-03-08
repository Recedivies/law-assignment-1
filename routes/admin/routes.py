from django.contrib import admin

from routes.models import Route


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    """Admin View for Route"""

    list_display = ("name", "methods", "hosts", "paths")

    search_fields = ["name", "methods"]
    ordering = ["-created_at"]
    sortable_by = ["created_at"]
