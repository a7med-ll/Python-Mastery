# -----------------------------------------------------------------------------
# Pagination Schemas
# -----------------------------------------------------------------------------

from pydantic import BaseModel


# -----------------------------------------------------------------------------
# Pagination Metadata
# -----------------------------------------------------------------------------

class PaginationMeta(BaseModel):
    """
    Pagination information returned with list responses.
    """

    page: int

    limit: int

    total: int

    pages: int


# -----------------------------------------------------------------------------
# Paginated Response
# -----------------------------------------------------------------------------

class PaginatedResponse(BaseModel):
    """
    Standard paginated data structure.
    """

    items: list

    pagination: PaginationMeta