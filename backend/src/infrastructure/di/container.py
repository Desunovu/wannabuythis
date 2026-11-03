from dishka import make_container
from dishka.container import Container

from src.infrastructure.di.providers.database import DatabaseProvider
from src.infrastructure.di.providers.infrastructure import InfrastructureProvider
from src.infrastructure.di.providers.infrastructure_development import (
    DevelopmentInfrastructureProvider,
)
from src.infrastructure.di.providers.mediator import MediatorProvider
from src.infrastructure.di.providers.settings import SettingsProvider
from src.infrastructure.di.providers.users import UsersProvider


def create_production_container() -> Container:
    return make_container(
        DatabaseProvider(),
        InfrastructureProvider(),
        UsersProvider(),
        MediatorProvider(),
        SettingsProvider(),
    )


def create_development_container() -> Container:
    return make_container(
        DatabaseProvider(),
        InfrastructureProvider(),
        DevelopmentInfrastructureProvider(),
        UsersProvider(),
        MediatorProvider(),
        SettingsProvider(),
    )
