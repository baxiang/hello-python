# 项目四：Weather API 服务

> 使用 FastAPI 构建天气数据 REST API 服务

---

## 项目目标

- 掌握 FastAPI 框架基础
- 学会创建 RESTful API
- 理解 Pydantic 数据验证
- 能够实现 API 认证和文档

---

## 第一部分 - 项目结构

```
weather_api/
├── main.py              # API 入口
├── models.py            # 数据库模型（复用项目三）
├── schemas.py           # Pydantic 模型
├── database.py          # 数据库连接（复用项目三）
├── repository.py        # 数据访问层（复用项目三）
├── api/
│   ├── __init__.py
│   ├── weather.py       # 天气 API 路由
│   └── cities.py        # 城市 API 路由
└── requirements.txt
```

---

## 第二部分 - 基础 API

### 2.1 Pydantic 模型

```python
# schemas.py
from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional, List

class WeatherBase(BaseModel):
    high_temp: Optional[int] = None
    low_temp: Optional[int] = None
    weather_condition: Optional[str] = None
    wind_direction: Optional[str] = None
    wind_power: Optional[str] = None
    humidity: Optional[int] = None

class WeatherCreate(WeatherBase):
    city_id: int
    record_date: date

class WeatherUpdate(WeatherBase):
    pass

class WeatherResponse(WeatherBase):
    id: int
    city_id: int
    record_date: date
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class CityBase(BaseModel):
    city_name: str = Field(..., min_length=1, max_length=50)
    city_code: Optional[str] = None
    province: Optional[str] = None

class CityCreate(CityBase):
    pass

class CityResponse(CityBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
```

### 2.2 FastAPI 主应用

```python
# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, init_db
from api import weather, cities

# 创建数据库表
init_db()

# 创建 FastAPI 应用
app = FastAPI(
    title="Weather API",
    description="天气数据查询 API 服务",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(weather.router, prefix="/api/weather", tags=["天气"])
app.include_router(cities.router, prefix="/api/cities", tags=["城市"])

@app.get("/")
def root():
    return {
        "message": "Weather API Service",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 2.3 天气 API 路由

```python
# api/weather.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from database import get_session
from repository import WeatherRepository
from schemas import WeatherResponse, WeatherCreate, WeatherUpdate

router = APIRouter()

def get_repo(session: Session = Depends(get_session)) -> WeatherRepository:
    return WeatherRepository(session)

@router.get("/{city_id}", response_model=List[WeatherResponse])
def get_city_weather(
    city_id: int,
    start_date: date = Query(None),
    end_date: date = Query(None),
    repo: WeatherRepository = Depends(get_repo)
):
    """获取城市天气记录"""
    records = repo.get_records_by_city(city_id, start_date, end_date)
    return records

@router.get("/{city_id}/latest", response_model=WeatherResponse)
def get_latest_weather(city_id: int, repo: WeatherRepository = Depends(get_repo)):
    """获取城市最新天气"""
    record = repo.get_latest_record(city_id)
    if not record:
        raise HTTPException(status_code=404, detail="No weather record found")
    return record

@router.post("/", response_model=WeatherResponse)
def create_weather_record(
    weather: WeatherCreate,
    repo: WeatherRepository = Depends(get_repo)
):
    """创建天气记录"""
    record = repo.add_weather_record(
        city_id=weather.city_id,
        record_date=weather.record_date,
        high_temp=weather.high_temp,
        low_temp=weather.low_temp,
        weather_condition=weather.weather_condition,
        wind_direction=weather.wind_direction,
        wind_power=weather.wind_power,
        humidity=weather.humidity
    )
    return record

@router.put("/{record_id}", response_model=WeatherResponse)
def update_weather_record(
    record_id: int,
    weather: WeatherUpdate,
    repo: WeatherRepository = Depends(get_repo)
):
    """更新天气记录"""
    # 实现更新逻辑
    pass

@router.delete("/{record_id}")
def delete_weather_record(record_id: int, repo: WeatherRepository = Depends(get_repo)):
    """删除天气记录"""
    # 实现删除逻辑
    pass
```

### 2.4 城市 API 路由

```python
# api/cities.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_session
from repository import WeatherRepository
from schemas import CityResponse, CityCreate

router = APIRouter()

@router.get("/", response_model=List[CityResponse])
def list_cities(skip: int = 0, limit: int = 100):
    """获取城市列表"""
    # 实现列表查询
    pass

@router.get("/{city_name}", response_model=CityResponse)
def get_city(city_name: str, repo: WeatherRepository = Depends(get_repo)):
    """获取城市详情"""
    city = repo.get_city_by_name(city_name)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city

@router.post("/", response_model=CityResponse)
def create_city(city: CityCreate, repo: WeatherRepository = Depends(get_repo)):
    """创建城市"""
    # 检查是否已存在
    existing = repo.get_city_by_name(city.city_name)
    if existing:
        raise HTTPException(status_code=400, detail="City already exists")
    
    new_city = repo.add_city(city.city_name, city.city_code, city.province)
    return new_city
```

---

## 第三部分 - 运行和测试

### 3.1 启动服务

```bash
# 安装依赖
uv add fastapi uvicorn sqlalchemy pymysql

# 启动服务
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 或使用 python
python main.py
```

### 3.2 API 测试

```bash
# 查看 API 文档
# http://localhost:8000/docs

# 健康检查
curl http://localhost:8000/health

# 获取城市天气
curl http://localhost:8000/api/weather/1

# 获取最新天气
curl http://localhost:8000/api/weather/1/latest

# 创建天气记录
curl -X POST http://localhost:8000/api/weather/ \
  -H "Content-Type: application/json" \
  -d '{
    "city_id": 1,
    "record_date": "2024-03-10",
    "high_temp": 15,
    "low_temp": 5,
    "weather_condition": "晴"
  }'

# 获取城市列表
curl http://localhost:8000/api/cities/

# 创建城市
curl -X POST http://localhost:8000/api/cities/ \
  -H "Content-Type: application/json" \
  -d '{
    "city_name": "北京",
    "city_code": "54511"
  }'
```

---

## 第四部分 - 项目总结

### 学到的技能

| 技能 | 说明 |
|------|------|
| FastAPI | 快速构建 REST API |
| Pydantic | 数据验证和序列化 |
| 路由设计 | RESTful API 设计 |
| 依赖注入 | FastAPI Depends |
| API 文档 | 自动生成 Swagger |
| CORS | 跨域配置 |

### 下一步

在 [项目五](./05-天气监控平台.md) 中，我们将：
- 添加前端界面
- 实现数据可视化
- 添加告警功能
- Docker 容器化部署
