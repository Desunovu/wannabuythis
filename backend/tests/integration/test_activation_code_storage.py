from datetime import timedelta

from fakeredis import FakeRedis

from src.infrastructure.cache.redis.activation_code_storage import (
    RedisActivationCodeStorage,
)


def _make_storage(ttl: timedelta = timedelta(hours=1)) -> RedisActivationCodeStorage:
    return RedisActivationCodeStorage(
        redis_client=FakeRedis(), activation_code_lifetime=ttl
    )


def test_save_get_delete_cycle():
    storage = _make_storage()
    storage.save_activation_code("alice", "123456")
    assert storage.get_activation_code("alice") == "123456"
    storage.delete_activation_code("alice")
    assert storage.get_activation_code("alice") is None


def test_code_is_stored_with_ttl():
    storage = _make_storage(ttl=timedelta(hours=1))
    storage.save_activation_code("alice", "123456")
    assert 0 < storage.redis_client.ttl("alice") <= 3600


def test_resend_overwrites_previous_code():
    storage = _make_storage()
    storage.save_activation_code("alice", "111111")
    storage.save_activation_code("alice", "222222")
    assert storage.get_activation_code("alice") == "222222"
    assert storage.get_activation_code("alice") != "111111"
