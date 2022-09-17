import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")

engine = create_engine(DB_CONNECTION_STRING)

SessionLocal = sessionmaker(bind=engine)
