# -----------------------------------------------------------------------------
# Database Tests
# -----------------------------------------------------------------------------

from sqlalchemy import select

from app.models.user import User
from app.models.todo import Todo
from app.core.security import hash_password


def test_database_relationship_and_cascade(client):

    register = client.post(
        "/api/v1/auth/register",
        json={
            "email": "database@test.com",
            "password": "test12345"
        }
    )

    assert register.status_code == 201


def test_models_can_be_created_with_relationship():

    user = User(
        email="model@test.com",
        hashed_password=hash_password("test12345")
    )

    todo = Todo(
        title="Database Todo",
        owner=user
    )

    assert todo.owner is user

    assert todo in user.todos
