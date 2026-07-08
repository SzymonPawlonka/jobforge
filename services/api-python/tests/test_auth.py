from fastapi.testclient import TestClient


def test_register_login_and_me(client: TestClient):
    response = client.post("/auth/register", json={"email": "alice@example.com", "password": "StrongPass123!"})
    assert response.status_code == 201
    assert response.json()["role"] == "USER"

    duplicate = client.post("/auth/register", json={"email": "alice@example.com", "password": "StrongPass123!"})
    assert duplicate.status_code == 409

    login = client.post("/auth/login", data={"username": "alice@example.com", "password": "StrongPass123!"})
    assert login.status_code == 200
    token = login.json()["access_token"]

    me = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["email"] == "alice@example.com"


def test_rejects_bad_password(client: TestClient):
    client.post("/auth/register", json={"email": "alice@example.com", "password": "StrongPass123!"})
    response = client.post("/auth/login", data={"username": "alice@example.com", "password": "wrong-password"})
    assert response.status_code == 401
