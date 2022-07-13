from backend.app.db.session import SessionLocal
from flask import g


def get_db():
    if "db" not in g:
        g.db = SessionLocal()

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db:
        db.close()
