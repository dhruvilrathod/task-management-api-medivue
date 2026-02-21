def test_partial_update(client):
    payload = {"title": "Updated title"}

    res = client.patch("/api/v1/tasks/1", json=payload)
    assert res.status_code == 200
    assert res.json()["title"] == "Updated title"


def test_patch_invalid_date(client):
    res = client.patch(
        "/api/v1/tasks/1",
        json={"due_date": "2020-01-01"},
    )
    assert res.status_code == 422