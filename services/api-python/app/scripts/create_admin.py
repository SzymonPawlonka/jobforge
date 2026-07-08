from sqlalchemy import select

from app.config import get_settings
from app.database import SessionLocal
from app.models import User
from app.security import hash_password


def main() -> None:
    settings = get_settings()
    email = settings.admin_email.lower()
    db = SessionLocal()
    try:
        user = db.scalar(select(User).where(User.email == email))
        if user:
            if user.role != "ADMIN":
                user.role = "ADMIN"
                db.commit()
                print(f"Zmieniono rolę {email} na ADMIN")
            else:
                print(f"Administrator {email} już istnieje")
            return
        db.add(User(email=email, password_hash=hash_password(settings.admin_password), role="ADMIN"))
        db.commit()
        print(f"Utworzono administratora {email}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
