from dishka import make_container

from src.infrastructure.di.providers.database import DatabaseProvider
from src.infrastructure.di.providers.infrastructure import InfrastructureProvider
from src.infrastructure.di.providers.mediator import MediatorProvider
from src.infrastructure.di.providers.settings import SettingsProvider
from tests.di.providers.database import TestDatabaseProvider
from tests.di.providers.infrastructure_integration_test import (
    IntegrationTestInfrastructureProvider,
)
from tests.di.providers.infrastructure_unit_test import UnitTestInfrastructureProvider


def create_unit_test_container():
    return make_container(
        DatabaseProvider(),
        InfrastructureProvider(),
        UnitTestInfrastructureProvider(),  # Override
        MediatorProvider(),
        SettingsProvider(),
    )


def create_integration_test_container():
    return make_container(
        DatabaseProvider(),
        TestDatabaseProvider(),  # Override
        InfrastructureProvider(),
        IntegrationTestInfrastructureProvider(),  # Override
        MediatorProvider(),
        SettingsProvider(),
    )
