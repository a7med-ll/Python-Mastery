from fastapi import APIRouter, FastAPI

# -----------------------------------------------------------------------------
# Create FastAPI Application
# -----------------------------------------------------------------------------

app = FastAPI(
    title="L4-007 API Versioning",
    description="Learn API versioning using FastAPI routers.",
    version="1.0.0"
)

# -----------------------------------------------------------------------------
# Create API Version Routers
# -----------------------------------------------------------------------------

# Create router for API version 1.
v1_router = APIRouter(
    prefix="/api/v1",
)

# Create router for API version 2.
v2_router = APIRouter(
    prefix="/api/v2",
)

# -----------------------------------------------------------------------------
# Version 1 Customer Endpoint
# -----------------------------------------------------------------------------

@v1_router.get("/customers/{customer_id}")
def l4_007GetCustomerV1(customer_id: int):
    """Return customer using the version 1 response structure."""

    return {
        "id": customer_id,
        "name":"Ahmed",
        "age": 30
    }

# -----------------------------------------------------------------------------
# Version 2 Customer Endpoint
# -----------------------------------------------------------------------------

@v2_router.get("/customers/{customer_id}")
def l4_007GetCustomerV2(customer_id: int):
    """Return customer using the version 2 response structure."""

    return {
        "customer_id":customer_id,
        "full_name":"Ahmed Lateef",
        "email": "ahmed@example.com",
        "status": "active"
    }

# -----------------------------------------------------------------------------
# Register API Routers
# -----------------------------------------------------------------------------

# Register version 1 routes with FastAPI.
app.include_router(v1_router)

# Register version 2 routes with FastAPI.
app.include_router(v2_router)

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