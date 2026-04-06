"""路由"""

from fastapi import APIRouter, HTTPException
from app.models.user import UserCreate, UserResponse
from app.services.user_service import user_service

router = APIRouter()


@router.get("/hello")
def hello():
    """问候接口"""
    return {"message": "Hello, FastAPI!"}


@router.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate):
    """创建用户"""
    return user_service.create(user.name, user.email)


@router.get("/users", response_model=list[UserResponse])
def get_users():
    """获取用户列表"""
    return user_service.get_all()


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    """获取用户"""
    user = user_service.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user