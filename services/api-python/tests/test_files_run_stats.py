from fastapi.testclient import TestClient
from sqlalchemy import select

from app.database import SessionLocal
from app.models import User
from app.security import hash_password


def _create_job(client: TestClient, headers: dict[str, str]) -> str:
    return client.post("/jobs", json={"name": "Analiza pliku"}, headers=headers).json()["id"]


def test_upload_download_run_and_stats(client: TestClient, auth_headers: dict[str, str]):
    job_id = _create_job(client, auth_headers)
    content = b"first line\nsecond line"
    uploaded = client.post(
        f"/jobs/{job_id}/file",
        headers=auth_headers,
        files={"upload": ("sample.txt", content, "text/plain")},
    )
    assert uploaded.status_code == 201
    assert uploaded.json()["size_bytes"] == len(content)

    downloaded = client.get(f"/jobs/{job_id}/file", headers=auth_headers)
    assert downloaded.status_code == 200
    assert downloaded.content == content

    run = client.post(f"/jobs/{job_id}/run", headers=auth_headers)
    assert run.status_code == 200
    assert run.json()["status"] == "COMPLETED"
    assert run.json()["result"]["word_count"] == 4

    stats = client.get("/stats/me", headers=auth_headers)
    assert stats.status_code == 200
    assert stats.json()["total_requests"] >= 4


def test_run_without_file_fails(client: TestClient, auth_headers: dict[str, str]):
    job_id = _create_job(client, auth_headers)
    response = client.post(f"/jobs/{job_id}/run", headers=auth_headers)
    assert response.status_code == 409


def test_file_validation(client: TestClient, auth_headers: dict[str, str]):
    job_id = _create_job(client, auth_headers)
    invalid = client.post(
        f"/jobs/{job_id}/file",
        headers=auth_headers,
        files={"upload": ("malware.exe", b"x", "application/octet-stream")},
    )
    assert invalid.status_code == 415


def test_admin_stats_requires_admin(client: TestClient, auth_headers: dict[str, str]):
    assert client.get("/stats/admin", headers=auth_headers).status_code == 403

    db = SessionLocal()
    admin = User(email="admin@example.com", password_hash=hash_password("AdminPass123!"), role="ADMIN")
    db.add(admin)
    db.commit()
    db.close()
    token = client.post("/auth/login", data={"username": "admin@example.com", "password": "AdminPass123!"}).json()["access_token"]
    response = client.get("/stats/admin", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["users"] >= 2
