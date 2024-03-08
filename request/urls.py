from django.urls import path  # noqa

from request.views.request import RequestAPI

request_urls = [path("", RequestAPI.as_view(), name="request-api")]

urlpatterns = []
urlpatterns += request_urls
