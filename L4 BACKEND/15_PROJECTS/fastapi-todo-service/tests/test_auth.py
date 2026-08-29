# -----------------------------------------------------------------------------
# Authentication API Tests
# -----------------------------------------------------------------------------

import uuid



# -----------------------------------------------------------------------------
# Register User
# -----------------------------------------------------------------------------

def test_register_user(client):

    email = f"pytest_{uuid.uuid4()}@test.com"


    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": "test12345"
        }
    )


    assert response.status_code == 201


    data = response.json()


    assert data["success"] is True

    assert data["data"]["email"] == email



# -----------------------------------------------------------------------------
# Duplicate Email Registration
# -----------------------------------------------------------------------------

def test_register_duplicate_email(client):

    email = f"duplicate_{uuid.uuid4()}@test.com"


    first_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": "test12345"
        }
    )


    assert first_response.status_code == 201



    second_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": "test12345"
        }
    )


    assert second_response.status_code == 400



# -----------------------------------------------------------------------------
# Invalid Login
# -----------------------------------------------------------------------------

def test_login_invalid_password(client):

    email = f"login_{uuid.uuid4()}@test.com"


    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": "test12345"
        }
    )


    assert register_response.status_code == 201



    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": email,
            "password": "wrongpassword"
        }
    )


    assert login_response.status_code == 401


def test_login_success(client):

    email = f"success_{uuid.uuid4()}@test.com"

    client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "test12345"}
    )

    response = client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": "test12345"}
    )

    assert response.status_code == 200

    assert response.json()["data"]["token_type"] == "bearer"


def test_register_rejects_invalid_email_and_short_password(client):

    response = client.post(
        "/api/v1/auth/register",
        json={"email": "invalid-email", "password": "short"}
    )

    assert response.status_code == 422

    assert response.json()["error_code"] == "VALIDATION_ERROR"


def test_protected_route_rejects_missing_and_invalid_token(client):

    missing = client.get("/api/v1/users/me")

    invalid = client.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer invalid-token"}
    )

    assert missing.status_code == 401

    assert invalid.status_code == 401
