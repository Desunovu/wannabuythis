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


@pytest.fixture
def integration_test_container():
    start_sqlalchemy_mappers()
    container = create_integration_test_container()
    with container() as request_container:
        yield request_container
    container.close()
    clear_mappers()


@pytest.fixture
def sqlite_session(integration_test_container) -> Session:
    return integration_test_container.get(Session)


@pytest.fixture
def sqlalchemy_uow(integration_test_container) -> UnitOfWork:
    return integration_test_container.get(UnitOfWork)


@pytest.fixture
def prepare_mappers():
    start_sqlalchemy_mappers()
    yield
    clear_mappers()


@pytest.fixture
def redis_activation_code_storage() -> RedisActivationCodeStorage:
    return RedisActivationCodeStorage(redis_client=FakeRedis())
