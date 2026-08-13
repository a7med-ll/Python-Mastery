from argon2 import PasswordHasher
from sqlalchemy import String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

# -----------------------------------------------------------------------------
# Database Connection URL
# -----------------------------------------------------------------------------

DATABASE_URL = (
    "postgresql+psycopg://nadalateef@localhost:5432/python_mastery_db"
)

# -----------------------------------------------------------------------------
# Create Database Engine
# -----------------------------------------------------------------------------

engine = create_engine(DATABASE_URL)

# -----------------------------------------------------------------------------
# Create Password Hasher
# -----------------------------------------------------------------------------

password_hasher = PasswordHasher()

# -----------------------------------------------------------------------------
# Create ORM Base Class
# -----------------------------------------------------------------------------

class Base(DeclarativeBase):
    """Base class for ORM models."""

    pass

# -----------------------------------------------------------------------------
# User ORM Model
# -----------------------------------------------------------------------------

class User(Base):
    """Map the users table to a Python class."""

    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(100)
    )
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(50))

# -----------------------------------------------------------------------------
# Create Dummy Users
# -----------------------------------------------------------------------------

def l4_006CreateUsers() -> None:
    """Create dummy users with hashed passwords."""

    # Hash User Password
    ahmed_password_hash = password_hasher.hash("Ahmed@1234")
    lokesh_password_hash = password_hasher.hash("Lokesh@1234")

    # Create user objects.
    ahmed = User(
        name="Ahmed",
        email="ahmed@example.com",
        password_hash=ahmed_password_hash,
        role="admin",
    )

    lokesh = User(
        name="Lokesh",
        email="lokesh@example.com",
        password_hash=lokesh_password_hash,
        role="user",
    )

    # Open database session.
    with Session(engine) as session:

        # Add users to the session.
        session.add_all([
            ahmed,
            lokesh,
        ])

        # Save users permanently to PostgreSQL.
        session.commit()

    print("Users created successfully.")

# -----------------------------------------------------------------------------
# Program Entry Point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    l4_006CreateUsers()