# -----------------------------------------------------------------------------
# Cache Service
# -----------------------------------------------------------------------------

from app.cache.redis import redis_client


# -----------------------------------------------------------------------------
# Cache Service Class
# -----------------------------------------------------------------------------

class CacheService:
    """Service responsible for cache operations."""


    # -------------------------------------------------------------------------
    # Get Cached Data
    # -------------------------------------------------------------------------

    def get(
            self,
            key: str
    ):
        """
        Retrieve data from cache.
        """

        return redis_client.get(
            key
        )


    # -------------------------------------------------------------------------
    # Store Data In Cache
    # -------------------------------------------------------------------------

    def set(
            self,
            key: str,
            value: object,
            expire_seconds: int = 300
    ) -> None:
        """
        Store data in cache.
        """

        redis_client.set(
            key,
            value,
            expire_seconds
        )


    # -------------------------------------------------------------------------
    # Delete Cached Data
    # -------------------------------------------------------------------------

    def delete(
            self,
            key: str
    ) -> None:
        """
        Remove data from cache.
        """

        redis_client.delete(
            key
        )


    # -------------------------------------------------------------------------
    # Delete Cache By Pattern
    # -------------------------------------------------------------------------

    def delete_pattern(
            self,
            pattern: str
    ) -> None:
        """
        Remove multiple cache keys using pattern matching.
        """

        keys = redis_client.keys(
            pattern
        )

        for key in keys:
            redis_client.delete(
                key
            )


# -----------------------------------------------------------------------------
# Cache Service Instance
# -----------------------------------------------------------------------------

cache_service = CacheService()