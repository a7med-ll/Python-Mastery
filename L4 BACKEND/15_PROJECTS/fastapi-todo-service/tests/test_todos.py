# -----------------------------------------------------------------------------
# Todo API Tests
# -----------------------------------------------------------------------------

import uuid


# -----------------------------------------------------------------------------
# Helper Function
# -----------------------------------------------------------------------------

def create_test_user(client):
    """
    Create user and return authentication token.
    """

    email = f"todo_{uuid.uuid4()}@test.com"


    register_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": "test12345"
        }
    )


    assert register_response.status_code == 201



    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": email,
            "password": "test12345"
        }
    )


    assert login_response.status_code == 200


    login_data = login_response.json()


    return login_data["data"]["access_token"]



# -----------------------------------------------------------------------------
# Create Todo Test
# -----------------------------------------------------------------------------

def test_create_todo(client):

    token = create_test_user(client)


    response = client.post(
        "/api/v1/todos/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "Test Todo",
            "description": "Created from pytest"
        }
    )


    assert response.status_code == 200


    data = response.json()


    assert data["success"] is True

    assert data["data"]["title"] == "Test Todo"



# -----------------------------------------------------------------------------
# Get All Todos Test
# -----------------------------------------------------------------------------

def test_get_todos(client):

    token = create_test_user(client)


    client.post(
        "/api/v1/todos/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "title": "Todo Listing Test",
            "description": "Testing list"
        }
    )


    response = client.get(
        "/api/v1/todos/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )


    assert response.status_code == 200


    data = response.json()


    assert data["success"] is True


def test_todo_complete_lifecycle_and_cache_hit(client):

    token = create_test_user(client)

    headers = {"Authorization": f"Bearer {token}"}

    created = client.post(
        "/api/v1/todos/",
        headers=headers,
        json={"title": "Lifecycle", "description": "First value"}
    )

    todo_id = created.json()["data"]["id"]

    first_get = client.get(f"/api/v1/todos/{todo_id}", headers=headers)

    cached_get = client.get(f"/api/v1/todos/{todo_id}", headers=headers)

    assert first_get.status_code == 200

    assert cached_get.status_code == 200

    assert cached_get.json()["data"]["created_at"]

    updated = client.put(
        f"/api/v1/todos/{todo_id}",
        headers=headers,
        json={"title": "Updated", "completed": True}
    )

    assert updated.status_code == 200

    assert updated.json()["data"]["title"] == "Updated"

    assert updated.json()["data"]["completed"] is True

    deleted = client.delete(f"/api/v1/todos/{todo_id}", headers=headers)

    assert deleted.status_code == 200

    assert client.get(f"/api/v1/todos/{todo_id}", headers=headers).status_code == 404


def test_todo_ownership_is_enforced(client):

    first_token = create_test_user(client)

    second_token = create_test_user(client)

    created = client.post(
        "/api/v1/todos/",
        headers={"Authorization": f"Bearer {first_token}"},
        json={"title": "Private Todo"}
    )

    todo_id = created.json()["data"]["id"]

    second_headers = {"Authorization": f"Bearer {second_token}"}

    assert client.get(f"/api/v1/todos/{todo_id}", headers=second_headers).status_code == 403

    assert client.put(
        f"/api/v1/todos/{todo_id}",
        headers=second_headers,
        json={"completed": True}
    ).status_code == 403

    assert client.delete(f"/api/v1/todos/{todo_id}", headers=second_headers).status_code == 403


def test_todo_validation_and_pagination(client):

    token = create_test_user(client)

    headers = {"Authorization": f"Bearer {token}"}

    invalid_todo = client.post(
        "/api/v1/todos/",
        headers=headers,
        json={"title": ""}
    )

    invalid_page = client.get(
        "/api/v1/todos/?page=0",
        headers=headers
    )

    invalid_limit = client.get(
        "/api/v1/todos/?limit=101",
        headers=headers
    )

    assert invalid_todo.status_code == 422

    assert invalid_page.status_code == 400

    assert invalid_limit.status_code == 400
