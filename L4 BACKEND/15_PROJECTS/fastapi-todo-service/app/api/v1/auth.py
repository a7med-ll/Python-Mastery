# -----------------------------------------------------------------------------
# Authentication API Routes
# -----------------------------------------------------------------------------

from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session

from app.api.dependencies import get_database_session

from app.schemas.auth_schema import (
    UserRegister,
    UserLogin,
    TokenResponse
)

from app.services.auth_service import AuthService
from app.schemas.response_schema import ResponseSchema



# -----------------------------------------------------------------------------
# Router Configuration
# -----------------------------------------------------------------------------

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# -----------------------------------------------------------------------------
# Register Endpoint
# -----------------------------------------------------------------------------

@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseSchema[dict]
)

def register(request: UserRegister, database: Session = Depends(get_database_session)):
    """Register a new user."""

    auth_service = AuthService(database)

    try:

        user = auth_service.register_user(request.email, request.password)

        return ResponseSchema(
            success=True,
            message="User registered successfully",
            data={
                "id": user.id,
                "email": user.email
            }
        )

    except ValueError as error:

        raise HTTPException(status_code=400, detail=str(error))

# -----------------------------------------------------------------------------
# Login Endpoint
# -----------------------------------------------------------------------------

@router.post(
    "/login",
    response_model=ResponseSchema[dict]
)

def login(
    username: str = Form(...),
    password: str = Form(...),
    database: Session = Depends(get_database_session)
):
    """
    Authenticate user and generate JWT token.
    """

    auth_service = AuthService(database)

    try:

        token = auth_service.login_user(
            username,
            password
        )

        return ResponseSchema(
            success=True,
            message="Login successful",
            data={
                "access_token": token,
                "token_type": "bearer"
            }
        )

    except ValueError as error:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error)
        )
