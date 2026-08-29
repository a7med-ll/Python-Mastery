# -----------------------------------------------------------------------------
# Request Logging Middleware
# -----------------------------------------------------------------------------

import time

from fastapi import Request

from app.core.logging import logger


# -----------------------------------------------------------------------------
# HTTP Request Logging Middleware
# -----------------------------------------------------------------------------

async def request_logging_middleware(
    request: Request,
    call_next
):
    """
    Middleware responsible for logging incoming requests
    and response execution details.
    """


    # -------------------------------------------------------------------------
    # Capture Request Information
    # -------------------------------------------------------------------------

    start_time = time.perf_counter()

    request_method = request.method

    request_path = request.url.path

    client_ip = request.client.host if request.client else "unknown"



    # -------------------------------------------------------------------------
    # Log Incoming Request
    # -------------------------------------------------------------------------

    logger.info(
        f"Incoming request: "
        f"method={request_method}, "
        f"path={request_path}, "
        f"client={client_ip}"
    )


    # -------------------------------------------------------------------------
    # Process Request
    # -------------------------------------------------------------------------

    response = await call_next(request)



    # -------------------------------------------------------------------------
    # Calculate Request Duration
    # -------------------------------------------------------------------------

    duration_ms = (
        time.perf_counter() - start_time
    ) * 1000



    # -------------------------------------------------------------------------
    # Log Response Information
    # -------------------------------------------------------------------------

    logger.info(
        f"Request completed: "
        f"method={request_method}, "
        f"path={request_path}, "
        f"status={response.status_code}, "
        f"duration={duration_ms:.2f}ms"
    )


    return response