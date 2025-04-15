import pytest

def test_category_crud(client):

    client.post("/users/register", json={
        "first_name": "Cat",
        "last_name": "Owner",
        "username": "catuser",
        "password": "catpass"
    })
    login = client.post("/users/login", data={"username": "catuser", "password": "catpass"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}


    response = client.post("/categories/", json={"name": "Work"}, headers=headers)
    assert response.status_code == 200
    cat = response.json()
    assert cat["name"] == "Work"


    response = client.get("/categories/", headers=headers)
    assert response.status_code == 200
    cats = response.json()
    assert any(c["name"] == "Work" for c in cats)


    cat_id = cat["id"]
    response = client.put(f"/categories/{cat_id}", json={"name": "Personal"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Personal"


    response = client.get(f"/categories/{cat_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Personal"


    response = client.delete(f"/categories/{cat_id}", headers=headers)
    assert response.status_code == 200

    response = client.get(f"/categories/{cat_id}", headers=headers)
    assert response.status_code == 404
