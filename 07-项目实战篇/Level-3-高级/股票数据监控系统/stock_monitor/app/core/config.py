"""配置"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    API_KEY: str = os.getenv("STOCK_API_KEY", "")
    API_URL: str = os.getenv("STOCK_API_URL", "https://api.example.com/v1")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./stocks.db")


config = Config()