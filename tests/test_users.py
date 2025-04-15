import pytest

def test_register_and_login(client):

    response = client.post("/users/register", json={
        "first_name": "Test",
        "last_name": "User",
        "username": "testuser",
        "password": "testpass123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"


    response = client.post("/users/login", data={
        "username": "testuser",
        "password": "testpass123"
    })
    assert response.status_code == 200
    tokens = response.json()
    assert "access_token" in tokens
    assert tokens["token_type"] == "bearer"


    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    response = client.post("/users/change-password", params={
        "old_password": "testpass123",
        "new_password": "newpass456"
    }, headers=headers)
    assert response.status_code == 200

 со старым паролем должен провалиться
    response = client.post("/users/login", data={
        "username": "testuser",
        "password": "testpass123"
    })
    assert response.status_code == 400

 с новым паролем
    response = client.post("/users/login", data={
        "username": "testuser",
        "password": "newpass456"
    })
    assert response.status_code == 200
    new_tokens = response.json()
    assert "access_token" in new_tokens


    headers = {"Authorization": f"Bearer {new_tokens['access_token']}"}
    response = client.post("/users/refresh-token", headers=headers)
    assert response.status_code == 200
    assert "access_token" in response.json()
