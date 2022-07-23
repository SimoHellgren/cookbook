import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.dependencies import get_db
from backend.app.db.base import Base


def get_test_db() -> Session:
    engine = create_engine("sqlite://")
    Base.metadata.create_all(bind=engine)

    test_db = Session(bind=engine)

    try:
        yield test_db

    finally:
        test_db.close()


@pytest.fixture
def test_db():
    yield from get_test_db()


@pytest.fixture(scope="session", autouse=True)
def db_for_api():
    app.dependency_overrides[get_db] = get_test_db

    yield


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c
