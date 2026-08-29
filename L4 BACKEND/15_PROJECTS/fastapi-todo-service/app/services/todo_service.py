# -----------------------------------------------------------------------------
# Todo Service
# -----------------------------------------------------------------------------

from math import ceil
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.todo import Todo
from app.repositories.todo_repository import TodoRepository
from app.cache.cache_service import cache_service


# -----------------------------------------------------------------------------
# Todo Service Class
# -----------------------------------------------------------------------------

class TodoService:
    """Service layer responsible for todo business logic."""


    # -------------------------------------------------------------------------
    # Constructor
    # -------------------------------------------------------------------------

    def __init__(
            self,
            database: Session
    ) -> None:
        """
        Initialize todo repository.
        """

        self.todo_repository = TodoRepository(database)



    # -------------------------------------------------------------------------
    # Invalidate Todo Cache
    # -------------------------------------------------------------------------

    def _invalidate_todo_cache(
            self,
            todo_id: int,
            user_id: int
    ) -> None:
        """
        Remove todo related cache entries.
        """


        # ---------------------------------------------------------------------
        # Remove single todo cache
        # ---------------------------------------------------------------------

        cache_service.delete(
            f"todo:{todo_id}"
        )


        # ---------------------------------------------------------------------
        # Remove user pagination cache
        # ---------------------------------------------------------------------

        cache_service.delete_pattern(
            f"todos:user:{user_id}:*"
        )



    # -------------------------------------------------------------------------
    # Create Todo
    # -------------------------------------------------------------------------

    def create_todo(
            self,
            todo: Todo
    ) -> Todo:
        """
        Create todo record.
        """

        created_todo = self.todo_repository.create_todo(
            todo
        )


        self._invalidate_todo_cache(
            created_todo.id,
            created_todo.owner_id
        )


        return created_todo



    # -------------------------------------------------------------------------
    # Get Todo By ID With Cache
    # -------------------------------------------------------------------------

    def get_todo_by_id(
            self,
            todo_id: int
    ) -> Todo | None:
        """
        Retrieve todo by ID using cache.
        """

        cache_key = f"todo:{todo_id}"


        # ---------------------------------------------------------------------
        # Check Cache
        # ---------------------------------------------------------------------

        cached_todo = cache_service.get(
            cache_key
        )


        if cached_todo:

            return Todo(
                id=cached_todo["id"],
                title=cached_todo["title"],
                description=cached_todo["description"],
                completed=cached_todo["completed"],
                owner_id=cached_todo["owner_id"],
                created_at=datetime.fromisoformat(cached_todo["created_at"])
            )



        # ---------------------------------------------------------------------
        # Database Query
        # ---------------------------------------------------------------------

        todo = self.todo_repository.get_todo_by_id(
            todo_id
        )


        if todo is None:
            return None



        # ---------------------------------------------------------------------
        # Store Cache
        # ---------------------------------------------------------------------

        cache_service.set(
            cache_key,
            {
                "id": todo.id,
                "title": todo.title,
                "description": todo.description,
                "completed": todo.completed,
                "owner_id": todo.owner_id,
                "created_at": todo.created_at.isoformat()
            }
        )


        return todo



    # -------------------------------------------------------------------------
    # Get User Todos With Pagination And Cache
    # -------------------------------------------------------------------------

    def get_user_todos(
            self,
            user_id: int,
            page: int = 1,
            limit: int = 10
    ) -> dict:
        """
        Retrieve user todos with pagination.
        """

        cache_key = (
            f"todos:user:{user_id}:"
            f"page:{page}:"
            f"limit:{limit}"
        )


        # ---------------------------------------------------------------------
        # Check Cache
        # ---------------------------------------------------------------------

        cached_data = cache_service.get(
            cache_key
        )


        if cached_data:
            return cached_data



        # ---------------------------------------------------------------------
        # Database Query
        # ---------------------------------------------------------------------

        result = self.todo_repository.get_user_todos(
            user_id,
            page,
            limit
        )



        # ---------------------------------------------------------------------
        # Calculate Pages
        # ---------------------------------------------------------------------

        pages = ceil(
            result["total"] / limit
        )



        response = {

            "items": [

                {
                    "id": todo.id,
                    "title": todo.title,
                    "description": todo.description,
                    "completed": todo.completed,
                    "owner_id": todo.owner_id,
                    "created_at": todo.created_at.isoformat()
                }

                for todo in result["items"]

            ],


            "pagination": {

                "page": page,
                "limit": limit,
                "total": result["total"],
                "pages": pages

            }

        }



        # ---------------------------------------------------------------------
        # Store Cache
        # ---------------------------------------------------------------------

        cache_service.set(
            cache_key,
            response
        )


        return response



    # -------------------------------------------------------------------------
    # Get All Todos
    # -------------------------------------------------------------------------

    def get_all_todos(
            self
    ) -> list[Todo]:
        """
        Retrieve all todos.
        """

        return self.todo_repository.get_all_todos()



    # -------------------------------------------------------------------------
    # Update Todo
    # -------------------------------------------------------------------------

    def update_todo(
            self,
            todo: Todo
    ) -> Todo:
        """
        Update todo record.
        """

        updated_todo = self.todo_repository.update_todo(
            todo
        )


        self._invalidate_todo_cache(
            updated_todo.id,
            updated_todo.owner_id
        )


        return updated_todo



    # -------------------------------------------------------------------------
    # Delete Todo
    # -------------------------------------------------------------------------

    def delete_todo(
            self,
            todo_id: int
    ) -> None:
        """
        Delete todo record.
        """

        todo = self.todo_repository.get_todo_by_id(
            todo_id
        )


        if todo:

            self.todo_repository.delete_todo(
                todo_id
            )


            self._invalidate_todo_cache(
                todo.id,
                todo.owner_id
            )
