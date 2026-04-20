"""配置"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """应用配置"""
    app_name: str = "FastAPI Demo"
    debug: bool = True
    secret_key: str = "dev-secret-key"
    
    class Config:
        env_file = ".env"


settings = Settings()