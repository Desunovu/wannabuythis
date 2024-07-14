import redis

from src import config


class RedisActivationCodeStorage:
    def __init__(self, redis_client: redis.Redis = None):
        if redis_client:
            self.redis_client = redis_client
        else:
            self.redis_client = redis.Redis(
                host=config.REDIS_HOST,
                port=config.REDIS_PORT,
                db=config.REDIS_ACTIVATION_CODES_DB,
            )

    def get_activation_code(self, username: str) -> str:
        return self.redis_client.get(username)

    def save_activation_code(self, username: str, code: str) -> None:
        self.redis_client.set(username, code)
