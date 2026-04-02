"""用户服务"""

from typing import Optional
from datetime import datetime
from app.models.user import UserResponse


class UserService:
    """用户服务"""
    
    def __init__(self):
        self._users: dict[int, dict] = {}
        self._next_id = 1
    
    def create(self, name: str, email: str) -> UserResponse:
        """创建用户"""
        user_data = {
            "id": self._next_id,
            "name": name,
            "email": email,
            "created_at": datetime.now()
        }
        self._users[self._next_id] = user_data
        self._next_id += 1
        return UserResponse(**user_data)
    
    def get(self, user_id: int) -> Optional[UserResponse]:
        """获取用户"""
        if user_id in self._users:
            return UserResponse(**self._users[user_id])
        return None
    
    def get_all(self) -> list[UserResponse]:
        """获取所有用户"""
        return [UserResponse(**u) for u in self._users.values()]


user_service = UserService()