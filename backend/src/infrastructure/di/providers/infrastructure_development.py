from typing import cast

import redis
from dishka import Provider, Scope, provide
from fakeredis import FakeRedis


class DevelopmentInfrastructureProvider(Provider):
    @provide(scope=Scope.APP)
    def get_redis_client(self) -> redis.Redis:
        return cast(redis.Redis, FakeRedis())
