"""This is the backend service that Nginx will forward requests to."""

from fastapi import FastAPI


# -----------------------------------------------------------------------------
# Create FastAPI Application
# -----------------------------------------------------------------------------

app = FastAPI(
    title="L4-013 Nginx Reverse Proxy API"
)

# -----------------------------------------------------------------------------
# Health Check Endpoint
# -----------------------------------------------------------------------------

@app.get("/")
def l4_013HealthCheck() -> dict:
    """
    Return application health status.
    """

    return {
        "application": "L4-013 FastAPI Backend",
        "status": "running",
        "service": "backend"
    }

# -----------------------------------------------------------------------------
# Customer API Endpoint
# -----------------------------------------------------------------------------

@app.get("/customers/{customer_id}")
def l4_013GetCustomer(
    customer_id: int,
) -> dict:
    """
    Return customer information.
    """

    return {
        "customer_id": customer_id,
        "name": "Ahmed",
        "status": "ACTIVE"
    }