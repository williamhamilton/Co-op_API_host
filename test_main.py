import pytest
from fastapi.testclient import TestClient
from main import app  

client = TestClient(app)
TOKEN = "coop-learner-2026"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

def test_read_dashboard():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_get_books_unauthorized():
    # This assumes AUTH_ENABLED is True by default
    response = client.get("/v1/books")
    assert response.status_code == 401

def test_get_books_authorized():
    response = client.get("/v1/books", headers=HEADERS)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_book():
    payload = {"id": 99, "title": "Test Book", "completed": False}
    response = client.post("/v1/books", json=payload, headers=HEADERS)
    assert response.status_code == 201
    assert response.json()["title"] == "Test Book"

def test_delete_book():
    response = client.delete("/v1/books/99", headers=HEADERS)
    assert response.status_code == 200