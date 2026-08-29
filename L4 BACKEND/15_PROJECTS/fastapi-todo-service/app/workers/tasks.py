"""Background task helpers.

The service does not need a separate task queue yet. Small background jobs can
be added here when a real use case is introduced.
"""


def todo_created_message(todo_id: int) -> str:
    """Create a simple message that can be logged in a background task."""

    return f"Todo created: {todo_id}"
