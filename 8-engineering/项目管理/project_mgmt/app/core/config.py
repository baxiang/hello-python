"""配置管理"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """应用配置"""
    app_name: str = "MyApp"
    version: str = "0.1.0"
    debug: bool = False
    database_url: str = "sqlite:///app.db"
    secret_key: str = "dev-secret-key"
    
    @classmethod
    def from_env(cls) -> "Config":
        """从环境变量加载"""
        return cls(
            app_name=os.getenv("APP_NAME", "MyApp"),
            version=os.getenv("APP_VERSION", "0.1.0"),
            debug=os.getenv("DEBUG", "false").lower() == "true",
            database_url=os.getenv("DATABASE_URL", "sqlite:///app.db"),
            secret_key=os.getenv("SECRET_KEY", "dev-secret-key")
        )


class ConfigManager:
    """配置管理器"""
    
    def __init__(self):
        self._config: Optional[Config] = None
        self._overrides: dict = {}
    
    def load(self, config: Config) -> None:
        """加载配置"""
        self._config = config
    
    def get(self, key: str, default=None):
        """获取配置项"""
        if key in self._overrides:
            return self._overrides[key]
        if self._config and hasattr(self._config, key):
            return getattr(self._config, key)
        return default
    
    def set(self, key: str, value) -> None:
        """设置配置项"""
        self._overrides[key] = value