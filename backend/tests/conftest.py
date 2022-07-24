import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.dependencies import get_db
from backend.app.db.base import Base


engine = create_engine("sqlite://", connect_args={"check_same_thread": False})
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


@pytest.fixture
def test_db():
    try:
        connection = engine.connect()
        connection.begin()
        db = Session(bind=connection)
        yield db

    finally:
        db.rollback()
        connection.close()


@pytest.fixture
def client(test_db):
    def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
