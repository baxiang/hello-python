"""数据模型"""

from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from ..core import Base


class City(Base):
    """城市模型"""
    __tablename__ = "cities"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    country = Column(String(50))
    lat = Column(Float)
    lon = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)


class WeatherRecord(Base):
    """天气记录"""
    __tablename__ = "weather_records"
    
    id = Column(Integer, primary_key=True)
    city_id = Column(Integer)
    city_name = Column(String(100))
    temp = Column(Float)
    feels_like = Column(Float)
    humidity = Column(Integer)
    pressure = Column(Integer)
    wind_speed = Column(Float)
    description = Column(String(200))
    recorded_at = Column(DateTime, default=datetime.utcnow)