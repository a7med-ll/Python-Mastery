# -----------------------------------------------------------------------------
# Validation Exception Handler
# -----------------------------------------------------------------------------

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


# -----------------------------------------------------------------------------
# Handle Request Validation Errors
# -----------------------------------------------------------------------------

async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    """
    Handle invalid request payloads.
    """

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation error",
            "error_code": "VALIDATION_ERROR",
            "details": exc.errors()
        }
    )