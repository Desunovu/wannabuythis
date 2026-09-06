from dishka import Provider, Scope, provide
from fakeredis import FakeRedis

from src.infrastructure.cache.redis.activation_code_storage import (
    RedisActivationCodeStorage,
)
from src.shared.ports.activation_code_storage import ActivationCodeStorage
from src.shared.utils.notifications.notificator import FakeNotificator, Notificator


class DevelopmentInfrastructureProvider(Provider):
    @provide(scope=Scope.APP)
    def get_activation_code_storage(self) -> ActivationCodeStorage:
        return RedisActivationCodeStorage(redis_client=FakeRedis())

    @provide(scope=Scope.APP)
    def get_notificator(self) -> Notificator:
        return FakeNotificator()
