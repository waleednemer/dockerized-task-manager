def create(client, **kw):
    body = {"title": "مهمة", **kw}
    return client.post("/api/tasks", json=body)


def test_list_empty(client):
    res = client.get("/api/tasks")
    assert res.status_code == 200 and res.get_json() == []


def test_create_and_list(client):
    res = create(client, title="اختبار", priority="high", due_date="2026-12-01")
    assert res.status_code == 201
    task = res.get_json()
    assert task["title"] == "اختبار"
    assert task["status"] == "todo"
    assert task["priority"] == "high"
    assert task["due_date"] == "2026-12-01"
    assert [t["id"] for t in client.get("/api/tasks").get_json()] == [task["id"]]


def test_create_without_title_returns_400(client):
    res = client.post("/api/tasks", json={"priority": "low"})
    assert res.status_code == 400 and "error" in res.get_json()


def test_create_with_invalid_status_returns_400(client):
    assert create(client, status="bad").status_code == 400


def test_update_status(client):
    tid = create(client).get_json()["id"]
    res = client.put(f"/api/tasks/{tid}", json={"status": "doing"})
    assert res.status_code == 200 and res.get_json()["status"] == "doing"


def test_update_missing_task_returns_404(client):
    assert client.put("/api/tasks/9999", json={"status": "done"}).status_code == 404


def test_update_empty_body_returns_400(client):
    tid = create(client).get_json()["id"]
    assert client.put(f"/api/tasks/{tid}", json={}).status_code == 400


def test_delete_then_404(client):
    tid = create(client).get_json()["id"]
    assert client.delete(f"/api/tasks/{tid}").status_code == 204
    assert client.delete(f"/api/tasks/{tid}").status_code == 404


def test_done_tasks_listed_last(client):
    first = create(client, title="الأولى").get_json()["id"]
    create(client, title="الثانية")
    client.put(f"/api/tasks/{first}", json={"status": "done"})
    titles = [t["title"] for t in client.get("/api/tasks").get_json()]
    assert titles == ["الثانية", "الأولى"]
