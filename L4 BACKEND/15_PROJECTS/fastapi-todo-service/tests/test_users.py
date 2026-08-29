# -----------------------------------------------------------------------------
# User API Tests
# -----------------------------------------------------------------------------

import uuid


# -----------------------------------------------------------------------------
# Get Current User Profile
# -----------------------------------------------------------------------------

def test_get_current_user(client):

    email = f"user_profile_{uuid.uuid4()}@test.com"


    register = client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": "test12345"
        }
    )

    assert register.status_code == 201


    login = client.post(
        "/api/v1/auth/login",
        data={
            "username": email,
            "password": "test12345"
        }
    )


    assert login.status_code == 200


    token = login.json()["data"]["access_token"]


    response = client.get(
        "/api/v1/users/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )


    assert response.status_code == 200


    data = response.json()


    assert data["success"] is True

    assert data["data"]["email"] == email



# -----------------------------------------------------------------------------
# Get User By ID
# -----------------------------------------------------------------------------

def test_get_user_by_id(client):

    email = f"get_user_{uuid.uuid4()}@test.com"


    register = client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": "test12345"
        }
    )


    assert register.status_code == 201



    login = client.post(
        "/api/v1/auth/login",
        data={
            "username": email,
            "password": "test12345"
        }
    )


    assert login.status_code == 200


    token = login.json()["data"]["access_token"]



    profile = client.get(
        "/api/v1/users/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )


    assert profile.status_code == 200


    user_id = profile.json()["data"]["id"]



    response = client.get(
        f"/api/v1/users/{user_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )


    assert response.status_code == 200


    assert response.json()["data"]["id"] == user_id



# -----------------------------------------------------------------------------
# Update User
# -----------------------------------------------------------------------------

def test_update_user(client):

    email = f"update_user_{uuid.uuid4()}@test.com"


    register = client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": "test12345"
        }
    )


    assert register.status_code == 201



    login = client.post(
        "/api/v1/auth/login",
        data={
            "username": email,
            "password": "test12345"
        }
    )


    assert login.status_code == 200


    token = login.json()["data"]["access_token"]



    profile = client.get(
        "/api/v1/users/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )


    assert profile.status_code == 200


    user_id = profile.json()["data"]["id"]



    response = client.put(
        f"/api/v1/users/{user_id}",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "email": f"updated_{uuid.uuid4()}@test.com"
        }
    )


    assert response.status_code == 200


    data = response.json()


    assert data["success"] is True

    assert data["data"]["email"].startswith("updated_")



# -----------------------------------------------------------------------------
# Delete User
# -----------------------------------------------------------------------------

def test_delete_user(client):

    email = f"delete_user_{uuid.uuid4()}@test.com"


    register = client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": "test12345"
        }
    )


    assert register.status_code == 201



    login = client.post(
        "/api/v1/auth/login",
        data={
            "username": email,
            "password": "test12345"
        }
    )


    assert login.status_code == 200


    token = login.json()["data"]["access_token"]



    profile = client.get(
        "/api/v1/users/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )


    assert profile.status_code == 200


    user_id = profile.json()["data"]["id"]



    response = client.delete(
        f"/api/v1/users/{user_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )


    assert response.status_code == 200


    data = response.json()


    assert data["success"] is True
