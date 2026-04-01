"""文件服务"""

import os
import uuid
from pathlib import Path
from sqlalchemy.orm import Session
from fastapi import UploadFile
from .models import FileRecord


class FileService:
    """文件服务"""
    
    UPLOAD_DIR = Path("uploads")
    
    @classmethod
    def init_upload_dir(cls):
        cls.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    async def save_file(db: Session, file: UploadFile) -> FileRecord:
        """保存文件"""
        FileService.init_upload_dir()
        
        # 生成唯一文件名
        ext = Path(file.filename).suffix
        unique_name = f"{uuid.uuid4()}{ext}"
        file_path = FileService.UPLOAD_DIR / unique_name
        
        # 保存文件
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        
        # 创建记录
        record = FileRecord(
            filename=unique_name,
            original_name=file.filename,
            file_path=str(file_path),
            file_size=len(content),
            mime_type=file.content_type
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        
        return record
    
    @staticmethod
    def get_file(db: Session, file_id: int) -> FileRecord | None:
        """获取文件"""
        return db.query(FileRecord).filter(FileRecord.id == file_id).first()
    
    @staticmethod
    def get_all(db: Session) -> list[FileRecord]:
        """获取所有文件"""
        return db.query(FileRecord).order_by(FileRecord.uploaded_at.desc()).all()
    
    @staticmethod
    def delete_file(db: Session, file_id: int) -> bool:
        """删除文件"""
        record = FileService.get_file(db, file_id)
        if not record:
            return False
        
        # 删除物理文件
        file_path = Path(record.file_path)
        if file_path.exists():
            file_path.unlink()
        
        # 删除记录
        db.delete(record)
        db.commit()
        return True