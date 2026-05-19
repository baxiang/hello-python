"""数据模型"""

from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime
from ..core import Base


class FileRecord(Base):
    """文件记录"""
    __tablename__ = "files"
    
    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=False)
    original_name = Column(String(255))
    file_path = Column(String(500), nullable=False)
    file_size = Column(Float)
    mime_type = Column(String(100))
    uploaded_at = Column(DateTime, default=datetime.utcnow)