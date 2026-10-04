from datetime import timedelta
from typing import Protocol

from src.shared.ports.activation_code_storage import ActivationCodeStorage


class RedisClient(Protocol):
    def get(self, key: str) -> bytes | None: ...

    def set(self, key: str, value: str, ex: int | None = None) -> None: ...

    def delete(self, key: str) -> int: ...


class RedisActivationCodeStorage(ActivationCodeStorage):
    """Activation code storage with an injected Redis or FakeRedis client."""

    def __init__(self, redis_client: RedisClient, activation_code_lifetime: timedelta):
        self.redis_client = redis_client
        self._activation_code_ttl = int(activation_code_lifetime.total_seconds())

    def get_activation_code(self, username: str) -> str | None:
        code = self.redis_client.get(username)
        return code.decode() if code else None

    def save_activation_code(self, username: str, code: str) -> None:
        self.redis_client.set(username, code, ex=self._activation_code_ttl)

    def delete_activation_code(self, username: str) -> None:
        self.redis_client.delete(username)
