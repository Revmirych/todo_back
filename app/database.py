from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/todo_db')

engine = create_engine(DATABASE_URL)
Base = declarative_base()

def my_session_local():
   SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
   yield SessionLocal()
