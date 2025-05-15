from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class CategoryBase(BaseModel):
    name: str = Field(min_length=3)

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    class Config:
        orm_mode = True

class TaskBase(BaseModel):
    title: str = Field(min_length=3)
    description: Optional[str] = None
    category_id: Optional[int] = None
    priority: Optional[int] = 1
    due_date: Optional[datetime] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    status: Optional[str] = None
    is_completed: Optional[bool] = None

class Task(TaskBase):
    id: int
    status: str
    is_completed: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    user_id: int
    category: Optional[Category]
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    first_name: str = Field(min_length=3)
    last_name: str = Field(min_length=3)
    username: str = Field(min_length=3)

class UserCreate(UserBase):
    password: str = Field(min_length=5)

class User(UserBase):
    id: int
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
