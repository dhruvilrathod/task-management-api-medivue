def test_soft_delete(client):
    res = client.delete("/api/v1/tasks/1")
    assert res.status_code == 204

    res = client.get("/api/v1/tasks/1")
    assert res.status_code == 404