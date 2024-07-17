import fakeredis
import pytest

from src.integration.adapters.redis.activation_code_storage import (
    RedisActivationCodeStorage,
)


@pytest.fixture(scope="session")
def redis_client() -> fakeredis.FakeRedis:
    """Create a FakeRedis client for testing."""
    return fakeredis.FakeRedis()


@pytest.fixture
def redis_activation_code_storage(
    redis_client: fakeredis.FakeRedis,
) -> RedisActivationCodeStorage:
    """Create a RedisActivationCodeStorage instance using the FakeRedis client."""
    return RedisActivationCodeStorage(redis_client)
