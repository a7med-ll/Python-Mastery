from datetime import datetime, timedelta, timezone

import jwt

# -----------------------------------------------------------------------------
# JWT Configuration
# -----------------------------------------------------------------------------

SECRET_KEY = 'l4-006-learning-secret-key-123456789'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# -----------------------------------------------------------------------------
# Create Access Token
# -----------------------------------------------------------------------------

def l4_006CreateAccessToken(
        user_id: int,
        role: str
) -> str:
    """Create a signed JWT access token."""

    # Create token expiry time.
    expire_time = (                     # --> means the token should stop working extended 30mins after current time
        datetime.now(timezone.utc)
        + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    # Create token payload
    payload = {
        "sub": str(user_id),      # --> token belongs to user 1
        "role": role,             # --> user is admin
        "exp": expire_time,       # --> token expiry time
    }

    # Encode and sign JWT.
    token = jwt.encode(           # --> this encodes everything and creates the token
        payload,                  # --> payload +
        SECRET_KEY,               # --> secret_key +
        algorithm=ALGORITHM,      # --> algorithm
    )

    return token   # --> and then this returns the token that was created by the encode and sign gwt

# -----------------------------------------------------------------------------
# Decode Access Token
# -----------------------------------------------------------------------------

def l4_006DecodeAccessToken(
        token: str,
) -> dict | None:
    """Decode and verify a JWT access token."""

    try:

        # Decode token and verify signature.
        payload = jwt.decode(                  # --> Decodes the token and also verifies
            token,
            SECRET_KEY,                        # --> Verifies Is the signature valid?
            algorithms=[ALGORITHM],            # --> Was it signed using the expected algorithm?
        )

        return payload    

    except jwt.ExpiredSignatureError:

        print("Token expired.")
        return None

    except jwt.InvalidTokenError:

        print("Token invalid.")
        return None

# -----------------------------------------------------------------------------
# Run JWT Example
# -----------------------------------------------------------------------------

def run_l4_006JwtTokens() -> None:
    """Run JWT creation and verification example."""

    # Create token
    token = l4_006CreateAccessToken(
        user_id=1,
        role='admin'
    )

    # Print token
    print("Access Token: ")
    print(token)

    # Decode token
    payload = l4_006DecodeAccessToken(token)

    # print decoded payload
    print("Decoded Payload: ")
    print(payload)

# -----------------------------------------------------------------------------
# Program Entry Point
# -----------------------------------------------------------------------------

if __name__ == '__main__':
    run_l4_006JwtTokens()