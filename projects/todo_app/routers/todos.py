from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from models import Todos
from database import SessionLocal
from typing import Annotated
from starlette import status
from pydantic import BaseModel, Field
from api_models import TodoRequest

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db # Provide a database session to the path operation
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]
        
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Todos).all()

@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail=f"Todo with the id {todo_id} not found")

@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo: TodoRequest):
    todo_model = Todos(
        title=todo.title,
        description=todo.description,
        priority=todo.priority,
        complete=todo.complete
    )
    db.add(todo_model)
    db.commit()
    return todo_model


@router.put("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def update_todo(db: db_dependency, todo: TodoRequest, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail=f"Todo with the id {todo_id} not found")
    
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    
    db.commit()
    return todo_model

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail=f"Todo with the id {todo_id} not found")
    
    db.delete(todo_model)
    db.commit()
    return