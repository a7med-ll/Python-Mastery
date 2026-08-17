from fastapi import FastAPI, Header, HTTPException

# -----------------------------------------------------------------------------
# Create FastAPI Application
# -----------------------------------------------------------------------------

app = FastAPI(
    title="L4-007 Idempotency",
    description="Learn API idempotency using idempotency keys.",
    version="1.0.0"
)

# -----------------------------------------------------------------------------
# Create Idempotency Store
# -----------------------------------------------------------------------------

idempotency_store = {}

# -----------------------------------------------------------------------------
# Create Transfer Endpoint
# -----------------------------------------------------------------------------

@app.get("/transfers")
def l4_007CreateTransfer(
        amount: float,
        idempotency_key: str = Header(alias="Idempotency-Key"),
) -> dict:
    """Create transfer using an idempotency key."""

    # Validate transfer amount.
    if amount <= 0:
        raise HTTPException(
            status_code = 400,
            detail="Transfer amount must be greater than zero."
        )

    # Check if idempotency key was already processed
    if idempotency_key in idempotency_store:

        print("Duplicate request detected.")

        # Return previously stored response.
        return idempotency_store[idempotency_key]

    # Create transfer response.
    transfer_response = {
        "transfer_id": len(idempotency_store) + 1,
        "amount": amount,
        "status": "completed"
    }

    # Store response using idempotency key.
    idempotency_store[
        idempotency_key
    ] = transfer_response

    print("New transfer processed.")

    return transfer_response

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