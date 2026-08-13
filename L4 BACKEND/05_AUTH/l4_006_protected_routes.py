from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from l4_006_jwt_tokens import l4_006DecodeAccessToken

# -----------------------------------------------------------------------------
# Create FastAPI Application
# -----------------------------------------------------------------------------

app = FastAPI()

# -----------------------------------------------------------------------------
# Create Bearer Authentication Scheme
# -----------------------------------------------------------------------------

security = HTTPBearer()

# -----------------------------------------------------------------------------
# Get Current User
# -----------------------------------------------------------------------------

def l4_006GetCurrentUser(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """Verify JWT and return current user payload."""

    # Get token from Authorization header.
    token = credentials.credentials

    # Decode and verify token.
    payload = l4_006DecodeAccessToken(
        token
    )

    # Reject invalid or expired token.
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token."
        )

    return payload

# -----------------------------------------------------------------------------
# Public Route
# -----------------------------------------------------------------------------

@app.get("/public")
def l4_006PublicRoute() -> dict:
    """Public route that requires no authentication."""

    return {
        "message": "Anyone can access this route."
    }

# -----------------------------------------------------------------------------
# Protected Route
# -----------------------------------------------------------------------------

@app.get("/profile")
def l4_006ProtectedProfile(
    current_user: dict = Depends(l4_006GetCurrentUser)
) -> dict:
    """Protected route that requires a valid JWT."""

    return {
        "message": "Protected route accessed successfully.",
        "user_id": current_user["sub"],
        "role": current_user["role"]
    }