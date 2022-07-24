from typing import Generator
from backend.app.db.session import SessionLocal
from sqlalchemy.orm import Session


def get_db() -> Generator[Session, None, None]:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
