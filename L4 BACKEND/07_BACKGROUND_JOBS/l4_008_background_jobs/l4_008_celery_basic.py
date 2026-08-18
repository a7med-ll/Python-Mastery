import time

from celery import Celery

# -----------------------------------------------------------------------------
# Create Celery Application
# -----------------------------------------------------------------------------

celery_app = Celery(
    "l4_008_celery_basic",
    broker="redis://localhost:6379/0"
)

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

    # Simulate a slow email operation.
    time.sleep(5)

    # Create task result.
    message = (
        f"Confirmation email sent to {customer_name} "
        f"for {product}."
    )

    # Show completed task.
    print(message)

    return message

# -----------------------------------------------------------------------------
# Send Task To Celery
# -----------------------------------------------------------------------------

def run_l4_008CeleryBasic() -> None:
    """Send confirmation email task to Celery."""

    # Send task to Redis for background processing.
    task = l4_008SendConfirmationEmail.delay(
        "Ahmed",
        "Laptop"
    )

    # Show that task was successfully submitted.
    print("Task submitted to Celery.")

    # Print Celery task ID.
    print(
        f"Task ID: {task.id}"
    )

# -----------------------------------------------------------------------------
# Program Entry Point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    run_l4_008CeleryBasic()