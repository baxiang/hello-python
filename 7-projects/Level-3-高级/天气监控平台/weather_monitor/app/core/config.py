"""配置"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    API_KEY: str = os.getenv("WEATHER_API_KEY", "")
    API_URL: str = os.getenv("WEATHER_API_URL", "https://devapi.qweather.com/v7")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./weather.db")


config = Config()
