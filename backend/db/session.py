from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///backend/test.db")

SessionLocal = sessionmaker(bind=engine)
