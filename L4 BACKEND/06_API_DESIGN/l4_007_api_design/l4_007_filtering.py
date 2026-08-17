from fastapi import FastAPI, Query

# -----------------------------------------------------------------------------
# Create FastAPI Application
# -----------------------------------------------------------------------------

app = FastAPI(
    title="L4-007 Filtering",
    description="Learn API filtering using FastAPI.",
    version="1.0.0"
)

# -----------------------------------------------------------------------------
# Create Dummy Customer Data
# -----------------------------------------------------------------------------

customers = [
    {
        "customer_id": 1,
        "name": "Ahmed",
        "country": "UAE",
        "status": "active"
    },
    {
        "customer_id": 2,
        "name": "Lokesh",
        "country": "UK",
        "status": "active"
    },
    {
        "customer_id": 3,
        "name": "Sara",
        "country": "UAE",
        "status": "inactive"
    },
    {
        "customer_id": 4,
        "name": "John",
        "country": "USA",
        "status": "active"
    }
]

# -----------------------------------------------------------------------------
# Get Customers With Filters
# -----------------------------------------------------------------------------

@app.get("/customers")
def l4_007GetCustomers(
    country: str | None = Query(default=None),
    status: str | None = Query(default=None)
) -> dict:
    """Return customers using optional filters."""

    # Start with all customers.
    filtered_customers = customers

    # Filter by country if provided.
    if country is not None:
        filtered_customers = [
            customer
            for customer in filtered_customers
            if customer["country"].lower() == country.lower()
        ]

    # Filter by status if provided.
    if status is not None:
        filtered_customers = [
            customer
            for customer in filtered_customers
            if customer["status"].lower() == status.lower()
        ]

    # Return filtered response.
    return {
        "total": len(filtered_customers),
        "items": filtered_customers
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