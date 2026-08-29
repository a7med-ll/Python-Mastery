# -----------------------------------------------------------------------------
# Security Utilities
# -----------------------------------------------------------------------------

from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings


# -----------------------------------------------------------------------------
# Password Hashing Configuration
# -----------------------------------------------------------------------------

password_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)


# -----------------------------------------------------------------------------
# Hash Password
# -----------------------------------------------------------------------------

def hash_password(
        password: str
) -> str:
    """
    Hash plain password.
    """

    return password_context.hash(
        password
    )


# -----------------------------------------------------------------------------
# Verify Password
# -----------------------------------------------------------------------------

def verify_password(
        plain_password: str,
        hashed_password: str
) -> bool:
    """
    Verify password.
    """

    return password_context.verify(
        plain_password,
        hashed_password
    )


# -----------------------------------------------------------------------------
# Create JWT Access Token
# -----------------------------------------------------------------------------

def create_access_token(
        data: dict,
        expires_minutes: int | None = None
) -> str:
    """
    Create JWT access token.
    """

    token_data = data.copy()


    token_expire_minutes = (
        expires_minutes
        if expires_minutes is not None
        else settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )

    expire_time = (
        datetime.now(timezone.utc)
        +
        timedelta(
            minutes=token_expire_minutes
        )
    )


    token_data.update(
        {
            "exp": expire_time,
            "iat": datetime.now(timezone.utc),
            "type": "access"
        }
    )


    return jwt.encode(
        token_data,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )


# -----------------------------------------------------------------------------
# Decode JWT Access Token
# -----------------------------------------------------------------------------

def decode_access_token(
        token: str
) -> dict | None:
    """
    Decode and validate JWT token.
    """

    try:

        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[
                settings.JWT_ALGORITHM
            ]
        )


        if payload.get("type") != "access":
            return None


        return payload


    except JWTError:

        return None
