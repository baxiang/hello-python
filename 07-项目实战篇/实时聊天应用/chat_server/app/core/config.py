"""配置管理"""

import os
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """应用配置"""
    
    # 服务器配置
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    
    # 数据库配置
    database_url: str = "sqlite:///./chat.db"
    
    # 聊天配置
    max_history: int = 100
    max_connections: int = 1000
    
    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    """获取配置实例"""
    return Settings()