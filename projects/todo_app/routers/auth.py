from datetime import timedelta, datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, EmailStr
from starlette import status
from models import Users
import bcrypt

from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from config import settings
from api_models import UserCreateRequest
from crud.auth import (
    db_dependency, 
    oauth2_scheme, 
    hash_password, 
    authenticate_user, 
    create_access_token, 
    get_current_user
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post('/', status_code=status.HTTP_201_CREATED)
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

@router.post('/token')
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(
        username=user.username,
        user_id=user.id,
        role=user.role,
        expires_delta=timedelta(hours=1)
    )

    return {"access_token": token, "token_type": "bearer"}