# -----------------------------------------------------------------------------
# Todo Repository
# -----------------------------------------------------------------------------

from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.todo import Todo

# -----------------------------------------------------------------------------
# Todo Repository Class
# -----------------------------------------------------------------------------

class TodoRepository:
    """ Repository responsible for todo database operations."""

    # -------------------------------------------------------------------------
    # Constructor
    # -------------------------------------------------------------------------

    def __init__(self, database: Session) -> None:
        """Initialize repository with database session."""

        self.database = database

    # -------------------------------------------------------------------------
    # Create Todo
    # -------------------------------------------------------------------------

    def create_todo(self, todo: Todo) -> Todo:
        """Create a new todo record."""

        self.database.add(todo)
        self.database.commit()
        self.database.refresh(todo)
        return todo

    # -------------------------------------------------------------------------
    # Get Todo By ID
    # -------------------------------------------------------------------------

    def get_todo_by_id(self, todo_id: int) -> Todo | None:
        """Retrieve todo by primary key."""

        statement = select(Todo).where(Todo.id == todo_id)
        result = self.database.execute(statement)
        return result.scalar_one_or_none()

    # -----------------------------------------------------------------------------
    # Get User Todos With Pagination
    # -----------------------------------------------------------------------------

    def get_user_todos(
            self,
            user_id: int,
            page: int = 1,
            limit: int = 10
    ):
        """
        Retrieve user todos with pagination.
        """

        # -------------------------------------------------------------------------
        # Calculate Offset
        # -------------------------------------------------------------------------

        offset = (page - 1) * limit

        # -------------------------------------------------------------------------
        # Get Total Records
        # -------------------------------------------------------------------------

        total = (
            self.database
            .query(Todo)
            .filter(
                Todo.owner_id == user_id
            )
            .count()
        )

        # -------------------------------------------------------------------------
        # Get Paginated Records
        # -------------------------------------------------------------------------

        todos = (
            self.database
            .query(Todo)
            .filter(
                Todo.owner_id == user_id
            )
            .offset(offset)
            .limit(limit)
            .all()
        )

        return {
            "items": todos,
            "total": total
        }

    # -------------------------------------------------------------------------
    # Get All Todos
    # -------------------------------------------------------------------------

    def get_all_todos(self) -> list[Todo]:
        """Retrieve all todos records."""

        statement = select(Todo)
        result = self.database.execute(statement)
        return list(result.scalars().all())

    # -------------------------------------------------------------------------
    # Update Todo
    # -------------------------------------------------------------------------

    def update_todo(self, todo: Todo) -> Todo:
        """Update existing todo record."""

        todo = self.database.merge(todo)
        self.database.commit()
        self.database.refresh(todo)
        return todo

    # -------------------------------------------------------------------------
    # Delete Todo
    # -------------------------------------------------------------------------

    def delete_todo(self, todo_id: int) -> None:
        """Delete todo record."""

        todo = self.get_todo_by_id(todo_id)

        if todo:
            self.database.delete(todo)
            self.database.commit()
