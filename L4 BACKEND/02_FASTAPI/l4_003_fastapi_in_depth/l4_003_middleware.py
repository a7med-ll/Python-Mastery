from time import perf_counter

from fastapi import FastAPI, Request

# -----------------------------------------------------------------------------
# Create FastAPI Application
# -----------------------------------------------------------------------------

app = FastAPI()

# -----------------------------------------------------------------------------
# Request Timing Middleware
# -----------------------------------------------------------------------------

@app.middleware("http")
async def l4_003RequestTimingMiddleware(
    request: Request,
    call_next
):
    """Measure request execution time."""

    # Record request start time.
    start_time = perf_counter()

    # Execute the next component.
    response = await call_next(request)

    # Calculate execution time.
    elapsed_time = perf_counter() - start_time

    # Add execution time to response header.
    response.headers["X-Process-Time"] = str(elapsed_time)

    return response

# -----------------------------------------------------------------------------
# Home Route
# -----------------------------------------------------------------------------

@app.get("/")
def l4_003HomeRoute() -> dict:
    """Return home page."""

    return {
        "message": "Middleware Example"
    }

# -----------------------------------------------------------------------------
# Customer Route
# -----------------------------------------------------------------------------

@app.get("/customers")
def l4_003CustomersRoute() -> dict:
    """Return customers."""

    return {
        "customers": [
            "Ahmed",
            "John",
            "Sarah"
        ]
    }