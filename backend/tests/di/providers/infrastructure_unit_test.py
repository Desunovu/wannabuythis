from dishka import Provider, Scope, provide

from src.shared.application.fakes import FakeUnitOfWork
from src.shared.application.uow import UnitOfWork
from src.shared.ports.activation_code_storage import (
    ActivationCodeStorage,
    FakeActivationCodeStorage,
)
from src.shared.utils.notifications.notificator import FakeNotificator, Notificator


class UnitTestInfrastructureProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_uow(self) -> UnitOfWork:
        return FakeUnitOfWork()

    @provide(scope=Scope.APP)
    def get_activation_code_storage(self) -> ActivationCodeStorage:
        return FakeActivationCodeStorage()

    @provide(scope=Scope.APP)
    def get_notificator(self) -> Notificator:
        return FakeNotificator()
