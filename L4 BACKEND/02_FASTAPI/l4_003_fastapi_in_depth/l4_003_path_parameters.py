from fastapi import FastAPI

# -----------------------------------------------------------------------------
# Create FastAPI Application
# -----------------------------------------------------------------------------

app = FastAPI()

# -----------------------------------------------------------------------------
# Home Route
# -----------------------------------------------------------------------------

@app.get("/")
def l4_003HomeRoute() -> dict:
    """Return the home route."""

    return {
        "message": "Path Parameters Demo"
    }

# -----------------------------------------------------------------------------
# Customer Route
# -----------------------------------------------------------------------------

@app.get("/customers/{customer_id}")
def l4_003CustomerRoute(customer_id: int) -> dict:
    """Return a customer ID."""

    return {
        "customer_id": customer_id
    }

# -----------------------------------------------------------------------------
# Product Route
# -----------------------------------------------------------------------------

@app.get("/product/{product_id}")
def l4_003ProductRoute(product_id: int) -> dict:
    """Return a product ID."""

    return {
        "product_id": product_id
    }