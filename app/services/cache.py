import json
from typing import Any, Optional


class Cache:
    def __init__(self, redis_client: Any, ttl_seconds: int) -> None:
        self._redis = redis_client
        self._ttl = ttl_seconds
        self._local: dict[str, str] = {}

    def get(self, key: str) -> Optional[Any]:
        if self._redis is None:
            value = self._local.get(key)
        else:
            value = self._redis.get(key)
        if value is None:
            return None
        if isinstance(value, bytes):
            value = value.decode("utf-8")
        return json.loads(value)

    def set(self, key: str, value: Any) -> None:
        payload = json.dumps(value, ensure_ascii=False)
        if self._redis is None:
            self._local[key] = payload
        else:
            self._redis.setex(key, self._ttl, payload)