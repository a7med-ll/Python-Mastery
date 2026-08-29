# -----------------------------------------------------------------------------
#
# API Response Schemas
#
# -----------------------------------------------------------------------------

from typing import Generic, TypeVar

from pydantic import BaseModel


# -----------------------------------------------------------------------------
#
# Generic Type
#
# -----------------------------------------------------------------------------

T = TypeVar("T")


# -----------------------------------------------------------------------------
#
# Standard API Response
#
# -----------------------------------------------------------------------------

class ResponseSchema(
    BaseModel,
    Generic[T]
):
    """
    Common successful API response structure.
    """

    success: bool

    message: str

    data: T | None = None


# -----------------------------------------------------------------------------
#
# Error Response Schema
#
# -----------------------------------------------------------------------------

class ErrorResponseSchema(BaseModel):
    """
    Common error API response structure.
    """

    success: bool = False

    message: str

    error_code: str | None = None

    details: dict | list | None = None