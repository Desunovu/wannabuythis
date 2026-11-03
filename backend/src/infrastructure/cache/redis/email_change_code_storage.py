import json
from datetime import timedelta

from src.infrastructure.cache.redis.activation_code_storage import RedisClient
from src.shared.ports.email_change_code_storage import (
    EmailChangeCodeStorage,
    PendingEmailChange,
)


class RedisEmailChangeCodeStorage(EmailChangeCodeStorage):
    """Keep pending email changes with a key prefix."""

    def __init__(self, redis_client: RedisClient, code_lifetime: timedelta):
        self.redis_client = redis_client
        self._code_ttl = int(code_lifetime.total_seconds())

    @staticmethod
    def _key(username: str) -> str:
        return f"email_change:{username}"

    def get(self, username: str) -> PendingEmailChange | None:
        raw_value = self.redis_client.get(self._key(username))
        if raw_value is None:
            return None
        code, new_email = json.loads(raw_value)
        return PendingEmailChange(code=code, new_email=new_email)

    def save(self, username: str, code: str, new_email: str) -> None:
        self.redis_client.set(
            self._key(username),
            json.dumps([code, new_email]),
            ex=self._code_ttl,
        )

    def delete(self, username: str) -> None:
        self.redis_client.delete(self._key(username))
