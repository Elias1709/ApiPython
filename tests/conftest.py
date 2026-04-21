import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def auth_headers():
    # Genera un token real usando el endpoint /token
    response = client.post("/token", data={
        "username": "admin",
        "password": "1234"
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def test_client():
    return client
