from uuid import UUID

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Job, User
from app.security import decode_access_token
from app.websocket_manager import manager

router = APIRouter(tags=["websocket"])


@router.websocket("/ws/jobs/{job_id}")
async def job_status_websocket(websocket: WebSocket, job_id: UUID, token: str) -> None:
    db: Session = SessionLocal()
    try:
        try:
            payload = decode_access_token(token)
            user_id = UUID(payload["sub"])
        except (ValueError, TypeError):
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Nieprawidłowy token")
            return
        user = db.get(User, user_id)
        job = db.get(Job, job_id)
        if user is None or job is None or job.user_id != user.id:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Brak dostępu")
            return

        await manager.connect(job_id, websocket)
        initial = {"job_id": str(job.id), "status": job.status}
        if job.result is not None:
            initial["result"] = job.result
        if job.error_message is not None:
            initial["error"] = job.error_message
        await websocket.send_json(initial)

        while True:
            # Klient może wysyłać dowolny tekst jako keepalive; statusy płyną z serwera.
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(job_id, websocket)
    finally:
        db.close()
