from fastapi.testclient import TestClient


def test_jobs_crud(client: TestClient, auth_headers: dict[str, str]):
    created = client.post("/jobs", json={"name": "Analiza raportu"}, headers=auth_headers)
    assert created.status_code == 201
    job_id = created.json()["id"]

    listed = client.get("/jobs", headers=auth_headers)
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    updated = client.patch(f"/jobs/{job_id}", json={"name": "Nowa nazwa"}, headers=auth_headers)
    assert updated.status_code == 200
    assert updated.json()["name"] == "Nowa nazwa"

    deleted = client.delete(f"/jobs/{job_id}", headers=auth_headers)
    assert deleted.status_code == 204
    assert client.get(f"/jobs/{job_id}", headers=auth_headers).status_code == 404


def test_cannot_access_another_users_job(client: TestClient, auth_headers: dict[str, str]):
    job_id = client.post("/jobs", json={"name": "Prywatne zadanie"}, headers=auth_headers).json()["id"]

    client.post("/auth/register", json={"email": "other@example.com", "password": "StrongPass123!"})
    other_token = client.post(
        "/auth/login", data={"username": "other@example.com", "password": "StrongPass123!"}
    ).json()["access_token"]
    response = client.get(f"/jobs/{job_id}", headers={"Authorization": f"Bearer {other_token}"})
    assert response.status_code == 404
