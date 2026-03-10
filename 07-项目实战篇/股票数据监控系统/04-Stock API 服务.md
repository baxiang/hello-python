# 项目四：Stock API 服务

> 使用 FastAPI 构建 RESTful API 服务

---

## 项目目标

- 掌握 FastAPI 框架使用
- 学会设计 RESTful API
- 实现数据接口服务化
- 理解 API 文档和参数验证

---

## 第一部分 - 需求分析

### 功能需求

1. 提供股票实时行情查询 API
2. 提供历史数据查询 API
3. 支持分页和筛选
4. 自动生成 API 文档

### 技术选型

| 组件 | 技术 |
|------|------|
| Web 框架 | FastAPI |
| 参数验证 | Pydantic |
| 文档 | Swagger UI |
| 服务器 | Uvicorn |

---

## 第二部分 - 实现步骤

### 2.1 安装依赖

```bash
pip install fastapi uvicorn pydantic
```

### 2.2 定义数据模型

```python
# schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class StockInfoSchema(BaseModel):
    """股票基本信息"""
    stock_code: str
    stock_name: str
    industry: Optional[str] = None

class StockDailySchema(BaseModel):
    """股票日线数据"""
    stock_code: str
    trade_date: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    amount: Optional[float] = None
    change: Optional[float] = None

class StockQuerySchema(BaseModel):
    """股票查询参数"""
    stock_code: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    limit: Optional[int] = 100
```

### 2.3 创建 API 服务

```python
# main.py
from fastapi import FastAPI, HTTPException, Query
from typing import Optional, List
from datetime import datetime
import pandas as pd
from repository import StockRepository

app = FastAPI(
    title="股票数据 API",
    description="提供股票数据查询服务",
    version="1.0.0"
)

# 初始化数据仓库
repo = StockRepository()

@app.get("/")
def root():
    """根路径"""
    return {"message": "股票数据 API 服务", "version": "1.0.0"}

@app.get("/stocks")
def get_all_stocks():
    """获取所有股票列表"""
    stocks = repo.get_all_stocks()
    return {
        "code": 200,
        "data": [
            {
                "stock_code": s.stock_code,
                "stock_name": s.stock_name,
                "industry": s.industry
            }
            for s in stocks
        ]
    }

@app.get("/stock/{stock_code}")
def get_stock_info(stock_code: str):
    """获取股票基本信息"""
    stock = repo.get_stock_by_code(stock_code)
    if not stock:
        raise HTTPException(status_code=404, detail="股票不存在")

    return {
        "code": 200,
        "data": {
            "stock_code": stock.stock_code,
            "stock_name": stock.stock_name,
            "industry": stock.industry
        }
    }

@app.get("/stock/{stock_code}/daily")
def get_stock_daily(
    stock_code: str,
    start_date: Optional[str] = Query(None, description="开始日期 YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="结束日期 YYYY-MM-DD"),
    limit: int = Query(100, ge=1, le=1000, description="返回记录数")
):
    """获取股票历史日线数据"""
    try:
        df = repo.get_daily_data(stock_code, start_date, end_date)

        if df.empty:
            return {"code": 200, "data": [], "message": "暂无数据"}

        # 限制返回数量
        df = df.tail(limit)

        # 转换日期格式
        df['date'] = df['date'].dt.strftime('%Y-%m-%d')

        return {
            "code": 200,
            "data": df.to_dict(orient='records'),
            "total": len(df)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stock/{stock_code}/realtime")
def get_stock_realtime(stock_code: str):
    """获取股票实时行情"""
    import requests

    url = f"https://qt.gtimg.cn/q={stock_code}"
    response = requests.get(url)
    response.encoding = 'gbk'

    data = response.text.split("~")
    if not data or data == "null":
        raise HTTPException(status_code=404, detail="股票不存在")

    return {
        "code": 200,
        "data": {
            "stock_code": stock_code,
            "stock_name": data[1],
            "price": float(data[3]),
            "change": float(data[4]),
            "percent": float(data[5]),
            "volume": float(data[6]),
            "amount": float(data[7]),
            "open": float(data[8]),
            "high": float(data[9]),
            "low": float(data[10]),
            "close": float(data[30])
        }
    }

@app.get("/stock/{stock_code}/stats")
def get_stock_stats(stock_code: str, days: int = Query(30, ge=1, le=365)):
    """获取股票统计信息"""
    stats = repo.get_stock_stats(stock_code, days)

    return {
        "code": 200,
        "data": {
            "stock_code": stock_code,
            "period_days": days,
            "avg_price": round(stats['avg_price'], 2) if stats['avg_price'] else None,
            "max_price": stats['max_price'],
            "min_price": stats['min_price'],
            "total_volume": stats['total_volume'],
            "trading_days": stats['days']
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 2.4 运行服务

```bash
# 启动服务
python main.py

# 访问 API 文档
# http://localhost:8000/docs

# 访问 ReDoc 文档
# http://localhost:8000/redoc
```

---

## 第三部分 - 扩展功能

### 3.1 添加缓存

```python
from fastapi import APIRouter
from functools import lru_cache
import time

# 简单内存缓存
cache = {}
CACHE_TTL = 60  # 60秒

def get_cached(key: str):
    """获取缓存"""
    if key in cache:
        timestamp, value = cache[key]
        if time.time() - timestamp < CACHE_TTL:
            return value
    return None

def set_cache(key: str, value):
    """设置缓存"""
    cache[key] = (time.time(), value)

@app.get("/stock/{stock_code}/realtime")
def get_stock_realtime(stock_code: str):
    # 先检查缓存
    cache_key = f"realtime_{stock_code}"
    cached = get_cached(cache_key)
    if cached:
        return cached

    # ... 获取数据

    # 设置缓存
    set_cache(cache_key, result)
    return result
```

### 3.2 错误处理

```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理"""
    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "message": f"服务器内部错误：{str(exc)}"
        }
    )
```

### 3.3 CORS 跨域

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 第四部分 - 项目总结

### 学到的技能

| 技能 | 说明 |
|------|------|
| FastAPI 基础 | 路由和参数定义 |
| Pydantic 模型 | 数据验证 |
| RESTful 设计 | API 设计规范 |
| Swagger 文档 | 自动生成 API 文档 |
| 缓存机制 | 内存缓存实现 |
| 错误处理 | 全局异常处理 |

### 下一步

在 [项目五](./05-股票监控平台.md) 中，我们将：
- 实现定时任务采集数据
- 添加价格监控和告警
- 实现邮件/短信通知

---

[← 上一篇](./03-数据存储与管理.md) | [下一篇 →](./05-股票监控平台.md)