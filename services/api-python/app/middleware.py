import logging
import time
from uuid import UUID

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.database import SessionLocal
from app.models import ApiRequestLog
from app.security import decode_access_token

logger = logging.getLogger(__name__)


class ApiRequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):  # type: ignore[no-untyped-def]
        started = time.perf_counter()
        status_code = 500
        try:
            response = await call_next(request)
            status_code = response.status_code
            return response
        finally:
            duration_ms = (time.perf_counter() - started) * 1000
            self._persist_log(request, status_code, duration_ms)

    @staticmethod
    def _persist_log(request: Request, status_code: int, duration_ms: float) -> None:
        user_id: UUID | None = None
        authorization = request.headers.get("authorization", "")
        if authorization.lower().startswith("bearer "):
            token = authorization.split(" ", 1)[1]
            try:
                user_id = UUID(decode_access_token(token)["sub"])
            except (ValueError, TypeError):
                user_id = None
        db = SessionLocal()
        try:
            db.add(
                ApiRequestLog(
                    user_id=user_id,
                    method=request.method,
                    path=request.url.path,
                    status_code=status_code,
                    duration_ms=round(duration_ms, 3),
                )
            )
            db.commit()
        except Exception:
            db.rollback()
            logger.exception("Nie udało się zapisać logu API")
        finally:
            db.close()
