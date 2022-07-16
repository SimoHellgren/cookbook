import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from backend.app.db.base import Base


@pytest.fixture
def db() -> Session:
    engine = create_engine("sqlite://")
    Base.metadata.create_all(bind=engine)

    return Session(bind=engine)
