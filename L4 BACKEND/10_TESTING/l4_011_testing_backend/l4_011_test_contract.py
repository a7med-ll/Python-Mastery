from fastapi import FastAPI
from fastapi.testclient import TestClient


# -----------------------------------------------------------------------------
# Create FastAPI Application
# -----------------------------------------------------------------------------

app = FastAPI()


# -----------------------------------------------------------------------------
# Create Customer Endpoint
# -----------------------------------------------------------------------------

@app.get("/customers/{customer_id}")
def l4_011GetCustomer(
    customer_id: int,
) -> dict:
    """Return customer information."""

    # Create customer response.
    customer = {
        "customer_id": customer_id,
        "name": "Ahmed",
        "status": "ACTIVE",
    }

    return customer


# -----------------------------------------------------------------------------
# Create Test Client
# -----------------------------------------------------------------------------

client = TestClient(
    app
)


# -----------------------------------------------------------------------------
# Test Response Contract
# -----------------------------------------------------------------------------

def test_l4_011CustomerResponseContract() -> None:
    """Verify customer API response contract."""

    # Send GET request.
    response = client.get(
        "/customers/1001"
    )


    # Verify HTTP status.
    assert response.status_code == 200


    # Convert JSON response.
    response_data = response.json()


    # Verify required response fields.
    assert "customer_id" in response_data
    assert "name" in response_data
    assert "status" in response_data



# -----------------------------------------------------------------------------
# Test Response Data Types
# -----------------------------------------------------------------------------

def test_l4_011CustomerResponseDataTypes() -> None:
    """Verify customer response data types."""

    # Send GET request.
    response = client.get(
        "/customers/1001"
    )


    # Convert JSON response.
    response_data = response.json()


    # Verify field data types.
    assert isinstance(
        response_data["customer_id"],
        int
    )

    assert isinstance(
        response_data["name"],
        str
    )

    assert isinstance(
        response_data["status"],
        str
    )