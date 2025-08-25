from fastapi.testclient import TestClient
from main import app, history  # or whatever your app module is
from models import Expression

client = TestClient(app)

def test_basic_division():
    expr = Expression(expr="30 / 4")
    r = client.post("/calculate", json=expr.model_dump())
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 7.5) < 1e-9

def test_percent_subtraction():
    expr = Expression(expr="100 - 6%")
    r = client.post("/calculate", json=expr.model_dump())
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 94.0) < 1e-9

def test_standalone_percent():
    expr = Expression(expr="6%")
    r = client.post("/calculate", json=expr.model_dump())
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 0.06) < 1e-9

def test_invalid_expr_returns_ok_false():
    expr = Expression(expr="2**(3")
    r = client.post("/calculate", json=expr.model_dump())
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is False
    assert "error" in data and data["error"] != ""

# TODO Add more tests
# Tests for Delete history API
def test_delete_multiple_history():
    expr = Expression(expr="6%")
    for i in range(5):
        client.post("/calculate", json=expr.model_dump())
    r = client.delete("/history")
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert data["cleared"] is True
    assert len(history) == 0

def test_delete_history_after_invalid_post():
    expr = Expression(expr="2**(3")
    client.post("/calculate", json=expr.model_dump())
    r = client.delete("/history")
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert data["cleared"] is True

def test_delete_empty_history():
    r = client.delete("/history")
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert data["cleared"] is True

# Test for GET history API
def test_limit_history_with_empty_history():
    r = client.get("/history", params={"limit": "50"})
    assert r.status_code == 200
    data = r.json()
    assert len(history) == 0

def test_limit_history_with_data_less_than_limit():
    expr = Expression(expr="1+1")
    for i in range(5):
        client.post("/calculate", json=expr.model_dump())

    r = client.get("/history", params={"limit": "50"})
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 5

def test_limit_history_with_data_over_limit():
    expr = Expression(expr="1+1")
    for i in range(5):
        client.post("/calculate", json=expr.model_dump())

    r = client.get("/history", params={"limit": "4"})
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 4
    

def test_history_with_negative_limit():
    expr = Expression(expr="1+1")
    for i in range(5):
        client.post("/calculate", json=expr.model_dump())
    r = client.get("/history", params={"limit": "-5"})
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 0
    print(data)





