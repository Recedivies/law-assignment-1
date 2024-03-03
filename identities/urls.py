from django.urls import path  # noqa

from identities.views.login import LoginAPI
from identities.views.register import RegisterAPI

identities_urls = [
    path("login/", LoginAPI.as_view(), name="user-login-api"),
    path("register/", RegisterAPI.as_view(), name="user-register-api"),
]

urlpatterns = []
urlpatterns += identities_urls
