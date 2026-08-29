# -----------------------------------------------------------------------------
# API Router
# -----------------------------------------------------------------------------

from fastapi import APIRouter

from app.api.v1 import todos
from app.api.v1 import auth
from app.api.v1 import users


# -----------------------------------------------------------------------------
# Main API Router
# -----------------------------------------------------------------------------

api_router = APIRouter()


# -----------------------------------------------------------------------------
# Include Routes
# -----------------------------------------------------------------------------

api_router.include_router(
    todos.router
)


api_router.include_router(
    auth.router
)

api_router.include_router(
    users.router
)