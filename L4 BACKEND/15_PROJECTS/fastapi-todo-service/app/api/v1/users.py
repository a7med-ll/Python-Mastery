# -----------------------------------------------------------------------------
# User API Routes
# -----------------------------------------------------------------------------

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.api.dependencies import (
    get_database_session,
    get_current_user
)

from app.core.exceptions import (
    not_found_exception,
    authorization_exception
)

from app.models.user import User

from app.schemas.user_schema import UserResponse, UserUpdate

from app.schemas.response_schema import ResponseSchema

from app.services.user_service import UserService


# -----------------------------------------------------------------------------
# Router Configuration
# -----------------------------------------------------------------------------

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# -----------------------------------------------------------------------------
# Get Current User Profile
# -----------------------------------------------------------------------------

@router.get(
    "/me",
    response_model=ResponseSchema[UserResponse]
)
def get_current_user_profile(
        current_user: User = Depends(get_current_user)
):
    """
    Retrieve logged-in user profile.
    """


    return ResponseSchema(
        success=True,
        message="User retrieved successfully",
        data=UserResponse.model_validate(
            current_user
        )
    )



# -----------------------------------------------------------------------------
# Get User By ID
# -----------------------------------------------------------------------------

@router.get(
    "/{user_id}",
    response_model=ResponseSchema[UserResponse]
)
def get_user(
        user_id: int,
        database: Session = Depends(get_database_session),
        current_user: User = Depends(get_current_user)
):
    """
    Retrieve user by ID.
    """


    # -------------------------------------------------------------------------
    # Initialize User Service
    # -------------------------------------------------------------------------

    service = UserService(
        database
    )


    # -------------------------------------------------------------------------
    # Find User
    # -------------------------------------------------------------------------

    user = service.get_user_by_id(
        user_id
    )


    if not user:

        raise not_found_exception(
            "User not found"
        )


    # -------------------------------------------------------------------------
    # Ownership Validation
    # -------------------------------------------------------------------------

    if user.id != current_user.id:

        raise authorization_exception(
            "Not authorized"
        )


    return ResponseSchema(
        success=True,
        message="User retrieved successfully",
        data=UserResponse.model_validate(
            user
        )
    )



# -----------------------------------------------------------------------------
# Update User
# -----------------------------------------------------------------------------

@router.put(
    "/{user_id}",
    response_model=ResponseSchema[UserResponse]
)
def update_user(
        user_id: int,
        user_data: UserUpdate,
        database: Session = Depends(get_database_session),
        current_user: User = Depends(get_current_user)
):
    """
    Update user profile.
    """


    # -------------------------------------------------------------------------
    # Initialize User Service
    # -------------------------------------------------------------------------

    service = UserService(
        database
    )


    # -------------------------------------------------------------------------
    # Find User
    # -------------------------------------------------------------------------

    user = service.get_user_by_id(
        user_id
    )


    if not user:

        raise not_found_exception(
            "User not found"
        )


    # -------------------------------------------------------------------------
    # Ownership Validation
    # -------------------------------------------------------------------------

    if user.id != current_user.id:

        raise authorization_exception(
            "Not authorized"
        )


    existing_user = service.get_user_by_email(
        str(user_data.email)
    )


    if existing_user and existing_user.id != user.id:

        from app.core.exceptions import bad_request_exception

        raise bad_request_exception(
            "User with this email already exists"
        )


    user.email = str(user_data.email)


    # -------------------------------------------------------------------------
    # Save Update
    # -------------------------------------------------------------------------

    updated_user = service.update_user(
        user
    )


    return ResponseSchema(
        success=True,
        message="User updated successfully",
        data=UserResponse.model_validate(
            updated_user
        )
    )



# -----------------------------------------------------------------------------
# Delete User
# -----------------------------------------------------------------------------

@router.delete(
    "/{user_id}",
    response_model=ResponseSchema[dict]
)
def delete_user(
        user_id: int,
        database: Session = Depends(get_database_session),
        current_user: User = Depends(get_current_user)
):
    """
    Delete user account.
    """


    # -------------------------------------------------------------------------
    # Initialize User Service
    # -------------------------------------------------------------------------

    service = UserService(
        database
    )


    # -------------------------------------------------------------------------
    # Find User
    # -------------------------------------------------------------------------

    user = service.get_user_by_id(
        user_id
    )


    if not user:

        raise not_found_exception(
            "User not found"
        )


    # -------------------------------------------------------------------------
    # Ownership Validation
    # -------------------------------------------------------------------------

    if user.id != current_user.id:

        raise authorization_exception(
            "Not authorized"
        )


    # -------------------------------------------------------------------------
    # Delete User
    # -------------------------------------------------------------------------

    service.delete_user(
        user_id
    )


    return ResponseSchema(
        success=True,
        message="User deleted successfully",
        data={}
    )
