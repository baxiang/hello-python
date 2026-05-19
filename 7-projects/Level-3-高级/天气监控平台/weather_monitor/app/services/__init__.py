"""天气服务"""

import httpx
from sqlalchemy.orm import Session
from datetime import datetime, date
from typing import Optional
from ..core.config import config
from ..models import City, WeatherRecord


class WeatherService:
    """天气服务"""

    @staticmethod
    async def fetch_weather(city_code: str) -> dict:
        """获取天气数据"""
        url = f"{config.API_URL}/weather/now"
        params = {"location": city_code, "key": config.API_KEY}

        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()

    @staticmethod
    def save_weather(db: Session, city_id: int, data: dict) -> WeatherRecord:
        """保存天气记录"""
        now_data = data.get("now", {})
        record = WeatherRecord(
            city_id=city_id,
            record_date=date.today(),
            high_temp=int(now_data.get("temp", 0)),
            low_temp=int(now_data.get("temp", 0)),
            weather_condition=now_data.get("text"),
            wind_direction=now_data.get("windDir"),
            wind_power=now_data.get("windScale"),
            humidity=int(now_data.get("humidity", 0)),
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def add_city(
        db: Session, city_name: str, city_code: str = None, province: str = None
    ) -> City:
        """添加城市"""
        city = City(city_name=city_name, city_code=city_code, province=province)
        db.add(city)
        db.commit()
        db.refresh(city)
        return city

    @staticmethod
    def get_cities(db: Session) -> list[City]:
        """获取所有城市"""
        return db.query(City).all()

    @staticmethod
    def get_city_by_name(db: Session, city_name: str) -> Optional[City]:
        """根据名称获取城市"""
        return db.query(City).filter(City.city_name == city_name).first()

    @staticmethod
    def get_weather_by_city(
        db: Session, city_id: int, limit: int = 30
    ) -> list[WeatherRecord]:
        """获取城市天气历史"""
        return (
            db.query(WeatherRecord)
            .filter(WeatherRecord.city_id == city_id)
            .order_by(WeatherRecord.record_date.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_latest_weather(db: Session, city_id: int) -> Optional[WeatherRecord]:
        """获取城市最新天气"""
        return (
            db.query(WeatherRecord)
            .filter(WeatherRecord.city_id == city_id)
            .order_by(WeatherRecord.record_date.desc())
            .first()
        )
