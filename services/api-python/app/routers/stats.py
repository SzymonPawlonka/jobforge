from fastapi import APIRouter, Depends
from sqlalchemy import case, desc, func, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user, require_admin
from app.models import ApiRequestLog, Job, StoredFile, User
from app.schemas import AdminStatsRead, StatsRead

router = APIRouter(prefix="/stats", tags=["stats"])


def _calculate_stats(db: Session, user_id=None) -> StatsRead:
    filters = []
    if user_id is not None:
        filters.append(ApiRequestLog.user_id == user_id)

    totals = db.execute(
        select(
            func.count(ApiRequestLog.id),
            func.coalesce(func.sum(case((ApiRequestLog.status_code.between(200, 399), 1), else_=0)), 0),
            func.coalesce(func.avg(ApiRequestLog.duration_ms), 0.0),
        ).where(*filters)
    ).one()
    total = int(totals[0] or 0)
    successful = int(totals[1] or 0)
    most_used = db.execute(
        select(ApiRequestLog.path, func.count(ApiRequestLog.id).label("uses"))
        .where(*filters)
        .group_by(ApiRequestLog.path)
        .order_by(desc("uses"), ApiRequestLog.path)
        .limit(1)
    ).first()
    return StatsRead(
        total_requests=total,
        successful_requests=successful,
        failed_requests=total - successful,
        average_duration_ms=round(float(totals[2] or 0.0), 3),
        most_used_endpoint=most_used[0] if most_used else None,
    )


@router.get("/me", response_model=StatsRead)
def my_stats(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> StatsRead:
    return _calculate_stats(db, current_user.id)


@router.get("/admin", response_model=AdminStatsRead)
def admin_stats(db: Session = Depends(get_db), _admin: User = Depends(require_admin)) -> AdminStatsRead:
    base = _calculate_stats(db)
    return AdminStatsRead(
        **base.model_dump(),
        users=db.scalar(select(func.count(User.id))) or 0,
        jobs=db.scalar(select(func.count(Job.id))) or 0,
        files=db.scalar(select(func.count(StoredFile.id))) or 0,
    )
