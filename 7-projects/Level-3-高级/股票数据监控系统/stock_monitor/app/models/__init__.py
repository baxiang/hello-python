"""数据模型"""

from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from ..core import Base


class Stock(Base):
    """股票模型"""
    __tablename__ = "stocks"
    
    id = Column(Integer, primary_key=True)
    symbol = Column(String(20), unique=True, nullable=False)
    name = Column(String(100))
    exchange = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)


class StockPrice(Base):
    """股票价格"""
    __tablename__ = "stock_prices"
    
    id = Column(Integer, primary_key=True)
    stock_id = Column(Integer)
    symbol = Column(String(20))
    price = Column(Float)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    volume = Column(Integer)
    change = Column(Float)
    change_percent = Column(Float)
    recorded_at = Column(DateTime, default=datetime.utcnow)