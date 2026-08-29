# -----------------------------------------------------------------------------
# Rate Limit Middleware
# -----------------------------------------------------------------------------

import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.cache.redis import redis_client
from app.core.config import settings


# -----------------------------------------------------------------------------
# Rate Limit Middleware Class
# -----------------------------------------------------------------------------

class RateLimitMiddleware(BaseHTTPMiddleware):

    """
    Redis based API rate limiting.
    """


    # -------------------------------------------------------------------------
    # Constructor
    # -------------------------------------------------------------------------

    def __init__(
            self,
            app,
            requests_limit: int = 60,
            window_seconds: int = 60
    ):

        super().__init__(app)

        self.requests_limit = requests_limit
        self.window_seconds = window_seconds



    # -------------------------------------------------------------------------
    # Dispatch Request
    # -------------------------------------------------------------------------

    async def dispatch(
            self,
            request: Request,
            call_next
    ):

        if not settings.RATE_LIMIT_ENABLED:
            return await call_next(request)

        # ---------------------------------------------------------------------
        # Identify Client
        # ---------------------------------------------------------------------

        client_ip = request.client.host if request.client else "unknown"


        # ---------------------------------------------------------------------
        # Create Redis Key
        # ---------------------------------------------------------------------

        current_window = int(
            time.time() // self.window_seconds
        )


        key = (
            f"rate_limit:"
            f"{client_ip}:"
            f"{current_window}"
        )


        # ---------------------------------------------------------------------
        # Get Current Count
        # ---------------------------------------------------------------------

        current_count = redis_client.get(
            key
        )


        if current_count is None:

            redis_client.set(
                key,
                1,
                expire_seconds=self.window_seconds
            )

        else:

            current_count = int(
                current_count
            )


            if current_count >= self.requests_limit:

                from fastapi.responses import JSONResponse

                return JSONResponse(
                    status_code=429,
                    content={
                        "success": False,
                        "message": "Too many requests"
                    }
                )


            redis_client.set(
                key,
                current_count + 1,
                expire_seconds=self.window_seconds
            )


        # ---------------------------------------------------------------------
        # Continue Request
        # ---------------------------------------------------------------------

        response = await call_next(
            request
        )


        return response
