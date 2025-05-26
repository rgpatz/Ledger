from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

load_dotenv() # Load variables from .env file

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable not set")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() # This is the same Base used in models.py

def create_db_and_tables():
    from app.models import Base as AppBase # import Base from models.py
    AppBase.metadata.create_all(bind=engine)

# Dependency-must be called by the FastAPI app to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 