from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.concurrency import run_in_threadpool
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.database import get_db
from app.deps import get_analyzer_client, get_current_user, get_owned_job
from app.grpc_client import AnalyzerUnavailableError, GrpcAnalyzerClient
from app.models import Job, User
from app.schemas import JobCreate, JobRead, JobUpdate
from app.websocket_manager import manager

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("", response_model=JobRead, status_code=status.HTTP_201_CREATED)
def create_job(payload: JobCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> Job:
    job = Job(user_id=current_user.id, name=payload.name.strip(), status="CREATED")
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@router.get("", response_model=list[JobRead])
def list_jobs(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> list[Job]:
    query = (
        select(Job)
        .options(selectinload(Job.stored_file))
        .where(Job.user_id == current_user.id)
        .order_by(Job.created_at.desc())
    )
    return list(db.scalars(query).all())


@router.get("/{job_id}", response_model=JobRead)
def read_job(job_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> Job:
    return get_owned_job(job_id, db, current_user)


@router.patch("/{job_id}", response_model=JobRead)
def update_job(payload: JobUpdate, job_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> Job:
    job = get_owned_job(job_id, db, current_user)
    if job.status == "RUNNING":
        raise HTTPException(status_code=409, detail="Nie można modyfikować zadania w trakcie analizy")
    job.name = payload.name.strip()
    db.commit()
    db.refresh(job)
    return job


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(job_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> None:
    job = get_owned_job(job_id, db, current_user)
    if job.status == "RUNNING":
        raise HTTPException(status_code=409, detail="Nie można usunąć zadania w trakcie analizy")
    db.delete(job)
    db.commit()


@router.post("/{job_id}/run", response_model=JobRead)
async def run_job(
    job_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    analyzer: GrpcAnalyzerClient = Depends(get_analyzer_client),
) -> Job:
    job = get_owned_job(job_id, db, current_user)
    if job.status == "RUNNING":
        raise HTTPException(status_code=409, detail="Zadanie jest już uruchomione")
    if job.stored_file is None:
        raise HTTPException(status_code=409, detail="Najpierw prześlij plik")

    job.status = "RUNNING"
    job.result = None
    job.error_message = None
    db.commit()
    await manager.broadcast(job.id, {"job_id": str(job.id), "status": "RUNNING"})

    try:
        result = await run_in_threadpool(analyzer.analyze, job.stored_file.filename, job.stored_file.data)
    except AnalyzerUnavailableError as exc:
        job.status = "FAILED"
        job.error_message = str(exc)[:2000]
        db.commit()
        db.refresh(job)
        await manager.broadcast(
            job.id,
            {"job_id": str(job.id), "status": "FAILED", "error": job.error_message},
        )
        return job
    except Exception as exc:
        job.status = "FAILED"
        job.error_message = f"Nieoczekiwany błąd analizatora: {exc}"[:2000]
        db.commit()
        db.refresh(job)
        await manager.broadcast(
            job.id,
            {"job_id": str(job.id), "status": "FAILED", "error": job.error_message},
        )
        return job

    job.status = "COMPLETED"
    job.result = result.as_dict()
    job.error_message = None
    db.commit()
    db.refresh(job)
    await manager.broadcast(
        job.id,
        {"job_id": str(job.id), "status": "COMPLETED", "result": job.result},
    )
    return job
