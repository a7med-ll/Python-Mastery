# -----------------------------------------------------------------------------
# API Dependencies
# -----------------------------------------------------------------------------

from collections.abc import Generator

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from app.core.security import decode_access_token

from app.core.exceptions import (
    authentication_exception
)

from app.database.session import SessionLocal

from app.models.user import User

from app.repositories.user_repository import UserRepository



# -----------------------------------------------------------------------------
# OAuth2 Configuration
# -----------------------------------------------------------------------------

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)



# -----------------------------------------------------------------------------
# Database Session Provider
# -----------------------------------------------------------------------------

def get_database_session() -> Generator[Session, None, None]:
    """
    Provide database session.
    """

    database = SessionLocal()


    try:

        yield database


    finally:

        database.close()



# -----------------------------------------------------------------------------
# Current User Dependency
# -----------------------------------------------------------------------------

def get_current_user(
        token: str = Depends(oauth2_scheme),
        database: Session = Depends(get_database_session)
) -> User:
    """
    Retrieve authenticated user.
    """


    # -------------------------------------------------------------------------
    # Decode Token
    # -------------------------------------------------------------------------

    payload = decode_access_token(
        token
    )


    if payload is None:

        raise authentication_exception(
            "Invalid or expired authentication token"
        )


    # -------------------------------------------------------------------------
    # Extract User ID
    # -------------------------------------------------------------------------

    user_id = payload.get(
        "sub"
    )


    if user_id is None:

        raise authentication_exception(
            "Invalid token payload"
        )


    try:

        user_id = int(
            user_id
        )


    except ValueError:

        raise authentication_exception(
            "Invalid user identifier"
        )



    # -------------------------------------------------------------------------
    # Load User
    # -------------------------------------------------------------------------

    user_repository = UserRepository(
        database
    )


    user = user_repository.get_user_by_id(
        user_id
    )


    if user is None:

        raise authentication_exception(
            "User not found"
        )



    # -------------------------------------------------------------------------
    # Check Account Status
    # -------------------------------------------------------------------------

    if not user.is_active:

        raise authentication_exception(
            "User account is inactive"
        )


    return user