"""This file exists so that alembic's autogenerate works properly (otherwise it doesn't pick up the models)"""
from backend.app.db.base_class import Base  # noqa: F401
from backend.app import models  # noqa: F401
