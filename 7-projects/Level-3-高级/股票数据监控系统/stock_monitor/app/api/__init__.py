"""API 路由"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core import get_db
from ..services import StockService

router = APIRouter()


@router.get("/stocks")
def get_stocks(db: Session = Depends(get_db)):
    """获取股票列表"""
    stocks = StockService.get_stocks(db)
    return [{"symbol": s.symbol, "name": s.name} for s in stocks]


@router.post("/stocks")
def add_stock(symbol: str, name: str = None, db: Session = Depends(get_db)):
    """添加股票"""
    return StockService.add_stock(db, symbol, name)


@router.get("/stocks/{symbol}/price")
async def get_price(symbol: str, db: Session = Depends(get_db)):
    """获取当前价格"""
    try:
        data = await StockService.fetch_price(symbol)
        record = StockService.save_price(db, data)
        return {
            "symbol": symbol,
            "price": data["price"],
            "change": data.get("change"),
            "change_percent": data.get("change_percent")
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/stocks/{symbol}/history")
def get_history(symbol: str, limit: int = 30, db: Session = Depends(get_db)):
    """获取历史价格"""
    records = StockService.get_history(db, symbol, limit)
    return [
        {
            "price": r.price,
            "change": r.change,
            "recorded_at": r.recorded_at
        }
        for r in records
    ]


@router.get("/stocks/{symbol}/latest")
def get_latest(symbol: str, db: Session = Depends(get_db)):
    """获取最新价格"""
    record = StockService.get_latest(db, symbol)
    if not record:
        raise HTTPException(status_code=404, detail="无数据")
    return {
        "symbol": symbol,
        "price": record.price,
        "change": record.change,
        "recorded_at": record.recorded_at
    }