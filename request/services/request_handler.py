import uuid
from typing import Any, Optional

import requests
from django.conf import settings

from commons.exceptions import NotFoundRequestException, TimeoutRequestException
from commons.patterns.runnable import Runnable
from config.constants import TIMEOUT_REQUEST
from config.services.caching.cache import CacheService
from config.services.rate_limiting.fixed_window_counter import FixedWindowCounterService
from config.services.request_validator.validator import RequestBodyValidatorService
from identities.models import User
from plugins.constants import PLUGIN_NOT_FOUND
from plugins.models import Plugin
from routes.constants import ROUTE_NOT_FOUND
from routes.models import Route
from services.constants import SERVICE_NOT_FOUND
from services.models import Service

logger = settings.LOGGER_INSTANCE


class RequestHandlerService(Runnable):
    @classmethod
    def run(
        cls,
        user: User,
        method: str,
        host: str,
        service_id: uuid.UUID,
        ip: str,
        path: Optional[str] = "/",
        port: Optional[int] = 443,
        **kwargs: Any,
    ) -> Any:
        try:
            service = Service.objects.get(id=service_id, enabled=True)
            routes = Route.objects.filter(hosts__icontains=host, paths__icontains=path, service=service, user=user)
            plugins = Plugin.objects.filter(service=service, user=user, enabled=True)
        except Service.DoesNotExist:
            raise NotFoundRequestException(SERVICE_NOT_FOUND)

        if not routes.exists():
            raise NotFoundRequestException(ROUTE_NOT_FOUND)

        if not plugins.exists():
            raise NotFoundRequestException(PLUGIN_NOT_FOUND)

        URL = f"https://{service.host}:{service.port}{service.path}"
        logger.info(URL)
        logger.info(plugins)

        config_caching = None
        config_rate_limiting = None
        caching_key = None
        rate_limiting_key = None
        cached_data = None
        request_body = None

        for plugin in plugins:
            if plugin.name == "caching":
                config_caching = plugin.config
                caching_key = f"{plugin.name}:{user.id}:{service_id}"
                cached_data = CacheService.run(cache_key=caching_key)

            if plugin.name == "request-validator":
                RequestBodyValidatorService.run(config=plugin.config, **kwargs)
                request_body = kwargs.get("request_body", None)

            if plugin.name == "rate-limiting":
                limit_by = plugin.config.get("limit_by ", "ip")

                if limit_by == "ip":
                    rate_limiting_key = f"{plugin.name}:ip:{ip}:{service_id}"

                config_rate_limiting = plugin.config
                FixedWindowCounterService.run(config=plugin.config, cache_key=rate_limiting_key)

        if rate_limiting_key:
            path = config_rate_limiting.get("path ", "")
            URL = f"{URL}{path}"

        if cached_data:
            return cached_data

        response_data = cls._make_request(method=method, URL=URL, timeout=service.timeout, request_body=request_body)
        if caching_key:
            CacheService.set_cache(key=caching_key, value=response_data, config=config_caching)

        return response_data

    @classmethod
    def _make_request(
        cls,
        method: str,
        URL: str,
        timeout: int,  # 1000 = 1s
        request_body: Any = None,
    ):
        methods = {
            "GET": requests.get,
            "POST": requests.post,
            "PUT": requests.put,
            "DELETE": requests.delete,
        }
        if method in methods:
            try:
                response = methods[method](URL, json=request_body, timeout=timeout / 1000)
                return response.json()
            except requests.exceptions.Timeout:
                raise TimeoutRequestException(TIMEOUT_REQUEST)
        else:
            return {"error": "Invalid method"}
