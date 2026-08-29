# -----------------------------------------------------------------------------
# Authentication Schemas
# -----------------------------------------------------------------------------

from pydantic import BaseModel, EmailStr, Field

# -----------------------------------------------------------------------------
# User Registration Request
# -----------------------------------------------------------------------------

class UserRegister(BaseModel):
    """
    Schema for user registration.
    """

    email: EmailStr

    password: str = Field(min_length=8, max_length=128)


# -----------------------------------------------------------------------------
# User Login Request
# -----------------------------------------------------------------------------

class UserLogin(BaseModel):
    """
    Schema for user login.
    """

    email: EmailStr

    password: str = Field(min_length=1, max_length=128)


# -----------------------------------------------------------------------------
# Token Response
# -----------------------------------------------------------------------------

class TokenResponse(BaseModel):
    """
    JWT token response.
    """

    access_token: str

    token_type: str
