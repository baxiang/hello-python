"""用户模型"""

from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class User:
    """用户模型"""
    id: Optional[int] = None
    name: str = ""
    email: str = ""
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }