from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    email: EmailStr
    role: Literal["USER", "ADMIN"]
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class FileMetadata(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    filename: str
    content_type: str
    size_bytes: int
    created_at: datetime


class JobCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100)


class JobUpdate(BaseModel):
    name: str = Field(min_length=3, max_length=100)


class JobRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    user_id: UUID
    name: str
    status: Literal["CREATED", "RUNNING", "COMPLETED", "FAILED"]
    result: dict[str, Any] | None
    error_message: str | None
    stored_file: FileMetadata | None
    created_at: datetime
    updated_at: datetime


class StatsRead(BaseModel):
    total_requests: int
    successful_requests: int
    failed_requests: int
    average_duration_ms: float
    most_used_endpoint: str | None


class AdminStatsRead(StatsRead):
    users: int
    jobs: int
    files: int


class HealthRead(BaseModel):
    status: Literal["ok"] = "ok"
    service: str = "jobforge-api"
    version: str
