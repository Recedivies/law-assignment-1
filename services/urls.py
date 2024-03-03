from django.urls import path, re_path  # noqa

from services.views.detail_service import DetailServiceInstanceAPI
from services.views.service import ServiceInstaceAPI

services_urls = [
    path("", ServiceInstaceAPI.as_view(), name="list-service-api"),
    path("<uuid:service_id>/", DetailServiceInstanceAPI.as_view(), name="detail-service-instance-api"),
    re_path(
        r"^(?P<service_name>[\w\s-]+)/$", DetailServiceInstanceAPI.as_view(), name="detail-service-instance-api-by-name"
    ),
]

urlpatterns = []
urlpatterns += services_urls
