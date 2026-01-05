from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from models import Todos
from database import get_db
from typing import Annotated
from starlette import status
from pydantic import BaseModel, Field
from api_models import TodoRequest
from crud.auth import get_current_user

router = APIRouter(
    prefix="/todos",
    tags=["Todos"]
)
        
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
        
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    result = db.query(Todos).filter(Todos.owner_id == user.id).all()
    return result

@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    todo_model = db.query(
        Todos
        ).filter(
            Todos.id == todo_id,
            Todos.owner_id == user.id
        ).first()
    
    if todo_model is not None:
        return todo_model

    raise HTTPException(status_code=404, detail=f"Todo with the id {todo_id} not found")

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, todo: TodoRequest):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    todo_model = Todos(
        title=todo.title,
        description=todo.description,
        priority=todo.priority,
        complete=todo.complete,
        owner_id=user.id
    )
    
    db.add(todo_model)
    db.commit()
    return todo_model


@router.put("/{todo_id}", status_code=status.HTTP_200_OK)
async def update_todo(user: user_dependency, db: db_dependency, todo: TodoRequest, todo_id: int = Path(gt=0)):
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id, Todos.owner_id == user.id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail=f"Todo with the id {todo_id} not found")
    
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete
    
    db.commit()
    return todo_model

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    todo_model = db.query(
        Todos
        ).filter(
            Todos.id == todo_id,
            Todos.owner_id == user.id
        ).first()
        
    if todo_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with the id {todo_id} not found"
        )
    
    db.delete(todo_model)
    db.commit()
    return