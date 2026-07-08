from collections import defaultdict
from uuid import UUID

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self) -> None:
        self._connections: dict[UUID, set[WebSocket]] = defaultdict(set)

    async def connect(self, job_id: UUID, websocket: WebSocket) -> None:
        await websocket.accept()
        self._connections[job_id].add(websocket)

    def disconnect(self, job_id: UUID, websocket: WebSocket) -> None:
        connections = self._connections.get(job_id)
        if not connections:
            return
        connections.discard(websocket)
        if not connections:
            self._connections.pop(job_id, None)

    async def broadcast(self, job_id: UUID, payload: dict) -> None:
        dead: list[WebSocket] = []
        for websocket in list(self._connections.get(job_id, set())):
            try:
                await websocket.send_json(payload)
            except Exception:
                dead.append(websocket)
        for websocket in dead:
            self.disconnect(job_id, websocket)


manager = ConnectionManager()
