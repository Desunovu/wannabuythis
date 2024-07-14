import pytest


@pytest.fixture
def redis_client():
    import fakeredis

    redis_client = fakeredis.FakeRedis()
    return redis_client


@pytest.fixture
def redis_activation_code_storage(redis_client):
    from src.integration.adapters.redis.activation_code_storage import (
        RedisActivationCodeStorage,
    )

    return RedisActivationCodeStorage(redis_client)
