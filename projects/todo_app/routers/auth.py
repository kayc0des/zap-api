from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, EmailStr
from starlette import status
from models import Users
import bcrypt

from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from config import settings
from api_models import UserCreateRequest

router = APIRouter()

# openssl rand -hex 32 - to generate a secret key
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

def get_db():
    db = SessionLocal()
    try:
        yield db # Provide a database session to the path operation
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]
    
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

def authenticate_user(db: Session, username: str, password: str):
    """Authenticate user by username and password

    Args:
        db (Session): Database session
        username (str): Username of the user
        password (str): Plain text password

    Returns:
        Users | None: Returns the user object if authentication is successful, else None
    """
    user = db.query(Users).filter(Users.username == username).first()
    if user and bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8')):
        return user
    return None

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

@router.post('/auth/token')
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": user.username, "token_type": "bearer"}