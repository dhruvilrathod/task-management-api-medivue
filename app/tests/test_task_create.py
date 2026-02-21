def test_create_task_success(client):
    payload = {
        "title": "Test task",
        "priority": 3,
        "due_date": "2026-03-01",
        "tags": ["Work", "Urgent"],
    }

    res = client.post("/api/v1/tasks", json=payload)

    assert res.status_code == 201
    data = res.json()
    assert data["title"] == "Test task"
    assert set(data["tags"]) == {"work", "urgent"}


def test_create_task_validation_error(client):
    payload = {
        "title": "",
        "priority": 10,
        "due_date": "2020-01-01",
    }

    res = client.post("/api/v1/tasks", json=payload)

    assert res.status_code == 422
    body = res.json()
    assert body["error"] == "Validation Failed"