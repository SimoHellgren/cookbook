import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import database_exists, create_database, drop_database
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.dependencies import get_db
from backend.app.db.base import Base
from dotenv import load_dotenv


load_dotenv()

DB_CONNECTION_STRING = os.getenv("TEST_DB_CONNECTION_STRING")
engine = create_engine(DB_CONNECTION_STRING)


@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    """Create a fresh DB for tests. NOTE: Drops any existing db with the same name."""
    if database_exists(engine.url):
        drop_database(engine.url)

    create_database(engine.url)
    Base.metadata.create_all(bind=engine)

    yield  # tests run at this point

    drop_database(engine.url)


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
