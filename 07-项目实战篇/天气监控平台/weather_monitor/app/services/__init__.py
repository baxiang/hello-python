"""天气服务"""

import httpx
from sqlalchemy.orm import Session
from datetime import datetime
from .config import config
from .models import WeatherRecord, City


class WeatherService:
    """天气服务"""
    
    @staticmethod
    async def fetch_weather(city: str) -> dict:
        """获取天气数据"""
        url = f"{config.API_URL}/weather"
        params = {
            "q": city,
            "appid": config.API_KEY,
            "units": "metric"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
    
    @staticmethod
    def save_record(db: Session, data: dict) -> WeatherRecord:
        """保存天气记录"""
        record = WeatherRecord(
            city_id=data.get("id"),
            city_name=data["name"],
            temp=data["main"]["temp"],
            feels_like=data["main"]["feels_like"],
            humidity=data["main"]["humidity"],
            pressure=data["main"]["pressure"],
            wind_speed=data["wind"]["speed"],
            description=data["weather"][0]["description"]
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record
    
    @staticmethod
    def get_history(db: Session, city: str, limit: int = 10) -> list:
        """获取历史记录"""
        return db.query(WeatherRecord).filter(
            WeatherRecord.city_name == city
        ).order_by(WeatherRecord.recorded_at.desc()).limit(limit).all()
    
    @staticmethod
    def add_city(db: Session, name: str, country: str = None, lat: float = None, lon: float = None) -> City:
        """添加城市"""
        city = City(name=name, country=country, lat=lat, lon=lon)
        db.add(city)
        db.commit()
        db.refresh(city)
        return city
    
    @staticmethod
    def get_cities(db: Session) -> list:
        """获取所有城市"""
        return db.query(City).all()