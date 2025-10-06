"""
- Create models, python classes that inherit from the Base -> SQLAlchemy will map these models to
database tables    
"""
from sqlalchemy import Column, Integer, String, Boolean

from database import Base

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
    