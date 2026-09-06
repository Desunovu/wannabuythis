import pytest
from fakeredis import FakeRedis
from sqlalchemy.orm import Session, clear_mappers

from src.infrastructure.cache.redis.activation_code_storage import (
    RedisActivationCodeStorage,
)
from src.infrastructure.database.sqlalchemy.orm import (
    start_sqlalchemy_mappers,
)
from src.shared.application.uow import UnitOfWork
from tests.di.container import create_integration_test_container


# ---------------------------------------------------------------------------
# Dishka integration-test container fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def integration_test_container():
    """Entered (request-scoped) dishka container with SQLite + FakeRedis."""
    start_sqlalchemy_mappers()
    container = create_integration_test_container()
    with container() as request_container:
        yield request_container
    container.close()
    clear_mappers()


@pytest.fixture
def sqlite_session(integration_test_container) -> Session:
    """SQLite Session из тестового контейнера (изоляция через свежий container)."""
    return integration_test_container.get(Session)


@pytest.fixture
def sqlalchemy_uow(integration_test_container) -> UnitOfWork:
    """SQLAlchemyUnitOfWork из тестового контейнера — для тестов UoW."""
    return integration_test_container.get(UnitOfWork)


@pytest.fixture
def prepare_mappers():
    """Регистрирует ORM-маппинги для тестов, не использующих контейнер."""
    start_sqlalchemy_mappers()
    yield
    clear_mappers()


# ---------------------------------------------------------------------------
# Redis / FakeRedis fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def redis_activation_code_storage() -> RedisActivationCodeStorage:
    """
    Использует RedisActivationCodeStorage поверх FakeRedis (in-memory).
    """
    return RedisActivationCodeStorage(redis_client=FakeRedis())