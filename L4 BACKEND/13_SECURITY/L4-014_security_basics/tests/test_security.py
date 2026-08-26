from fastapi.testclient import TestClient

from fastapi_security_example.main import app


# -----------------------------------------------------------------------------
# Create Test Client
# -----------------------------------------------------------------------------

client = TestClient(app)

# -----------------------------------------------------------------------------
# Test Security Health Endpoint
# -----------------------------------------------------------------------------

def test_l4_014SecurityHealth() -> None:
    """Verify that the security health endpoint works."""

    response = client.get("/")

    # Verify successful response.
    assert response.status_code == 200

    # Verify security features exits
    data = response.json()

    assert "Input Validation" in data["security_features"]

    assert "Security Headers" in data["security_features"]

# -----------------------------------------------------------------------------
# Test Valid User Input
# -----------------------------------------------------------------------------

def test_l4_014ValidUserCreation() -> None:
    """Verify valid input is accepted."""

    response = client.post(
        "/users",
        json={
            "username": "Ahmed",
            "age": 30
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["user"]["username"] == "Ahmed"

    assert data["user"]["age"] == 30

# -----------------------------------------------------------------------------
# Test Invalid User Input
# -----------------------------------------------------------------------------

def test_l4_014InvalidUserValidation() -> None:
    """Verify invalid input is rejected."""

    response = client.post(
        "/users",
        json={
            "username": "A",
            "age": -5
        }
    )

    # Pydantic validation failure.
    assert response.status_code == 422

# -----------------------------------------------------------------------------
# Test SQL Injection Protection
# -----------------------------------------------------------------------------

def test_l4_014SQLInjectionProtection() -> None:
    """Verify suspicious input is blocked."""

    response = client.get(
        "/search/admin' OR '1'='1"
    )

    assert response.status_code == 400

# -----------------------------------------------------------------------------
# Test Security Headers
# -----------------------------------------------------------------------------

def test_l4_014SecurityHeaders() -> None:
    """Verify security headers exists."""

    response = client.get("/")

    assert response.headers[
               "X-Content-Type-Options"
           ] == "nosniff"

    assert response.headers[
               "X-Frame-Options"
           ] == "DENY"