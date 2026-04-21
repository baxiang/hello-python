"""配置管理"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置"""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    APP_NAME: str = "Task Manager API"
    APP_ENV: str = "development"
    API_TITLE: str = "Task Manager API"
    APP_DESCRIPTION: str = "FastAPI任务管理API，演示JWT认证、CRUD、WebSocket、后台任务"
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = "sqlite+aiosqlite:///./taskmanager.db"


def get_settings() -> Settings:
    """获取配置实例"""
    return Settings()