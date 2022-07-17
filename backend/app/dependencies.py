from typing import Optional
from backend.app.db.session import SessionLocal
from sqlalchemy.orm import Session
from flask import g


def get_db() -> Session:
    if "db" not in g:
        g.db = SessionLocal()

    return g.db


def close_db(e: Optional[BaseException] = None) -> None:
    db = g.pop("db", None)

    if db:
        db.close()
