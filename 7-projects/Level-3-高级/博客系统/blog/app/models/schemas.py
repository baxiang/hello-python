"""Pydantic 模型"""

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


# 用户模型
class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# 文章模型
class PostBase(BaseModel):
    title: str
    content: str
    summary: Optional[str] = None


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    is_published: Optional[bool] = None


class PostResponse(PostBase):
    id: int
    author_id: int
    is_published: bool
    view_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# 评论模型
class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    pass


class CommentResponse(CommentBase):
    id: int
    post_id: int
    author_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True