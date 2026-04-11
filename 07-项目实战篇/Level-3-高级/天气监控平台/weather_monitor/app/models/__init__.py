"""数据模型"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core import Base


class City(Base):
    """城市模型"""

    __tablename__ = "cities"

    id = Column(Integer, primary_key=True)
    city_name = Column(String(50), unique=True, nullable=False)
    city_code = Column(String(20))
    province = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

    weather_records = relationship("WeatherRecord", back_populates="city")


class WeatherRecord(Base):
    """天气记录"""

    __tablename__ = "weather_records"

    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    record_date = Column(Date, nullable=False)
    high_temp = Column(Integer)
    low_temp = Column(Integer)
    weather_condition = Column(String(50))
    wind_direction = Column(String(50))
    wind_power = Column(String(20))
    humidity = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    city = relationship("City", back_populates="weather_records")
