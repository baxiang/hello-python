"""配置"""

from dataclasses import dataclass


@dataclass
class Config:
    """应用配置"""
    DEBUG: bool = True
    SECRET_KEY: str = "dev-secret-key"
    DATABASE_URL: str = "sqlite:///app.db"


config = Config()