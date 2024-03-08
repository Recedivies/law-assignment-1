from django.urls import path, re_path  # noqa

from plugins.views.detail_plugin import DetailPluginAPI
from plugins.views.plugin import PluginAPI

plugins_urls = [
    path("", PluginAPI.as_view(), name="plugin-api"),
    path("<uuid:plugin_id>/", DetailPluginAPI.as_view(), name="detail-plugin-api"),
    re_path(r"^(?P<plugin_instance_name>[\w\s-]+)/$", DetailPluginAPI.as_view(), name="detail-plugin-api-by-name"),
]

urlpatterns = []
urlpatterns += plugins_urls
