from fastapi import Depends, FastAPI, HTTPException, status

# -----------------------------------------------------------------------------
# Create FastAPI Application
# -----------------------------------------------------------------------------

app = FastAPI()

# -----------------------------------------------------------------------------
# Get Current User Role
# -----------------------------------------------------------------------------

def l4_003GetUserRole() -> str:
    """Return the current user role."""

    return "customer"


# -----------------------------------------------------------------------------
# Require Admin Role
# -----------------------------------------------------------------------------

def l4_003RequireAdmin(
    role: str = Depends(l4_003GetUserRole)
) -> str:
    """Allow access only for admin users."""

    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return role


# -----------------------------------------------------------------------------
# Protected Profile Route
# -----------------------------------------------------------------------------

@app.get("/profile")
def l4_003ProfileRoute(
    role: str = Depends(l4_003RequireAdmin)
) -> dict:
    """Return protected profile information."""

    return {
        "message": "Profile accessed",
        "role": role
    }