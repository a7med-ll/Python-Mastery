# -----------------------------------------------------------------------------
# Redis Client
# -----------------------------------------------------------------------------

import json

import redis
from redis.exceptions import RedisError

from app.core.config import settings


# -----------------------------------------------------------------------------
# Redis Client Class
# -----------------------------------------------------------------------------

class RedisClient:

    """
    Redis connection wrapper.
    """


    # -------------------------------------------------------------------------
    # Constructor
    # -------------------------------------------------------------------------

    def __init__(self):

        self.client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True
        )


    # -------------------------------------------------------------------------
    # Ping Redis
    # -------------------------------------------------------------------------

    def ping(self) -> bool:
        """
        Check Redis connection.
        """

        if not settings.REDIS_ENABLED:
            return False

        try:
            return self.client.ping()

        except RedisError:
            return False



    # -------------------------------------------------------------------------
    # Get Data
    # -------------------------------------------------------------------------

    def get(
            self,
            key: str
    ):
        """
        Retrieve data from Redis.
        """

        if not settings.REDIS_ENABLED:
            return None

        try:
            value = self.client.get(
                key
            )

        except RedisError:
            return None


        if value is None:
            return None


        return json.loads(
            value
        )



    # -------------------------------------------------------------------------
    # Set Data
    # -------------------------------------------------------------------------

    def set(
            self,
            key: str,
            value,
            expire_seconds: int = 300
    ) -> None:
        """
        Store data in Redis.
        """


        if not settings.REDIS_ENABLED:
            return

        try:
            self.client.set(
                key,
                json.dumps(value),
                ex=expire_seconds
            )

        except RedisError:
            return



    # -------------------------------------------------------------------------
    # Delete Data
    # -------------------------------------------------------------------------

    def delete(
            self,
            key: str
    ) -> None:
        """
        Delete Redis key.
        """

        if not settings.REDIS_ENABLED:
            return

        try:
            self.client.delete(
                key
            )

        except RedisError:
            return

    # -------------------------------------------------------------------------
    # Get Keys By Pattern
    # -------------------------------------------------------------------------

    def keys(
            self,
            pattern: str
    ):
        """
        Retrieve Redis keys matching pattern.
        """

        if not settings.REDIS_ENABLED:
            return []

        try:
            return list(
                self.client.scan_iter(
                    match=pattern
                )
            )

        except RedisError:
            return []

    # -------------------------------------------------------------------------
    # Delete Pattern
    # -------------------------------------------------------------------------

    def delete_pattern(
            self,
            pattern: str
    ) -> None:
        """
        Delete keys matching pattern.
        """


        keys = list(
            self.keys(pattern)
        )


        if keys:

            self.client.delete(
                *keys
            )


# -----------------------------------------------------------------------------
# Redis Instance
# -----------------------------------------------------------------------------

redis_client = RedisClient()
