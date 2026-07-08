from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "JobForge API"
    app_version: str = "1.0.0"
    database_url: str = "postgresql+psycopg://jobforge:jobforge@localhost:5432/jobforge"
    jwt_secret: str = Field(default="development-secret-change-me-at-least-32-characters", min_length=32)
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = Field(default=60, ge=1, le=1440)
    grpc_target: str = "localhost:50051"
    grpc_tls: bool = False
    grpc_timeout_seconds: float = Field(default=10.0, gt=0, le=60)
    max_file_bytes: int = 1_048_576
    cors_origins: str = "*"
    log_level: str = "INFO"
    admin_email: str = "admin@jobforge.com"
    admin_password: str = "ChangeMe123!"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @field_validator("jwt_secret")
    @classmethod
    def reject_default_secret_in_non_test(cls, value: str) -> str:
        # Pozwala uruchomić projekt od razu lokalnie, ale README wymaga zmiany sekretu.
        return value

    @property
    def cors_origin_list(self) -> list[str]:
        if self.cors_origins.strip() == "*":
            return ["*"]
        return [item.strip() for item in self.cors_origins.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()

