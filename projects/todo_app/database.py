from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# DATABASE_URL = "sqlite:///./todo_app/todo.db"
# OR

# Get the path to the folder containing this file (todo_app/)
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "todo.db"

DATABASE_URL = f"sqlite:///{DB_PATH}" 

engine = create_engine(DATABASE_URL, connect_args={'check_same_thread': False}) # gateway between python and the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()