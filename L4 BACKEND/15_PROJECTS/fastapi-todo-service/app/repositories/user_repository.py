# -----------------------------------------------------------------------------
# User Repository
# -----------------------------------------------------------------------------

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User

# -----------------------------------------------------------------------------
# User Repository Class
# -----------------------------------------------------------------------------

class UserRepository:
    """ Repository responsible for user database operations."""

    # -------------------------------------------------------------------------
    # Constructor
    # -------------------------------------------------------------------------

    def __init__(self, database: Session) -> None:
        """Initialize repository with database session."""

        self.database = database

    # -------------------------------------------------------------------------
    # Create User
    # -------------------------------------------------------------------------

    def create_user(self, user: User) -> User:
        """Create a new user record."""

        self.database.add(user)
        self.database.commit()
        self.database.refresh(user)

        return user

    # -------------------------------------------------------------------------
    # Get User By ID
    # -------------------------------------------------------------------------

    def get_user_by_id(self, user_id: int) -> User | None:
        """Retrieve user by primary key."""

        statement = select(User).where(User.id == user_id)
        result = self.database.execute(statement)
        return result.scalar_one_or_none()

    # -------------------------------------------------------------------------
    # Get User By Email
    # -------------------------------------------------------------------------

    def get_user_by_email(self, email: str) -> User | None:
        """Retrieve user by email address."""

        statement = select(User).where(User.email == email)
        result = self.database.execute(statement)
        return result.scalar_one_or_none()

    # -------------------------------------------------------------------------
    # Get All Users
    # -------------------------------------------------------------------------

    def get_all_users(self) -> list[User]:
        """Retrieve all users."""

        statement = select(User)
        result = self.database.execute(statement)
        return list(result.scalars().all())

    # -------------------------------------------------------------------------
    # Update User
    # -------------------------------------------------------------------------

    def update_user(self, user: User) -> User:
        """Update user record."""

        user = self.database.merge(user)
        self.database.commit()
        self.database.refresh(user)
        return user

    # -------------------------------------------------------------------------
    # Delete User
    # -------------------------------------------------------------------------

    def delete_user(self, user_id: int) -> None:
        """Delete user record."""

        user = self.get_user_by_id(user_id)

        if user:
            self.database.delete(user)
            self.database.commit()
