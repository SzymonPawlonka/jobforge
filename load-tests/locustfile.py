import os
import random
import string

from locust import HttpUser, between, task


class JobForgeUser(HttpUser):
    wait_time = between(0.5, 2.0)

    def on_start(self):
        suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
        email = f"locust-{suffix}@example.com"
        password = "LoadTest123!"
        self.client.post("/auth/register", json={"email": email, "password": password}, name="POST /auth/register")
        response = self.client.post(
            "/auth/login",
            data={"username": email, "password": password},
            name="POST /auth/login",
        )
        response.raise_for_status()
        self.headers = {"Authorization": f"Bearer {response.json()['access_token']}"}
        created = self.client.post("/jobs", json={"name": "Locust initial job"}, headers=self.headers, name="POST /jobs")
        created.raise_for_status()
        self.job_id = created.json()["id"]

    @task(5)
    def list_jobs(self):
        self.client.get("/jobs", headers=self.headers, name="GET /jobs")

    @task(3)
    def read_job(self):
        self.client.get(f"/jobs/{self.job_id}", headers=self.headers, name="GET /jobs/{id}")

    @task(1)
    def create_job(self):
        self.client.post("/jobs", json={"name": "Locust generated job"}, headers=self.headers, name="POST /jobs")
