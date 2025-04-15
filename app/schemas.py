from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    class Config:
        orm_mode = True

class TaskBase(BaseModel):
    title: str
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
    updated_at: datetime
    user_id: int
    category: Optional[Category]
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    first_name: str
    last_name: str
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
