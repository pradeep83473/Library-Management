from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    response = client.post("/register", json={"name": "Test User", "email": "test@example.com", "password": "testpass", "role": "user"})
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

def test_login():
    response = client.post("/login", json={"email": "test@example.com", "password": "testpass"})
    assert response.status_code == 200
    assert "access_token" in response.json()