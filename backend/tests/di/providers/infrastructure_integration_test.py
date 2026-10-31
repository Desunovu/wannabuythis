from dishka import Provider, Scope, provide
from fakeredis import FakeRedis

from src.config import Settings
from src.infrastructure.cache.redis.activation_code_storage import (
    RedisActivationCodeStorage,
)
from src.shared.ports.activation_code_storage import ActivationCodeStorage
from src.shared.utils.notifications.notificator import FakeNotificator, Notificator


class IntegrationTestInfrastructureProvider(Provider):
    @provide(scope=Scope.APP)
    def get_activation_code_storage(self, settings: Settings) -> ActivationCodeStorage:
        return RedisActivationCodeStorage(
            redis_client=FakeRedis(),
            activation_code_lifetime=settings.activation_code_lifetime,
        )

    @provide(scope=Scope.APP)
    def get_notificator(self) -> Notificator:
        return FakeNotificator()
