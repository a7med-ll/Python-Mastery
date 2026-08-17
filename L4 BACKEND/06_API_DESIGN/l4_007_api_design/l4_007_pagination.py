"""use 25 dummy customers so you can clearly test multiple pages."""

import math

from fastapi import FastAPI, Query

# -----------------------------------------------------------------------------
# Create FastAPI Application
# -----------------------------------------------------------------------------

app = FastAPI(
    title="L4-007 Pagination",
    description="Learn API pagination using FastAPI.",
    version="1.0.0"
)


# -----------------------------------------------------------------------------
# Create Dummy Customer Data
# -----------------------------------------------------------------------------

customers = [
    {
        "customer_id":1,
        "name": f"Customer {customer_id}"
    }
    for customer_id in range(1,26)
]

# -----------------------------------------------------------------------------
# Get Customers With Pagination
# -----------------------------------------------------------------------------

@app.get("/customers")
def l4_007GetCustomers(
        page: int = Query(1, ge=1),
        size: int = Query(10, ge=1, le=10),
) -> dict:
    """Return customers using pagination."""

    # Get total number of customers.
    total_customers = len(customers)

    # Calculate total number of pages.
    total_pages = math.ceil(total_customers / size)

    # Calculate how many records to skip.
    offset = (page - 1) * size

    # Calculate where the current page should end.
    end = offset + size

    # Get customers for the requested page.
    paginated_customers = customers[offset:end]

    # Return paginated response.
    return {
        "page": page,
        "size": size,
        "total": total_customers,
        "total_pages": total_pages,
        "items": paginated_customers
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