from typing import Protocol

from src.shared.ports.activation_code_storage import ActivationCodeStorage


class RedisClient(Protocol):
    def get(self, key: str) -> bytes | None: ...

    def set(self, key: str, value: str) -> None: ...


class RedisActivationCodeStorage(ActivationCodeStorage):
    """Хранилище активационных кодов поверх redis-клиента.

    Redis-клиент инжектируется извне (реальный ``redis.Redis`` или
    ``fakeredis.FakeRedis``), поэтому класс не зависит от окружения.
    """

    def __init__(self, redis_client: RedisClient):
        self.redis_client = redis_client

    def get_activation_code(self, username: str) -> str | None:
        code = self.redis_client.get(username)
        return code.decode() if code else None

    def save_activation_code(self, username: str, code: str) -> None:
        self.redis_client.set(username, code)
