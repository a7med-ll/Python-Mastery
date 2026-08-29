# -----------------------------------------------------------------------------
# Authentication Service
# -----------------------------------------------------------------------------

from sqlalchemy.orm import Session

from app.models.user import User

from app.repositories.user_repository import UserRepository

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)

# -----------------------------------------------------------------------------
# Authentication Service Class
# -----------------------------------------------------------------------------

class AuthService:
    """Service layer responsible for authentication logic."""

    # -------------------------------------------------------------------------
    # Constructor
    # -------------------------------------------------------------------------

    def __init__(self, database: Session) -> None:
        """Initialize authentication service."""

        self.user_repository = UserRepository(database)

    # -------------------------------------------------------------------------
    # Register User
    # -------------------------------------------------------------------------

    def register_user(self, email: str, password: str) -> User:
        """Register a new user."""

        existing_user = self.user_repository.get_user_by_email(email)

        if existing_user:
            raise ValueError("User with this email already exists")

        user = User(email=email, hashed_password=hash_password(password))

        return self.user_repository.create_user(user)

    # -------------------------------------------------------------------------
    # Login User
    # -------------------------------------------------------------------------

    def login_user(self, email: str, password: str) -> str:
        """Authenticate user and generate JWT token."""

        user = self.user_repository.get_user_by_email(email)

        if user is None:
            raise ValueError("Invalid email or password")

        if not user.is_active:
            raise ValueError("User account is inactive")

        if not verify_password(password, user.hashed_password):
            raise ValueError("Invalid email or password")

        # Create JWT token with user id.
        token = create_access_token(
            {
                "sub": str(user.id)
            }
        )

        return token
