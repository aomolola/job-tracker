
from fastapi.testclient import TestClient
from auth.security import hash_password, verify_password

from main import app


client = TestClient(app)


def test_password_hashing():
    password = "secure-password"

    hashed_password = hash_password(password)

    assert hashed_password != password
    assert verify_password(password, hashed_password)
    assert not verify_password("wrong-password", hashed_password)


def test_register_user():
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "new-user@example.com",
            "password": "secure-password"
        }
    )

    assert response.status_code == 201

    data = response.json()
    assert data["email"] == "new-user@example.com"
    assert "id" in data
    assert "hashed_password" not in data
