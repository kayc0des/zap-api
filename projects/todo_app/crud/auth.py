from datetime import timedelta, datetime, timezone
from fastapi import Depends, HTTPException
from starlette import status
from models import Users
import bcrypt

from database import get_db
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from config import settings

# openssl rand -hex 32 - to generate a secret key
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
        
db_dependency = Annotated[Session, Depends(get_db)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
    
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

def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta = None):
    """Create a JWT access token for the authenticated user

    Args:
        username (str): Username of the user
        user_id (int): ID of the user
    Returns:
        str: JWT access token
    """
    encode = {"sub": username, "id": user_id, "role": role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: db_dependency):
    """Get the current authenticated user from the JWT token

    Args:
        token (str): JWT token from the request
        db (Session): Database session
    Returns:
        Users: The authenticated user object
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        role: str = payload.get("role")
        if username is None or user_id is None or role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = db.query(Users).filter(Users.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # return {"username": username, "user_id": user_id, "user_role": role}
    return user