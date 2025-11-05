import redis

from src.config import settings
from src.shared.ports.activation_code_storage import ActivationCodeStorage


class RedisActivationCodeStorage(ActivationCodeStorage):
    def __init__(self, redis_client: redis.Redis = None):
        if redis_client:
            self.redis_client = redis_client
        else:
            self.redis_client = redis.Redis(
                host=settings.redis_host,
                port=settings.redis_port,
                db=settings.redis_activation_codes_db,
            )

    def get_activation_code(self, username: str) -> None | str:
        code = self.redis_client.get(username)
        if code is None:
            return None
        return code.decode()

    def save_activation_code(self, username: str, code: str) -> None:
        self.redis_client.set(username, code)
