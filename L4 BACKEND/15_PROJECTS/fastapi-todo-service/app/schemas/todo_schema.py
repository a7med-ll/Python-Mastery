# -----------------------------------------------------------------------------
# Todo Schemas
# -----------------------------------------------------------------------------

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.pagination_schema import PaginationMeta


# -----------------------------------------------------------------------------
# Create Todo Request
# -----------------------------------------------------------------------------

class TodoCreate(BaseModel):
    """Schema for creating todo."""

    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)


# -----------------------------------------------------------------------------
# Update Todo Request
# -----------------------------------------------------------------------------

class TodoUpdate(BaseModel):
    """Schema for updating todo."""

    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    completed: bool | None = None


# -----------------------------------------------------------------------------
# Todo Response
# -----------------------------------------------------------------------------

class TodoResponse(BaseModel):
    """Schema returned to API clients."""

    id: int
    title: str
    description: str | None
    completed: bool
    owner_id: int
    created_at: datetime


    model_config = ConfigDict(
        from_attributes=True
    )

# -----------------------------------------------------------------------------
# Todo Pagination Response
# -----------------------------------------------------------------------------

class TodoPaginationResponse(BaseModel):
    """
    Paginated todo response.
    """

    items: list[TodoResponse]

    pagination: PaginationMeta
