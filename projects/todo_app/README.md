# Todo App
This is a small project designed to help you get started with databases. Its purpose is to introduce SQL, SQLite, and demonstrate how to establish a database connection using the SQLAlchemy ORM. For more details, check out the [SQLAlchemy documentation](https://docs.sqlalchemy.org/en/20/)

## `database.py`
This is the file used to create the database engine using SQLAlchemy ORM! 

- `DATABASE_URL`: This is simply a connection string - it tells SQLAlchemy where the database is and how to connect to it. Think of it like a database "address".
  ```python
  DATABASE_URL = "" # string declaration of database url
  ```
- `engine = create_engine(DATABASE_URL)`: This is a function from SQLAlchemy that connects Python to a database. Analogy is opennin a pipeline so Python can talk to SQLite/ PostgreSQL, MySQL

- `SessionLocal = sessionmaker(...)`: **sessionmaker** creates sessions, which are like “workspaces” for talking to the database. Every time you want to read/write data, you use a session. Think of it as a temporary connection where you can add, edit, or delete data, then save it.
  ```python
  SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
  ```
  - `SessionLocal` is a factory for creating sessions (think of each session as a workspace for database operations).
  - `autocommit=False` → changes are only saved when you explicitly call .commit().
  - `autoflush=False` → SQLAlchemy won’t automatically push pending changes to the database until you commit.
  - `bind=engine` → tells the sessions to use the engine we just created.

- `Base = declarative_base()`: **declarative_base()** is a function that gives you a base class to define your models (tables). Models are Python classes that represent database tables. Using declarative_base ties your classes to SQLAlchemy so it knows how to create tables in the database.

### Workflow
- Find a safe path for the database file. ✅
- Build a connection string (DATABASE_URL). ✅
- Create an engine — the gateway to the database. ✅
- Create a session factory to interact with the database safely. ✅
- Create a base class to define your database tables (models). ✅


## `models.py`

The class in this script represents a `todos` table in the database. Each attribute in the class corresponds to a **column** in the table:

- `id` → Primary key, uniquely identifies each todo item.  
- `title` → Text field for the todo title.  
- `description` → Text field for details about the todo.  
- `priority` → Integer to indicate importance.  
- `complete` → Boolean to track whether the task is done, defaulting to `False`.  

### Summary

This file sets up the structure of the `todos` table in Python. SQLAlchemy uses the model to handle all database operations such as creating tables, inserting data, updating records, and querying todos.


## `main.py`

This file is the entry point of the FastAPI application. It sets up and starts the web server while ensuring that the database tables are ready for use.

### Purpose

1. **Initialize the FastAPI app**  
   - The file creates an instance of the FastAPI application, which will handle all incoming HTTP requests and route them to the appropriate endpoints.  

2. **Prepare the database**  
   - It uses the models defined in the project to create all necessary database tables.  
   - If the tables already exist, SQLAlchemy does not overwrite or delete them; it only creates tables that are missing.  
   - This ensures that the database structure is always in sync with the models when the application starts.  

3. **Safe repeated execution**  
   - Running the application multiple times or in development mode (e.g., with auto-reload) is safe. Existing tables and data remain intact.  
