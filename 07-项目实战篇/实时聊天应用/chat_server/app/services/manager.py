"""WebSocket 连接管理"""

from fastapi import WebSocket
from typing import Dict
from datetime import datetime
import json
from ..models import User, UserStatus, Message, MessageType


class ConnectionManager:
    """WebSocket 连接管理器"""
    
    def __init__(self):
        # username -> {"websocket": WebSocket, "user": User}
        self._connections: Dict[str, dict] = {}
    
    @property
    def connections(self) -> Dict[str, dict]:
        return self._connections
    
    async def connect(self, websocket: WebSocket, username: str) -> bool:
        """接受新连接"""
        if username in self._connections:
            return False
        
        await websocket.accept()
        self._connections[username] = {
            "websocket": websocket,
            "user": User(username=username)
        }
        return True
    
    def disconnect(self, username: str) -> None:
        """断开连接"""
        self._connections.pop(username, None)
    
    def get_users(self) -> list[str]:
        """获取在线用户列表"""
        return list(self._connections.keys())
    
    def get_user(self, username: str) -> User | None:
        """获取用户信息"""
        conn = self._connections.get(username)
        return conn["user"] if conn else None
    
    def set_status(self, username: str, status: UserStatus) -> None:
        """设置用户状态"""
        conn = self._connections.get(username)
        if conn:
            conn["user"].status = status
    
    async def send_to(self, username: str, message: dict) -> None:
        """发送消息给指定用户"""
        conn = self._connections.get(username)
        if conn:
            await conn["websocket"].send_json(message)
    
    async def broadcast(
        self, 
        message: dict, 
        exclude: str | None = None
    ) -> None:
        """广播消息给所有用户"""
        for username, conn in self._connections.items():
            if username != exclude:
                await conn["websocket"].send_json(message)
    
    async def broadcast_users(self) -> None:
        """广播用户列表"""
        message = {
            "type": MessageType.USERS.value,
            "users": self.get_users(),
            "count": len(self._connections)
        }
        await self.broadcast(message)


# 全局连接管理器
manager = ConnectionManager()