from threading import Thread

from fastapi.testclient import TestClient


def test_websocket_receives_running_and_completed(
    client: TestClient, auth_headers: dict[str, str], user_token: str
):
    job_id = client.post("/jobs", json={"name": "WebSocket test"}, headers=auth_headers).json()["id"]
    uploaded = client.post(
        f"/jobs/{job_id}/file",
        headers=auth_headers,
        files={"upload": ("sample.txt", b"one two\nthree", "text/plain")},
    )
    assert uploaded.status_code == 201

    response_holder = {}
    with client.websocket_connect(f"/ws/jobs/{job_id}?token={user_token}") as websocket:
        assert websocket.receive_json()["status"] == "CREATED"

        def run_job() -> None:
            response_holder["response"] = client.post(f"/jobs/{job_id}/run", headers=auth_headers)

        thread = Thread(target=run_job)
        thread.start()
        first = websocket.receive_json()
        second = websocket.receive_json()
        thread.join(timeout=5)

    assert [first["status"], second["status"]] == ["RUNNING", "COMPLETED"]
    assert response_holder["response"].status_code == 200
