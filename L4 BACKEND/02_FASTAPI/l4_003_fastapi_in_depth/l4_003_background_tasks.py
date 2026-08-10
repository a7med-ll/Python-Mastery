from fastapi import BackgroundTasks, FastAPI

# -----------------------------------------------------------------------------
# Create FastAPI Application
# -----------------------------------------------------------------------------

app = FastAPI()

# -----------------------------------------------------------------------------
# Background Task
# -----------------------------------------------------------------------------

def l4_003SendWelcomeEmail(email: str) -> None:
    """Simulate sending a welcome email."""

    print(f"Welcome email sent to: {email}")


# -----------------------------------------------------------------------------
# Customer Route
# -----------------------------------------------------------------------------

@app.post("/customers")
def l4_003CreateCustomer(
    email: str,
    background_tasks: BackgroundTasks
) -> dict:
    """Create a customer and schedule a background task."""

    # Add task to run after response is returned.
    background_tasks.add_task(
        l4_003SendWelcomeEmail,
        email
    )

    return {
        "message": "Customer created successfully",
        "email": email
    }