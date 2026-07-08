import os

os.environ["DATABASE_URL"] = "sqlite://"
os.environ["JWT_SECRET"] = "test-secret-that-is-definitely-longer-than-32-characters"
os.environ["GRPC_TARGET"] = "unused:50051"

import pytest
from fastapi.testclient import TestClient

from app.database import Base, engine
from app.deps import get_analyzer_client
from app.grpc_client import AnalysisResult
from app.main import app


class FakeAnalyzer:
    def analyze(self, filename: str, content: bytes) -> AnalysisResult:
        import hashlib
        text = content.decode("utf-8", errors="replace")
        return AnalysisResult(
            size_bytes=len(content),
            character_count=len(text),
            word_count=len(text.split()),
            line_count=0 if not content else content.count(b"\n") + 1,
            sha256=hashlib.sha256(content).hexdigest(),
        )


@pytest.fixture(autouse=True)
def clean_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    app.dependency_overrides[get_analyzer_client] = lambda: FakeAnalyzer()
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def user_token(client: TestClient) -> str:
    client.post("/auth/register", json={"email": "user@example.com", "password": "StrongPass123!"})
    response = client.post("/auth/login", data={"username": "user@example.com", "password": "StrongPass123!"})
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(user_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {user_token}"}
