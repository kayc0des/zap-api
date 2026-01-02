from pydantic import BaseModel, Field, EmailStr

class UserCreateRequest(BaseModel):
    """Schema for user creation request"""
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr = Field(...)
    password: str = Field(min_length=6)
    is_active: bool = Field(default=True)
    role: str = Field(default="user")
    
class TodoRequest(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=3, max_length=250)
    priority: int = Field(gt=0, lt=6)
    complete: bool = False
    