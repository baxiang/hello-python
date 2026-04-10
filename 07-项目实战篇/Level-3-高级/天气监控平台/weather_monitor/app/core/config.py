"""配置"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    API_KEY: str = os.getenv("WEATHER_API_KEY", "")
    API_URL: str = os.getenv("WEATHER_API_URL", "https://api.openweathermap.org/data/2.5")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./weather.db")


config = Config()