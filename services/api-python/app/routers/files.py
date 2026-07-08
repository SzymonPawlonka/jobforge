from pathlib import Path
from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile, status
from sqlalchemy.orm import Session

from app.config import get_settings
from app.database import get_db
from app.deps import get_current_user, get_owned_job
from app.models import StoredFile, User
from app.schemas import FileMetadata

router = APIRouter(prefix="/jobs", tags=["files"])
ALLOWED_EXTENSIONS = {".txt", ".csv", ".json"}


@router.post("/{job_id}/file", response_model=FileMetadata, status_code=status.HTTP_201_CREATED)
async def upload_file(
    job_id: UUID,
    upload: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> StoredFile:
    settings = get_settings()
    job = get_owned_job(job_id, db, current_user)
    if job.status == "RUNNING":
        raise HTTPException(status_code=409, detail="Nie można zmieniać pliku w trakcie analizy")
    if job.stored_file is not None:
        raise HTTPException(status_code=409, detail="Zadanie ma już przypisany plik")

    filename = Path(upload.filename or "").name
    extension = Path(filename).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=415, detail="Dozwolone rozszerzenia: .txt, .csv, .json")

    content = await upload.read(settings.max_file_bytes + 1)
    if len(content) > settings.max_file_bytes:
        raise HTTPException(status_code=413, detail="Plik przekracza limit 1 MiB")

    stored_file = StoredFile(
        job_id=job.id,
        filename=filename,
        content_type=upload.content_type or "application/octet-stream",
        size_bytes=len(content),
        data=content,
    )
    job.status = "CREATED"
    job.result = None
    job.error_message = None
    db.add(stored_file)
    db.commit()
    db.refresh(stored_file)
    return stored_file


@router.get("/{job_id}/file")
def download_file(job_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> Response:
    job = get_owned_job(job_id, db, current_user)
    if job.stored_file is None:
        raise HTTPException(status_code=404, detail="Plik nie istnieje")
    file = job.stored_file
    safe_filename = file.filename.replace('"', "")
    return Response(
        content=file.data,
        media_type=file.content_type,
        headers={"Content-Disposition": f'attachment; filename="{safe_filename}"'},
    )


@router.delete("/{job_id}/file", status_code=status.HTTP_204_NO_CONTENT)
def delete_file(job_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> None:
    job = get_owned_job(job_id, db, current_user)
    if job.status == "RUNNING":
        raise HTTPException(status_code=409, detail="Nie można usunąć pliku w trakcie analizy")
    if job.stored_file is None:
        raise HTTPException(status_code=404, detail="Plik nie istnieje")
    db.delete(job.stored_file)
    job.status = "CREATED"
    job.result = None
    job.error_message = None
    db.commit()
