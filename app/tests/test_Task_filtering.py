def test_filter_by_tag(client):
    res = client.get("/api/v1/tasks?tags=urgent")
    assert res.status_code == 200

    data = res.json()
    for task in data["items"]:
        assert "urgent" in task["tags"]


def test_filter_priority(client):
    res = client.get("/api/v1/tasks?priority=3")
    assert res.status_code == 200