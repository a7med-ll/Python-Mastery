import time

from fastapi import BackgroundTasks, FastAPI
from pydantic import BaseModel

# -----------------------------------------------------------------------------
# Create FastAPI Application
# -----------------------------------------------------------------------------

app = FastAPI(
    title="L4-008 FastAPI Background Tasks",
    description="Learn basic background task processing using FastAPI.",
    version="1.0.0"
)

# -----------------------------------------------------------------------------
# Order Request Model
# -----------------------------------------------------------------------------

class OrderRequest(BaseModel):
    """Define order request data."""

    customer_name: str
    product: str

# -----------------------------------------------------------------------------
# Send Confirmation Email
# -----------------------------------------------------------------------------

def l4_008SendConfirmationEmail(
        customer_name: str,
        product: str,
) -> None:
    """Simulate sending an order confirmation email."""

    # Show that the background task has started.
    print("Background task started.")

    # Simulate a slow email operation.
    time.sleep(5)

    # Show that the background task has completed.
    print(
        f"Confirmation email sent to {customer_name} "
        f"for {product}."
    )

# -----------------------------------------------------------------------------
# Create Order
# -----------------------------------------------------------------------------

@app.post("/orders")
def l4_008CreateOrder(
        order: OrderRequest,
        background_tasks: BackgroundTasks,
) -> dict:
    """Create an order and schedule confirmation email."""

    # Simulate creating the order.
    print(
        f"Order created for {order.customer_name}: "
        f"{order.product}"
    )

    # Register email function as a background task. ****
    background_tasks.add_task(
        l4_008SendConfirmationEmail,
        order.customer_name,
        order.product,
    )

    # Return response without waiting for email task to complete.
    return {
        "message": "Order created successfully.",
        "customer_name": order.customer_name,
        "product": order.product
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