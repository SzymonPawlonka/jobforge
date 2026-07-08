import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.middleware import ApiRequestLoggingMiddleware
from app.routers import auth, files, jobs, stats, users, websocket
from app.schemas import HealthRead

settings = get_settings()
logging.basicConfig(level=settings.log_level)

app = FastAPI(
    title="JobForge API",
    version=settings.app_version,
    description="REST API do zlecania, przetwarzania i monitorowania zadań plikowych.",
)

app.add_middleware(ApiRequestLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=settings.cors_origin_list != ["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(jobs.router)
app.include_router(files.router)
app.include_router(stats.router)
app.include_router(websocket.router)


@app.get("/health", response_model=HealthRead, tags=["system"])
def health() -> HealthRead:
    return HealthRead(version=settings.app_version)
