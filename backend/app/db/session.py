from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    "sqlite:///backend/app/test.db", connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)
