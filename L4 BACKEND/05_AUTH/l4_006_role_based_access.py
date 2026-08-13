from fastapi import Depends, FastAPI, HTTPException, status

from l4_006_protected_routes import l4_006GetCurrentUser

# -----------------------------------------------------------------------------
# Create FastAPI Application
# -----------------------------------------------------------------------------

app = FastAPI()

# -----------------------------------------------------------------------------
# Require Admin Role
# -----------------------------------------------------------------------------

def l4_006RequireAdmin(
    current_user: dict = Depends(l4_006GetCurrentUser)
) -> dict:
    """Allow only users with the admin role."""

    # Get role from JWT payload.
    role = current_user.get("role")

    # Check user role.
    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required."
        )

    # Return authenticated admin.
    return current_user

# -----------------------------------------------------------------------------
# User Route
# -----------------------------------------------------------------------------

@app.get("/dashboard")
def l4_006UserDashboard(
    current_user: dict = Depends(l4_006GetCurrentUser)
) -> dict:
    """Allow any authenticated user."""

    return {
        "message": "Dashboard accessed successfully.",
        "user_id": current_user["sub"],
        "role": current_user["role"]
    }

# -----------------------------------------------------------------------------
# Admin Route
# -----------------------------------------------------------------------------

@app.get("/admin")
def l4_006AdminRoute(
    current_user: dict = Depends(l4_006RequireAdmin)
) -> dict:
    """Allow only admin users."""

    return {
        "message": "Admin route accessed successfully.",
        "user_id": current_user["sub"],
        "role": current_user["role"]
    }