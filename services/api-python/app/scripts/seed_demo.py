from sqlalchemy import select

from app.database import SessionLocal
from app.models import Job, User
from app.security import hash_password


def main() -> None:
    db = SessionLocal()
    try:
        email = "demo@jobforge.local"
        user = db.scalar(select(User).where(User.email == email))
        if user is None:
            user = User(email=email, password_hash=hash_password("DemoPass123!"), role="USER")
            db.add(user)
            db.flush()
        existing = db.scalar(select(Job).where(Job.user_id == user.id))
        if existing is None:
            db.add_all([
                Job(user_id=user.id, name="Analiza raportu", status="CREATED"),
                Job(user_id=user.id, name="Analiza danych CSV", status="CREATED"),
            ])
        db.commit()
        print("Dane demonstracyjne gotowe: demo@jobforge.local / DemoPass123!")
    finally:
        db.close()


if __name__ == "__main__":
    main()
