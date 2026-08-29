# -----------------------------------------------------------------------------
# User Service
# -----------------------------------------------------------------------------

from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.cache.cache_service import cache_service
from datetime import datetime


# -----------------------------------------------------------------------------
# User Service Class
# -----------------------------------------------------------------------------

class UserService:
    """ Service layer responsible for user business logic."""

    # -------------------------------------------------------------------------
    # Constructor
    # -------------------------------------------------------------------------

    def __init__(self, database: Session) -> None:
        """Initialize repository with database session."""
        self.user_repository = UserRepository(database)

    # -------------------------------------------------------------------------
    # Create User
    # -------------------------------------------------------------------------

    def create_user(self, user: User) -> User:
        """Create new user in database."""

        existing_user = self.user_repository.get_user_by_email(user.email)

        if existing_user:
            raise ValueError("User with this email already exists")

        return self.user_repository.create_user(user)

    # -------------------------------------------------------------------------
    # Get User By ID
    # -------------------------------------------------------------------------

    def get_user_by_id(
            self,
            user_id: int
    ) -> User | None:
        """
        Retrieve user by ID with cache support.
        """

        # ---------------------------------------------------------------------
        # Generate Cache Key
        # ---------------------------------------------------------------------

        cache_key = f"user:{user_id}"

        # ---------------------------------------------------------------------
        # Check Redis Cache
        # ---------------------------------------------------------------------

        cached_user = cache_service.get(
            cache_key
        )

        if cached_user:
            return User(
                id=cached_user["id"],
                email=cached_user["email"],
                is_active=cached_user["is_active"],
                created_at=datetime.fromisoformat(cached_user["created_at"]),
            )

        # ---------------------------------------------------------------------
        # Fetch From Database
        # ---------------------------------------------------------------------

        user = self.user_repository.get_user_by_id(
            user_id
        )

        if user is None:
            return None

        # ---------------------------------------------------------------------
        # Store User In Cache
        # ---------------------------------------------------------------------

        cache_service.set(
            cache_key,
            {
                "id": user.id,
                "email": user.email,
                "is_active": user.is_active,
                "created_at": user.created_at.isoformat()
            }
        )

        return user

    # -------------------------------------------------------------------------
    # Get User By Email
    # -------------------------------------------------------------------------

    def get_user_by_email(self, email: str) -> User | None:
        """Retrieve user by email."""

        return self.user_repository.get_user_by_email(email)

    # -------------------------------------------------------------------------
    # Get All Users
    # -------------------------------------------------------------------------

    def get_all_users(self) -> list[User]:
        """Retrieve all users in database."""

        return self.user_repository.get_all_users()

    # -------------------------------------------------------------------------
    # Update User
    # -------------------------------------------------------------------------

    def update_user(
            self,
            user: User
    ) -> User:
        """
        Update existing user and clear cache.
        """

        updated_user = self.user_repository.update_user(
            user
        )

        # ---------------------------------------------------------------------
        # Remove Old Cache
        # ---------------------------------------------------------------------

        cache_key = f"user:{user.id}"

        cache_service.delete(
            cache_key
        )

        return updated_user

    # -------------------------------------------------------------------------
    # Delete User
    # -------------------------------------------------------------------------

    def delete_user(
            self,
            user_id: int
    ) -> None:
        """
        Delete user and clear cache.
        """

        self.user_repository.delete_user(
            user_id
        )

        # ---------------------------------------------------------------------
        # Remove Cache
        # ---------------------------------------------------------------------

        cache_key = f"user:{user_id}"

        cache_service.delete(
            cache_key
        )