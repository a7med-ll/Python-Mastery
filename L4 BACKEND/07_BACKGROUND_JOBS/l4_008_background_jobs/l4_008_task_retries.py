import time

from celery import Celery

# -----------------------------------------------------------------------------
# Create Celery Application
# -----------------------------------------------------------------------------

celery_app = Celery(
    "l4_008_task_retries",
    broker="redis://localhost:6379/0"
)

# -----------------------------------------------------------------------------
# Send Confirmation Email Task
# -----------------------------------------------------------------------------

@celery_app.task(
    bind=True,
    max_retries=3
)

def l4_008SendConfirmationEmail(
        self,
        customer_name: str,
        product: str
) -> str:
    """Simulate an email task with automatic retries."""

    # Get the current retry count.
    retry_count = self.request.retries

    # Show current task attempt.
    print(
        f"Executing email task. Retry count: {retry_count}"
    )

    try:

        # Simulate temporary failure for the first two executions.
        if retry_count < 2:
            raise ConnectionError(
                "Email service temporarily unavailable."
            )

        # Simulate successful email processing.
        time.sleep(2)

        # Create successful task message.
        message = (
            f"Confirmation email sent to {customer_name} "
            f"for {product}."
        )

        # Show successful task.
        print(message)

        return message

    except ConnectionError as error:

        # Show temporary task failure.
        print(
            f"Task failed: {error}"
        )

        # Retry the task after 5 seconds.
        raise self.retry(
            exc=error,
            countdown=5
        )

# -----------------------------------------------------------------------------
# Send Task To Celery
# -----------------------------------------------------------------------------

def run_l4_008TaskRetries() -> None:
    """Send retry example task to Celery."""

    # Send task to Redis for background processing.
    task = l4_008SendConfirmationEmail.delay(
        "Ahmed",
        "Laptop"
    )

    # Show that the task was submitted.
    print("Task submitted to Celery.")

    # Show Celery task ID.
    print(
        f"Task ID: {task.id}"
    )


# -----------------------------------------------------------------------------
# Program Entry Point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    run_l4_008TaskRetries()
