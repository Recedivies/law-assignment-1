from datetime import timedelta
from typing import Any

from django.conf import settings
from django.core.cache import cache

from commons.patterns.runnable import Runnable
from plugins.constants import CONFIG_TYPE

logger = settings.LOGGER_INSTANCE


class CacheService(Runnable):
    @classmethod
    def run(cls, cache_key: str) -> Any:
        cached_data = cache.get(cache_key)
        if cached_data is not None:  # Cache hit
            ttl = cache.ttl(cache_key)

            if ttl > 0:  # Check if the cache is still valid
                logger.info("Cache Hit")
                return cached_data
            logger.info("Cache expired")
        else:  # Cache miss
            logger.info("Cache Miss")

        return None

    @classmethod
    def set_cache(cls, key: str, value: Any, config: CONFIG_TYPE) -> None:
        cache_expiry = timedelta(seconds=config.get("cache_ttl", 0))
        cache.set(key=key, value=value, timeout=cache_expiry.total_seconds())
