from fastapi import FastAPI

# -----------------------------------------------------------------------------
# Create FastAPI Application
# -----------------------------------------------------------------------------

app = FastAPI()

# -----------------------------------------------------------------------------
# Customer Query Parameter
# -----------------------------------------------------------------------------

@app.get("/customers")
def l4_003CustomerQuery(country: str) -> dict:
    """Return customers filtered by country."""

    return {
        "country": country
    }


# -----------------------------------------------------------------------------
# Transaction Query Parameters
# -----------------------------------------------------------------------------

@app.get("/transactions")
def l4_003TransactionQuery(
    status: str,
    limit: int = 10
) -> dict:
    """Return transaction query parameters."""

    return {
        "status": status,
        "limit": limit
    }