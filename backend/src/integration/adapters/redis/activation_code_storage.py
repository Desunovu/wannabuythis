import redis

from src import config
from src.common.adapters.activation_code_storage import ActivationCodeStorage


class RedisActivationCodeStorage(ActivationCodeStorage):
    def __init__(self, redis_client: redis.Redis = None):
        if redis_client:
            self.redis_client = redis_client
        else:
            self.redis_client = redis.Redis(
                host=config.REDIS_HOST,
                port=config.REDIS_PORT,
                db=config.REDIS_ACTIVATION_CODES_DB,
            )

    def get_activation_code(self, username: str) -> None | str:
        code = self.redis_client.get(username)
        if code is None:
            return None
        return code.decode()

    def save_activation_code(self, username: str, code: str) -> None:
        self.redis_client.set(username, code)
