from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///backend/app/test.db")

SessionLocal = sessionmaker(bind=engine)
