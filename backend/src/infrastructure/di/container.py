from dishka import make_container
from dishka.container import Container

from src.infrastructure.di.providers.database import DatabaseProvider
from src.infrastructure.di.providers.infrastructure import InfrastructureProvider
from src.infrastructure.di.providers.infrastructure_development import (
    DevelopmentInfrastructureProvider,
)
from src.infrastructure.di.providers.mediator import MediatorProvider
from src.infrastructure.di.providers.settings import SettingsProvider


def create_production_container() -> Container:
    return make_container(
        DatabaseProvider(),
        InfrastructureProvider(),
        MediatorProvider(),
        SettingsProvider(),
    )


def create_development_container() -> Container:
    """Stuff like FakeRedis, FakeNotificator, real DB"""
    return make_container(
        DatabaseProvider(),
        InfrastructureProvider(),
        DevelopmentInfrastructureProvider(),
        MediatorProvider(),
        SettingsProvider(),
    )
