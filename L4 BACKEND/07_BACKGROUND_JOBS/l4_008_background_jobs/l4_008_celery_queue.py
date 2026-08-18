"""This file combines FastAPI + Celery + Redis."""

import time

from celery import Celery
from fastapi import FastAPI
from pydantic import BaseModel

# -----------------------------------------------------------------------------
# Create FastAPI Application
# -----------------------------------------------------------------------------

app = FastAPI(
    title="L4-008 Celery Queue",
    description="Process FastAPI background jobs using Celery and Redis.",
    version="1.0.0"
)

# -----------------------------------------------------------------------------
# Create Celery Application
# -----------------------------------------------------------------------------

celery_app = Celery(
    "l4_008_celery_queue",
    broker="redis://localhost:6379/0"
)

# -----------------------------------------------------------------------------
# Order Request Model
# -----------------------------------------------------------------------------

class OrderRequest(BaseModel):
    """Define order request data."""

    customer_name: str
    product: str

# -----------------------------------------------------------------------------
# Send Confirmation Email Task
# -----------------------------------------------------------------------------

@celery_app.task
def l4_008SendConfirmationEmail(
        customer_name: str,
        product: str,
) -> str:
    """Simulate sending an order confirmation email."""

    # Show that Celery worker started the task.
    print(
        f"Sending confirmation email to {customer_name}..."
    )

    # Simulate slow email processing.
    time.sleep(5)

    # Create completed task message.
    message = (
        f"Confirmation email sent to {customer_name} "
        f"for {product}."
    )

    # Show completed task.
    print(message)

    return message

# -----------------------------------------------------------------------------
# Create Order
# -----------------------------------------------------------------------------

@app.post("/orders")
def l4_008CreateOrder(order: OrderRequest) -> dict:
    """Create an order and queue confirmation email."""

    # Simulate creating the order.
    print(
        f"Order created for {order.customer_name}: "
        f"{order.product}"
    )

    # Send email task to Celery queue. ***
    task = l4_008SendConfirmationEmail.delay(
        order.customer_name,
        order.product,
    )

    # Return response without waiting for email task.
    return {
        "message": "Order created successfully.",
        "customer_name": order.customer_name,
        "product": order.product,
        "task_id": task.id
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
