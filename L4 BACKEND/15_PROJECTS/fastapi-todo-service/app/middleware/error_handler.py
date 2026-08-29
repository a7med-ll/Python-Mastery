# -----------------------------------------------------------------------------
# Global Error Handler Middleware
# -----------------------------------------------------------------------------

from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.logging import logger


# -----------------------------------------------------------------------------
# Global Exception Handler
# -----------------------------------------------------------------------------

async def global_exception_handler(
        request: Request,
        exc: Exception
):
    """
    Handle unexpected application exceptions globally.
    """


    logger.error(
        f"Unhandled exception: "
        f"method={request.method}, "
        f"path={request.url.path}, "
        f"error={str(exc)}"
    )


    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
            "error_code": "INTERNAL_SERVER_ERROR",
            "details": None
        }
    )