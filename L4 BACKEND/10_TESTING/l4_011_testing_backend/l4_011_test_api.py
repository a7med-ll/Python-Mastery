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
def get_customer(
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
    app                   # --> testing the FastAPI app
)

# -----------------------------------------------------------------------------
# Test Customer Endpoint
# -----------------------------------------------------------------------------

def test_l4_011GetCustomer() -> None:
    """Test customer endpoint."""

    # Send GET request to FastAPI application.
    response = client.get(
        "/customers/1001"
    )

    # Verify HTTP status code.
    assert response.status_code == 200

    # Convert JSON response into Python dictionary.
    response_data = response.json()

    # Verify customer ID
    assert response_data["customer_id"] == 1001

    # Verify customer name
    assert response_data["name"] == "Ahmed"

    # Verify customer status
    assert response_data["status"] == "ACTIVE"