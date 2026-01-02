from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field, EmailStr
from starlette import status
from models import Users
import bcrypt

from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db # Provide a database session to the path operation
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]

class UserCreateRequest(BaseModel):
    """Schema for user creation request"""
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr = Field(...)
    password: str = Field(min_length=6)
    is_active: bool = Field(default=True)
    role: str = Field(default="user")
    
# Utility Function to hash passwords
def hash_password(password: str) -> str:
    """This function will hash the password before storing it in the database

    Args:
        password (str): Password in plain text

    Returns:
        str: Hashed passwords
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

@router.post('/auth/signup', status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreateRequest, db: db_dependency):
    """Endpoint to create a new user

    Args:
        user (UserCreateRequest): User creation request body
        db (Session): Database session dependency
    
    Returns:
        dict: Success message
    """
    hashed_pw = hash_password(user.password)
    user_model = Users(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pw,
        is_active=user.is_active,
        role=user.role
    )

    db.add(user_model)
    db.commit()
    return {"message": "User created successfully"}