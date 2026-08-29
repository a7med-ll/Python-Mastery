# -----------------------------------------------------------------------------
# Security Test
# -----------------------------------------------------------------------------

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token
)


def test_password_hashing():

    password = "test12345"

    hashed_password = hash_password(password)

    print(hashed_password)

    assert hashed_password != password

    assert verify_password(
        password,
        hashed_password
    )


def test_invalid_and_expired_tokens_are_rejected():

    expired_token = create_access_token(
        {"sub": "1"},
        expires_minutes=-1
    )

    assert decode_access_token("invalid-token") is None

    assert decode_access_token(expired_token) is None
