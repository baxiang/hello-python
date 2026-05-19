"""API 路由"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from ..core import get_db
from ..models.schemas import (
    UserCreate, UserResponse,
    PostCreate, PostUpdate, PostResponse
)
from ..services import UserService, PostService

router = APIRouter()


# 用户路由
@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """创建用户"""
    if UserService.get_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="用户名已存在")
    if UserService.get_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="邮箱已注册")
    return UserService.create(db, user)


@router.get("/users/{username}", response_model=UserResponse)
def get_user(username: str, db: Session = Depends(get_db)):
    """获取用户"""
    user = UserService.get_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


# 文章路由
@router.post("/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, author_id: int, db: Session = Depends(get_db)):
    """创建文章"""
    return PostService.create(db, post, author_id)


@router.get("/posts", response_model=list[PostResponse])
def get_posts(
    skip: int = 0,
    limit: int = 10,
    author_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """获取文章列表"""
    return PostService.get_list(db, skip, limit, author_id)


@router.get("/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """获取文章详情"""
    post = PostService.get(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="文章不存在")
    PostService.increment_view(db, post_id)
    return post


@router.put("/posts/{post_id}", response_model=PostResponse)
def update_post(post_id: int, post: PostUpdate, db: Session = Depends(get_db)):
    """更新文章"""
    updated = PostService.update(db, post_id, post)
    if not updated:
        raise HTTPException(status_code=404, detail="文章不存在")
    return updated


@router.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    """删除文章"""
    if not PostService.delete(db, post_id):
        raise HTTPException(status_code=404, detail="文章不存在")
    return {"message": "删除成功"}