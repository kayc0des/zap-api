"""
- Create models, python classes that inherit from the Base -> SQLAlchemy will map these models to
database tables    
"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

class Users(Base):
    """Create the table called users

    Args:
        Base (cls): Inherits the base class wired to SQLAlchemy
    """
    
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")
    
    todos = relationship("Todos", back_populates="owner")

class Todos(Base):
    """Create the table called todos

    Args:
        Base (cls): Inherits the base class wired to SQLAlchemy
    """
    
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    owner = relationship("Users", back_populates="todos")
    