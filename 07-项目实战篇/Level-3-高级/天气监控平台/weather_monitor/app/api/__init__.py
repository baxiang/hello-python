"""API 路由"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..models import City
from ..services import WeatherService

router = APIRouter()


@router.get("/cities")
def get_cities(db: Session = Depends(get_db)):
    """获取城市列表"""
    cities = WeatherService.get_cities(db)
    return [{"id": c.id, "name": c.city_name, "code": c.city_code} for c in cities]


@router.post("/cities")
def add_city(
    city_name: str,
    city_code: str = None,
    province: str = None,
    db: Session = Depends(get_db),
):
    """添加城市"""
    existing = WeatherService.get_city_by_name(db, city_name)
    if existing:
        raise HTTPException(status_code=400, detail="城市已存在")
    return WeatherService.add_city(db, city_name, city_code, province)


@router.get("/weather/{city_id}")
def get_weather(city_id: int, limit: int = 30, db: Session = Depends(get_db)):
    """获取城市天气历史"""
    records = WeatherService.get_weather_by_city(db, city_id, limit)
    return [
        {
            "date": r.record_date,
            "high_temp": r.high_temp,
            "low_temp": r.low_temp,
            "condition": r.weather_condition,
            "humidity": r.humidity,
        }
        for r in records
    ]


@router.get("/weather/{city_id}/latest")
def get_latest_weather(city_id: int, db: Session = Depends(get_db)):
    """获取城市最新天气"""
    record = WeatherService.get_latest_weather(db, city_id)
    if not record:
        raise HTTPException(status_code=404, detail="无天气数据")
    return {
        "city_id": city_id,
        "date": record.record_date,
        "high_temp": record.high_temp,
        "low_temp": record.low_temp,
        "condition": record.weather_condition,
        "wind": record.wind_direction,
        "humidity": record.humidity,
    }


@router.post("/weather/{city_id}/fetch")
async def fetch_and_save_weather(city_id: int, db: Session = Depends(get_db)):
    """获取并保存实时天气"""
    city = db.query(City).filter_by(id=city_id).first()
    if not city or not city.city_code:
        raise HTTPException(status_code=400, detail="城市不存在或无城市代码")

    try:
        data = await WeatherService.fetch_weather(city.city_code)
        record = WeatherService.save_weather(db, city_id, data)
        return {"message": "天气数据已更新", "record_id": record.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
