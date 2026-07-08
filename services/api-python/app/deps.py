from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.grpc_client import GrpcAnalyzerClient
from app.models import Job, User
from app.security import decode_access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Nieprawidłowe dane uwierzytelniające",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        user_id = UUID(payload["sub"])
    except (ValueError, TypeError):
        raise credentials_error
    user = db.get(User, user_id)
    if user is None:
        raise credentials_error
    return user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wymagana rola ADMIN")
    return current_user


def get_owned_job(job_id: UUID, db: Session, current_user: User) -> Job:
    job = db.get(Job, job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Zadanie nie istnieje")
    if job.user_id != current_user.id:
        # 404 ogranicza ujawnianie istnienia cudzego zasobu.
        raise HTTPException(status_code=404, detail="Zadanie nie istnieje")
    return job


def get_analyzer_client() -> GrpcAnalyzerClient:
    return GrpcAnalyzerClient()
