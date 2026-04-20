"""用户模型"""

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    """用户基础模型"""
    name: str
    email: EmailStr


class UserCreate(UserBase):
    """用户创建模型"""
    pass


class UserResponse(UserBase):
    """用户响应模型"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True