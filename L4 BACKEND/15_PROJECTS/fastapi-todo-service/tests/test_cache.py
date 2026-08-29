# -----------------------------------------------------------------------------
# Redis Cache Tests
# -----------------------------------------------------------------------------

from app.cache.redis import redis_client
from app.core.config import settings


# -----------------------------------------------------------------------------
# Test Redis Connection
# -----------------------------------------------------------------------------

def test_redis_connection():

    result = redis_client.ping()

    assert result is True


# -----------------------------------------------------------------------------
# Test Redis Set And Get
# -----------------------------------------------------------------------------

def test_redis_set_get():

    key = "test:user"

    value = {
        "id": 1,
        "email": "cache@test.com"
    }

    # Store data
    redis_client.set(
        key,
        value
    )

    # Retrieve data
    cached_value = redis_client.get(
        key
    )

    assert cached_value == value


# -----------------------------------------------------------------------------
# Test Redis Delete
# -----------------------------------------------------------------------------

def test_redis_delete():

    key = "test:delete"

    redis_client.set(
        key,
        {
            "value": "temporary"
        }
    )

    redis_client.delete(
        key
    )

    result = redis_client.get(
        key
    )

    assert result is None

# -----------------------------------------------------------------------------
# Test Cache Invalidation
# -----------------------------------------------------------------------------

def test_cache_delete():

    key = "user:99"

    redis_client.set(
        key,
        {
            "id": 99,
            "email": "old@test.com"
        }
    )


    redis_client.delete(
        key
    )


    assert redis_client.get(key) is None


def test_cache_can_be_disabled_without_crashing():

    settings.REDIS_ENABLED = False

    try:

        redis_client.set("disabled:key", {"value": True})

        assert redis_client.get("disabled:key") is None

        assert redis_client.ping() is False

    finally:

        settings.REDIS_ENABLED = True
