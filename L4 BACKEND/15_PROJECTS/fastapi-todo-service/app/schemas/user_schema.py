from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


# -----------------------------------------------------------------------------
# User Response
# -----------------------------------------------------------------------------

class UserResponse(BaseModel):
    """Schema returned to API clients."""

    id: int
    email: str
    is_active: bool
    created_at: datetime


    model_config = ConfigDict(
        from_attributes=True
    )


# -----------------------------------------------------------------------------
# User Update Request
# -----------------------------------------------------------------------------

class UserUpdate(BaseModel):
    """Schema for updating user."""

    email: EmailStr
