from getpass import getpass

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from l4_006_create_users import User
from l4_006_jwt_tokens import l4_006CreateAccessToken

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
# Login User
# -----------------------------------------------------------------------------

def l4_006LoginUser() -> None:
    """Authenticate user and create access token."""

    # Get login credentials from user.
    email = input("Email: ")
    password = getpass("Password: ")

    # Open database session.
    with Session(engine) as session:

        # Find user using email.
        user = (
            session.query(User)
            .filter(User.email == email)
            .first()
        )

        # Check if user exists.
        if user is None:
            print("Invalid email or password.")
            return

        # Verify entered password against stored password hash.
        try:
            password_hasher.verify(
                user.password_hash,
                password
            )

        except VerifyMismatchError:
            print("Invalid email or password.")
            return

        # Create JWT access token.
        access_token = l4_006CreateAccessToken(
            user_id=user.user_id,
            role=user.role
        )

        # Print successful login.
        print("Login successful.")
        print(f"Welcome: {user.name}")
        print(f"Role: {user.role}")
        print(f"Access Token: {access_token}")

# -----------------------------------------------------------------------------
# Program Entry Point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    l4_006LoginUser()