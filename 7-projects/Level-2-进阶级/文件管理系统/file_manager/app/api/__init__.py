"""API 路由"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from ..core import get_db
from ..services import FileService

router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """上传文件"""
    record = await FileService.save_file(db, file)
    return {
        "id": record.id,
        "filename": record.original_name,
        "size": record.file_size
    }


@router.get("/files")
def get_files(db: Session = Depends(get_db)):
    """获取文件列表"""
    files = FileService.get_all(db)
    return [{"id": f.id, "filename": f.original_name, "size": f.file_size} for f in files]


@router.get("/download/{file_id}")
def download_file(file_id: int, db: Session = Depends(get_db)):
    """下载文件"""
    record = FileService.get_file(db, file_id)
    if not record:
        raise HTTPException(status_code=404, detail="文件不存在")
    
    return FileResponse(
        path=record.file_path,
        filename=record.original_name,
        media_type=record.mime_type
    )


@router.delete("/files/{file_id}")
def delete_file(file_id: int, db: Session = Depends(get_db)):
    """删除文件"""
    if not FileService.delete_file(db, file_id):
        raise HTTPException(status_code=404, detail="文件不存在")
    return {"message": "删除成功"}