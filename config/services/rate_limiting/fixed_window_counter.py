import time
from typing import Any

from django_redis import get_redis_connection

from commons.exceptions import RateLimitedException
from commons.patterns.runnable import Runnable
from config.constants import RATE_LIMIT_EXCEEDED
from plugins.constants import CONFIG_TYPE


class FixedWindowCounterService(Runnable):
    @classmethod
    def run(cls, config: CONFIG_TYPE, cache_key: str) -> Any:
        redis_connection = get_redis_connection()
        second = config.get("second")

        current_window = str(int(time.time()) // second)
        cache_key = cache_key + ":" + current_window

        value = redis_connection.get(cache_key)
        request_count = int(value) if value else 0

        if request_count >= second:
            raise RateLimitedException(RATE_LIMIT_EXCEEDED)

        lua_script = """
        local cache_key = KEYS[1]
        local second = tonumber(ARGV[1])

        local value = redis.call('GET', cache_key)

        if value then
            redis.call('INCR', cache_key)
        else
            local cache_expiry = tonumber(second)
            redis.call('SET', cache_key, 1, 'EX', cache_expiry)
        end
        """
        redis_connection.eval(lua_script, 1, cache_key, second)
