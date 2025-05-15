import pytest

def test_task_crud_and_filters(client):

    client.post("/users/register", json={
        "first_name": "Task",
        "last_name": "Tester",
        "username": "taskuser",
        "password": "taskpass"
    })
    login = client.post("/users/login", data={"username": "taskuser", "password": "taskpass"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}


    cat = client.post("/categories/", json={"name": "TestCat"}, headers=headers).json()
    cat_id = cat["id"]


    response = client.post("/tasks/", json={
        "title": "Test Task",
        "description": "Desc",
        "category_id": cat_id,
        "priority": 2
    }, headers=headers)
    assert response.status_code == 200
    task = response.json()
    assert task["title"] == "Test Task"
    assert task["category"]["id"] == cat_id


    response = client.get("/tasks/", headers=headers)
    assert response.status_code == 200
    tasks = response.json()
    assert any(t["title"] == "Test Task" for t in tasks)


    response = client.get(f"/tasks/?category_id={cat_id}", headers=headers)
    assert response.status_code == 200
    assert all(t["category"]["id"] == cat_id for t in response.json())


    task_id = task["id"]
    response = client.put(f"/tasks/{task_id}", json={"title": "Updated Task"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Task"


    response = client.put(f"/tasks/{task_id}", json={"title": ""}, headers=headers)
    assert response.status_code != 200


    response = client.patch(f"/tasks/{task_id}/status", params={"status": "completed"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["status"] == "completed"
    assert response.json()["is_completed"] is True


    response = client.put(f"/tasks/0", json={"title": "Updated Task"}, headers=headers)
    assert response.status_code != 200


    response = client.delete(f"/tasks/{task_id}", headers=headers)
    assert response.status_code == 200


    response = client.delete(f"/tasks/0", headers=headers)
    assert response.status_code != 200


    response = client.get(f"/tasks/{task_id}", headers=headers)
    assert response.status_code == 404
