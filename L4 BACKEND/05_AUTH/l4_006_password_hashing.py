from pwdlib import PasswordHash

# -----------------------------------------------------------------------------
# Create Password Hasher
# -----------------------------------------------------------------------------

password_hasher = PasswordHash.recommended()

# -----------------------------------------------------------------------------
# Hash Password
# -----------------------------------------------------------------------------

def l4_006HashPassword(password: str) -> str:
    """Hash a plain-text password."""

    # Generate secure password hash.
    hashed_password = password_hasher.hash(
        password
    )

    return hashed_password

# -----------------------------------------------------------------------------
# Verify Password
# -----------------------------------------------------------------------------

def l4_006VerifyPassword(
        plain_password: str,
        hashed_password: str,
) -> bool:
    """Verify a password against a hashed password."""

    # Compare plain password with stored hash.
    return password_hasher.verify(
        plain_password,
        hashed_password
    )

# -----------------------------------------------------------------------------
# Run Password Hashing Example
# -----------------------------------------------------------------------------

def run_l4_006PasswordHashing() -> None:
    """Run password hashing example."""

    # Create Example Password
    password = "Ahmed@1234"

    # Hash Password
    hashed_password = l4_006HashPassword(
        password
    )

    # Print Original Password
    print(f"Password: {password}")

    # Print Hashed Password
    print(f"Password: {hashed_password}")

    # Verify correct password.
    correct_result = l4_006VerifyPassword(
        "Ahmed@1234",
        hashed_password
    )

    # Verify incorrect password.
    incorrect_result = l4_006VerifyPassword(
        "WrongPassword",
        hashed_password
    )

    # Print verification results.
    print(f"Correct password: {correct_result}")
    print(f"Wrong password: {incorrect_result}")

# -----------------------------------------------------------------------------
# Program Entry Point
# -----------------------------------------------------------------------------

if __name__ == '__main__':
    run_l4_006PasswordHashing()



