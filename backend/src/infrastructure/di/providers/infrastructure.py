import redis
from dishka import Provider, Scope, provide
from sqlalchemy.orm import sessionmaker

from src.config import Settings
from src.infrastructure.cache.redis.activation_code_storage import (
    RedisActivationCodeStorage,
)
from src.infrastructure.database.sqlalchemy.unit_of_work import SQLAlchemyUnitOfWork
from src.shared.application.uow import UnitOfWork
from src.shared.ports.activation_code_storage import ActivationCodeStorage
from src.shared.utils.activation_codes.activation_code_generator import (
    ActivationCodeGenerator,
    RandomActivationCodeGenerator,
)
from src.shared.utils.auth.password_manager import (
    Argon2PasswordManager,
    PasswordManager,
)
from src.shared.utils.auth.token_manager import JWTManager, TokenManager
from src.shared.utils.generators.uuid_generator import (
    DefaultUUIDGenerator,
    UUIDGenerator,
)
from src.shared.utils.notifications.notificator import EmailNotificator, Notificator


class InfrastructureProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_uow(self, session_factory: sessionmaker) -> UnitOfWork:
        return SQLAlchemyUnitOfWork(session_factory)

    @provide(scope=Scope.APP)
    def get_password_manager(self) -> PasswordManager:
        return Argon2PasswordManager()

    @provide(scope=Scope.APP)
    def get_token_manager(self, settings: Settings) -> TokenManager:
        return JWTManager(settings=settings)

    @provide(scope=Scope.APP)
    def get_uuid_generator(self) -> UUIDGenerator:
        return DefaultUUIDGenerator()

    @provide(scope=Scope.APP)
    def get_activation_code_generator(self) -> ActivationCodeGenerator:
        return RandomActivationCodeGenerator()

    @provide(scope=Scope.APP)
    def get_redis_client(self, settings: Settings) -> redis.Redis:
        return redis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=settings.redis_activation_codes_db,
        )

    @provide(scope=Scope.APP)
    def get_activation_code_storage(
        self, redis_client: redis.Redis
    ) -> ActivationCodeStorage:
        return RedisActivationCodeStorage(redis_client=redis_client)

    @provide(scope=Scope.APP)
    def get_notificator(self, settings: Settings) -> Notificator:
        return EmailNotificator(settings=settings)
