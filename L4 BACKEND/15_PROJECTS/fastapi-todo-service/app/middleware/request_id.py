# -----------------------------------------------------------------------------
# Request ID Middleware
# -----------------------------------------------------------------------------

import uuid

from starlette.middleware.base import BaseHTTPMiddleware

from fastapi import Request


# -----------------------------------------------------------------------------
# Request ID Middleware Class
# -----------------------------------------------------------------------------

class RequestIDMiddleware(BaseHTTPMiddleware):

    """
    Middleware that adds unique request ID
    for request tracing.
    """


    async def dispatch(
            self,
            request: Request,
            call_next
    ):

        # ---------------------------------------------------------------------
        # Generate Request ID
        # ---------------------------------------------------------------------

        request_id = str(
            uuid.uuid4()
        )


        # ---------------------------------------------------------------------
        # Attach Request ID
        # ---------------------------------------------------------------------

        request.state.request_id = request_id


        # ---------------------------------------------------------------------
        # Process Request
        # ---------------------------------------------------------------------

        response = await call_next(
            request
        )


        # ---------------------------------------------------------------------
        # Add Response Header
        # ---------------------------------------------------------------------

        response.headers["X-Request-ID"] = request_id


        return response