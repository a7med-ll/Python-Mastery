from datetime import datetime, timedelta, timezone

import jwt

from l4_006_jwt_tokens import (
    ALGORITHM,
    SECRET_KEY,
    l4_006CreateAccessToken,
)

# -----------------------------------------------------------------------------
# Refresh Token Configuration
# -----------------------------------------------------------------------------

REFRESH_TOKEN_EXPIRE_DAYS = 7

# -----------------------------------------------------------------------------
# Create Refresh Token
# -----------------------------------------------------------------------------

def l4_006CreateRefreshToken(
    user_id: int,
    role: str
) -> str:
    """Create a signed JWT refresh token."""

    # Create refresh token expiry time.
    expire_time = (
        datetime.now(timezone.utc)
        + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )

    # Create refresh token payload.
    payload = {
        "sub": str(user_id),
        "role": role,
        "type": "refresh",
        "exp": expire_time
    }

    # Encode and sign refresh token.
    refresh_token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return refresh_token

# -----------------------------------------------------------------------------
# Create New Access Token
# -----------------------------------------------------------------------------

def l4_006RefreshAccessToken(
    refresh_token: str
) -> str | None:
    """Create a new access token using a valid refresh token."""

    try:

        # Decode and verify refresh token.
        payload = jwt.decode(
            refresh_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        # Check that token is a refresh token.
        if payload.get("type") != "refresh":
            print("Invalid refresh token.")
            return None

        # Get user information from refresh token.
        user_id = int(payload["sub"])
        role = payload["role"]

        # Create new access token.
        access_token = l4_006CreateAccessToken(
            user_id=user_id,
            role=role
        )

        return access_token

    except jwt.ExpiredSignatureError:

        print("Refresh token expired.")
        return None

    except jwt.InvalidTokenError:

        print("Invalid refresh token.")
        return None

# -----------------------------------------------------------------------------
# Run Refresh Token Example
# -----------------------------------------------------------------------------

def run_l4_006RefreshTokens() -> None:
    """Run refresh token example."""

    # Create refresh token.
    refresh_token = l4_006CreateRefreshToken(
        user_id=1,
        role="admin"
    )

    # Print refresh token.
    print("Refresh Token:")
    print(refresh_token)

    # Create new access token using refresh token.
    new_access_token = l4_006RefreshAccessToken(
        refresh_token
    )

    # Print new access token.
    print("New Access Token:")
    print(new_access_token)

# -----------------------------------------------------------------------------
# Program Entry Point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    run_l4_006RefreshTokens()