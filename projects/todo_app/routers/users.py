from fastapi import APIRouter, Depends, HTTPException, Path
from database import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from crud.auth import get_current_user, hash_password
from starlette import status
from models import Users
from pydantic import BaseModel, Field
import bcrypt

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

class UpdatePasswordRequest(BaseModel):
    old_password: str = Field(..., min_length=3)
    new_password: str = Field(..., min_length=3)
        
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    user_data = db.query(Users).filter(Users.id == user.id).first()
    return user_data

@router.put("/change-password", status_code=status.HTTP_202_ACCEPTED)
async def change_password(
    password_data: UpdatePasswordRequest, 
    user: user_dependency, 
    db: db_dependency
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    
    if not bcrypt.checkpw(
        password_data.old_password.encode('utf-8'),
        user.hashed_password.encode('utf-8')
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Old password doesn't match"
        )
    
    if bcrypt.checkpw(
        password_data.new_password.encode('utf-8'),
        user.hashed_password.encode('utf-8')
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be different"
        )
    
    # Update password
    print(type(user))
    user.hashed_password = hash_password(password_data.new_password)
    db.commit()

    return {"message": f"Password Changed for user: {user.username}"}