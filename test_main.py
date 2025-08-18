from fastapi.testclient import TestClient
from main import app  # or whatever your app module is

client = TestClient(app)

def test_basic_division():
    r = client.post("/calculate", params={"expr": "30/4"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 7.5) < 1e-9

def test_percent_subtraction():
    r = client.post("/calculate", params={"expr": "100 - 6%"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 94.0) < 1e-9

def test_standalone_percent():
    r = client.post("/calculate", params={"expr": "6%"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 0.06) < 1e-9

def test_invalid_expr_returns_ok_false():
    r = client.post("/calculate", params={"expr": "2**(3"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is False
    assert "error" in data and data["error"] != ""

# TODO Add more tests
# Tests for Delete history API
def test_delete_filled_history():
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

def test_delete_history_after_invalid_post():
    client.post("/calculate", params={"expr": "2**(3"})
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
    assert len(data) == 0

def test_limit_history_with_data_less_than_limit():
    for i in range(5):
        client.post("/calculate", params={"expr": "1+1"})

    r = client.get("/history", params={"limit": "50"})
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 5

def test_limit_history_with_data_over_limit():
    for i in range(5):
        client.post("/calculate", params={"expr": "1+1"})

    r = client.get("/history", params={"limit": "4"})
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 4

def test_history_with_negative_limit():
    for i in range(5):
        client.post("/calculate", params={"expr": "1+1"})
    r = client.get("/history", params={"limit": "-5"})
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 0





