from django.contrib import admin

from identities.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin View for User"""

    list_display = ("full_name", "email", "created_at")
    list_display_links = ["full_name"]

    search_fields = ["full_name", "email"]
    ordering = ["-created_at"]
    sortable_by = ["created_at"]
