"""数据模型"""

from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Optional


class MessageType(str, Enum):
    """消息类型"""
    JOIN = "join"
    LEAVE = "leave"
    MESSAGE = "message"
    USERS = "users"
    HISTORY = "history"
    STATUS = "status"


class UserStatus(str, Enum):
    """用户状态"""
    ONLINE = "online"
    AWAY = "away"
    BUSY = "busy"


class Message(BaseModel):
    """聊天消息"""
    type: MessageType
    username: str
    content: Optional[str] = None
    timestamp: datetime = None
    users: Optional[list[str]] = None
    
    def __init__(self, **data):
        super().__init__(**data)
        if self.timestamp is None:
            self.timestamp = datetime.now()


class User(BaseModel):
    """用户信息"""
    username: str
    status: UserStatus = UserStatus.ONLINE
    connected_at: datetime = None
    
    def __init__(self, **data):
        super().__init__(**data)
        if self.connected_at is None:
            self.connected_at = datetime.now()