from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# DATABASE_URL = "sqlite:///./todo_app/todo.db"
# OR

# Get the path to the folder containing this file (todo_app/)
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "todosapp.db"

DATABASE_URL = f"sqlite:///{DB_PATH}" 

engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False}) # gateway between python and the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

"""
The declarative base class from which all models will inherit
It is used by SQLAlchemy to map the models to database tables

When you create classes that inherit from this Base, SQLAlchemy will know to create
the corresponding tables in the database.
"""
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()