from django.urls import path, re_path  # noqa

from routes.views.detail_route import DetailRouteAPI
from routes.views.route import RouteAPI

routes_urls = [
    path("", RouteAPI.as_view(), name="route-api"),
    path("<uuid:route_id>/", DetailRouteAPI.as_view(), name="detail-route-api"),
    re_path(r"^(?P<route_name>[\w\s-]+)/$", DetailRouteAPI.as_view(), name="detail-route-api-by-name"),
]

urlpatterns = []
urlpatterns += routes_urls
