from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, Field

# -----------------------------------------------------------------------------
# Create FastAPI Application
# -----------------------------------------------------------------------------

app = FastAPI(
    title="L4-007 Customer API",
    description="Customer API demonstrating OpenAPI and Swagger documentation.",
    version="1.0.0"
)

# -----------------------------------------------------------------------------
# Customer Response Model
# -----------------------------------------------------------------------------

class CustomerResponse(BaseModel):
    """Define customer response structure."""

    customer_id: int = Field(
        description="Unique customer identifier."
    )

    full_name: str = Field(
        description="Customer full name."
    )

    email: str = Field(
        description="Customer email address."
    )

    status: str = Field(
        description="Current customer status."
    )

# -----------------------------------------------------------------------------
# Create Dummy Customer Data
# -----------------------------------------------------------------------------

customers = {
    1: {
        "customer_id": 1,
        "full_name": "Ahmed",
        "email": "ahmed@example.com",
        "status": "active"
    },
    2: {
        "customer_id": 2,
        "full_name": "Lokesh",
        "email": "lokesh@example.com",
        "status": "inactive"
    }
}

# -----------------------------------------------------------------------------
# Get Customer
# -----------------------------------------------------------------------------

@app.get(
    "/customers/{customer_id}",
    response_model=CustomerResponse,
    summary="Get customer",
    description="Return a customer using the customer ID.",
    tags=["Customers"],
    responses={
        404: {
            "description": "Customer not found."
        }
    }
)
def l4_007GetCustomer(
    customer_id: int = Path(
        ge=1,
        description="Unique customer identifier."
    )
) -> CustomerResponse:
    """Return customer information."""

    # Find customer using customer ID.
    customer = customers.get(
        customer_id
    )

    # Check if customer exists.
    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer was not found."
        )

    # Convert customer data into response model.
    return CustomerResponse(
        **customer
    )

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