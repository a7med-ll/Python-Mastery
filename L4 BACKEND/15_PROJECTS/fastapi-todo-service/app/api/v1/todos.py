# -----------------------------------------------------------------------------
# Todo API Routes
# -----------------------------------------------------------------------------

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.api.dependencies import (
    get_database_session,
    get_current_user
)

from app.core.exceptions import (
    not_found_exception,
    authorization_exception,
    bad_request_exception
)

from app.models.user import User
from app.models.todo import Todo

from app.schemas.todo_schema import (
    TodoCreate,
    TodoUpdate,
    TodoResponse,
    TodoPaginationResponse
)

from app.schemas.pagination_schema import PaginationMeta

from app.schemas.response_schema import ResponseSchema

from app.services.todo_service import TodoService


# -----------------------------------------------------------------------------
# Router Configuration
# -----------------------------------------------------------------------------

router = APIRouter(
    prefix="/todos",
    tags=["Todos"]
)


# -----------------------------------------------------------------------------
# Create Todo
# -----------------------------------------------------------------------------

@router.post(
    "/",
    response_model=ResponseSchema[TodoResponse]
)
def create_todo(
        todo_data: TodoCreate,
        database: Session = Depends(get_database_session),
        current_user: User = Depends(get_current_user)
):
    """
    Create todo for authenticated user.
    """


    service = TodoService(
        database
    )


    todo = Todo(
        title=todo_data.title,
        description=todo_data.description,
        owner_id=current_user.id
    )


    created_todo = service.create_todo(
        todo
    )


    return ResponseSchema(
        success=True,
        message="Todo created successfully",
        data=TodoResponse.model_validate(
            created_todo
        )
    )



# -----------------------------------------------------------------------------
# Get Todo By ID
# -----------------------------------------------------------------------------

@router.get(
    "/{todo_id}",
    response_model=ResponseSchema[TodoResponse]
)
def get_todo(
        todo_id: int,
        database: Session = Depends(get_database_session),
        current_user: User = Depends(get_current_user)
):
    """
    Retrieve todo by ID.
    """


    service = TodoService(
        database
    )


    todo = service.get_todo_by_id(
        todo_id
    )


    if not todo:

        raise not_found_exception(
            "Todo not found"
        )


    if todo.owner_id != current_user.id:

        raise authorization_exception(
            "Not authorized"
        )


    return ResponseSchema(
        success=True,
        message="Todo retrieved successfully",
        data=TodoResponse.model_validate(
            todo
        )
    )



# -----------------------------------------------------------------------------
# Get All Todos With Pagination
# -----------------------------------------------------------------------------

@router.get(
    "/",
    response_model=ResponseSchema[TodoPaginationResponse]
)
def get_all_todos(
        page: int = 1,
        limit: int = 10,
        database: Session = Depends(get_database_session),
        current_user: User = Depends(get_current_user)
):
    """
    Retrieve authenticated user todos with pagination.
    """


    if page < 1:

        raise bad_request_exception(
            "Page must be greater than zero"
        )


    if limit < 1 or limit > 100:

        raise bad_request_exception(
            "Limit must be between 1 and 100"
        )


    service = TodoService(
        database
    )


    todos = service.get_user_todos(
        current_user.id,
        page,
        limit
    )


    return ResponseSchema(
        success=True,
        message="Todos retrieved successfully",
        data=TodoPaginationResponse(
            items=[
                TodoResponse.model_validate(todo)
                for todo in todos["items"]
            ],
            pagination=PaginationMeta(
                **todos["pagination"]
            )
        )
    )



# -----------------------------------------------------------------------------
# Update Todo
# -----------------------------------------------------------------------------

@router.put(
    "/{todo_id}",
    response_model=ResponseSchema[TodoResponse]
)
def update_todo(
        todo_id: int,
        todo_data: TodoUpdate,
        database: Session = Depends(get_database_session),
        current_user: User = Depends(get_current_user)
):
    """
    Update todo record.
    """


    service = TodoService(
        database
    )


    todo = service.get_todo_by_id(
        todo_id
    )


    if not todo:

        raise not_found_exception(
            "Todo not found"
        )


    if todo.owner_id != current_user.id:

        raise authorization_exception(
            "Not authorized"
        )


    if todo_data.title is not None:

        todo.title = todo_data.title


    if todo_data.description is not None:

        todo.description = todo_data.description


    if todo_data.completed is not None:

        todo.completed = todo_data.completed



    updated_todo = service.update_todo(
        todo
    )


    return ResponseSchema(
        success=True,
        message="Todo updated successfully",
        data=TodoResponse.model_validate(
            updated_todo
        )
    )



# -----------------------------------------------------------------------------
# Delete Todo
# -----------------------------------------------------------------------------

@router.delete(
    "/{todo_id}",
    response_model=ResponseSchema[dict]
)
def delete_todo(
        todo_id: int,
        database: Session = Depends(get_database_session),
        current_user: User = Depends(get_current_user)
):
    """
    Delete todo record.
    """


    service = TodoService(
        database
    )


    todo = service.get_todo_by_id(
        todo_id
    )


    if not todo:

        raise not_found_exception(
            "Todo not found"
        )


    if todo.owner_id != current_user.id:

        raise authorization_exception(
            "Not authorized"
        )


    service.delete_todo(
        todo_id
    )


    return ResponseSchema(
        success=True,
        message="Todo deleted successfully",
        data={}
    )