"""用户服务"""

from typing import Optional
from app.models.user import User


class UserService:
    """用户服务"""
    
    def __init__(self):
        self._users: dict[int, User] = {}
        self._next_id = 1
    
    def create(self, name: str, email: str) -> User:
        """创建用户"""
        user = User(id=self._next_id, name=name, email=email)
        self._users[self._next_id] = user
        self._next_id += 1
        return user
    
    def get(self, user_id: int) -> Optional[User]:
        """获取用户"""
        return self._users.get(user_id)
    
    def get_all(self) -> list[User]:
        """获取所有用户"""
        return list(self._users.values())
    
    def delete(self, user_id: int) -> bool:
        """删除用户"""
        if user_id in self._users:
            del self._users[user_id]
            return True
        return False


user_service = UserService()