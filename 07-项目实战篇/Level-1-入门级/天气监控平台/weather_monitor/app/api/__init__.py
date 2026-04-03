"""API 路由"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core import get_db
from ..services import WeatherService

router = APIRouter()


@router.get("/weather/{city}")
async def get_weather(city: str, db: Session = Depends(get_db)):
    """获取当前天气"""
    try:
        data = await WeatherService.fetch_weather(city)
        record = WeatherService.save_record(db, data)
        return {
            "city": data["name"],
            "temp": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/history/{city}")
def get_history(city: str, limit: int = 10, db: Session = Depends(get_db)):
    """获取历史记录"""
    records = WeatherService.get_history(db, city, limit)
    return [{"city": r.city_name, "temp": r.temp, "recorded_at": r.recorded_at} for r in records]


@router.get("/cities")
def get_cities(db: Session = Depends(get_db)):
    """获取城市列表"""
    return WeatherService.get_cities(db)