from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.responses import Response

# -----------------------------------------------------------------------------
# Create FastAPI Application
# -----------------------------------------------------------------------------

app = FastAPI(
    title="L4-007 Error Responses",
    description="Learn consistent API error response conventions.",
    version="1.0.0"
)

# -----------------------------------------------------------------------------
# Create Dummy Customer Data
# -----------------------------------------------------------------------------

customers = {
    1: {
        "customer_id": 1,
        "name": "Ahmed",
        "status": "active"
    },
    2: {
        "customer_id": 2,
        "name": "Lokesh",
        "status": "inactive"
    }
}

# -----------------------------------------------------------------------------
# Create Error Response
# -----------------------------------------------------------------------------

def l4_007CreateErrorResponse(
    status_code: int,
    error_code: str,
    message: str
) -> JSONResponse:
    """Create a standard API error response."""

    # Create and return standard error response.
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": error_code,
                "message": message,
                "status": status_code
            }
        }
    )

# -----------------------------------------------------------------------------
# Get Customer
# -----------------------------------------------------------------------------

@app.get("/customers/{customer_id}")
def l4_007GetCustomer(
    customer_id: int
) -> Response:
    """Return customer or standard error response."""

    # Find customer using customer ID.
    customer = customers.get(
        customer_id
    )

    # Check if customer exists.
    if customer is None:
        return l4_007CreateErrorResponse(
            status_code=404,
            error_code="CUSTOMER_NOT_FOUND",
            message="Customer was not found."
        )

    # Return customer.
    return customer

# -----------------------------------------------------------------------------
# Activate Customer
# -----------------------------------------------------------------------------

@app.post("/customers/{customer_id}/activate")
def l4_007ActivateCustomer(
    customer_id: int
) -> Response:
    """Activate customer or return standard error response."""

    # Find customer using customer ID.
    customer = customers.get(
        customer_id
    )

    # Check if customer exists.
    if customer is None:
        return l4_007CreateErrorResponse(
            status_code=404,
            error_code="CUSTOMER_NOT_FOUND",
            message="Customer was not found."
        )

    # Check if customer is already active.
    if customer["status"] == "active":
        return l4_007CreateErrorResponse(
            status_code=409,
            error_code="CUSTOMER_ALREADY_ACTIVE",
            message="Customer is already active."
        )

    # Activate customer.
    customer["status"] = "active"

    return {
        "customer_id": customer["customer_id"],
        "status": customer["status"]
    }

# -----------------------------------------------------------------------------
# Program Entry Point
# -----------------------------------------------------------------------------

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )