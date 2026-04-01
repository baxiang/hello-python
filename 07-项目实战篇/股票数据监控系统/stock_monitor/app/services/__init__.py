"""股票服务"""

import httpx
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from .config import config
from .models import Stock, StockPrice


class StockService:
    """股票服务"""
    
    @staticmethod
    async def fetch_price(symbol: str) -> dict:
        """获取股票价格"""
        # 模拟 API 调用
        url = f"{config.API_URL}/quote"
        params = {"symbol": symbol, "apikey": config.API_KEY}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
    
    @staticmethod
    def save_price(db: Session, data: dict) -> StockPrice:
        """保存价格记录"""
        record = StockPrice(
            symbol=data["symbol"],
            price=data["price"],
            open=data.get("open"),
            high=data.get("high"),
            low=data.get("low"),
            volume=data.get("volume"),
            change=data.get("change"),
            change_percent=data.get("change_percent")
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record
    
    @staticmethod
    def add_stock(db: Session, symbol: str, name: str = None, exchange: str = None) -> Stock:
        """添加股票"""
        stock = Stock(symbol=symbol, name=name, exchange=exchange)
        db.add(stock)
        db.commit()
        db.refresh(stock)
        return stock
    
    @staticmethod
    def get_stocks(db: Session) -> list[Stock]:
        """获取所有股票"""
        return db.query(Stock).all()
    
    @staticmethod
    def get_history(db: Session, symbol: str, limit: int = 30) -> list[StockPrice]:
        """获取历史价格"""
        return db.query(StockPrice).filter(
            StockPrice.symbol == symbol
        ).order_by(StockPrice.recorded_at.desc()).limit(limit).all()
    
    @staticmethod
    def get_latest(db: Session, symbol: str) -> Optional[StockPrice]:
        """获取最新价格"""
        return db.query(StockPrice).filter(
            StockPrice.symbol == symbol
        ).order_by(StockPrice.recorded_at.desc()).first()