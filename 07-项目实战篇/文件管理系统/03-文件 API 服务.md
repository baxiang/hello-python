# 项目三：文件 API 服务

> 掌握 FastAPI 文件上传下载接口

---

## 项目目标

- FastAPI 文件上传
- 文件下载
- 目录操作 API
- 批量操作

---

## 第一部分 - API 设计

```
文件 API
├── 文件操作
│   ├── GET  /files                    # 文件列表
│   ├── GET  /files/{id}               # 文件详情
│   ├── POST /files                    # 创建文件/目录
│   ├── PUT  /files/{id}               # 更新文件
│   ├── DELETE /files/{id}             # 删除文件
│   ├── POST /files/{id}/move           # 移动文件
│   ├── POST /files/{id}/copy           # 复制文件
├── 上传下载
│   ├── POST /files/upload             # 上传文件
│   ├── GET  /files/{id}/download      # 下载文件
├── 搜索
│   ├── GET  /files/search             # 搜索文件
│   ├── GET  /files/starred            # 收藏文件
└── 统计
    └── GET  /files/stats               # 存储统计
```

---

## 第二部分 - 实现步骤

### 2.1 Pydantic 模型

```python
# schemas.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class FileBase(BaseModel):
    name: str
    parent_id: Optional[int] = None
    description: Optional[str] = None


class FileCreate(BaseModel):
    name: str
    parent_id: Optional[int] = None
    is_directory: bool = False
    description: Optional[str] = None


class FileUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_starred: Optional[bool] = None


class FileResponse(BaseModel):
    id: int
    name: str
    path: str
    parent_id: Optional[int]
    size: int
    mime_type: Optional[str]
    extension: Optional[str]
    is_directory: bool
    is_starred: bool
    is_hidden: bool
    owner_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class FileListResponse(BaseModel):
    items: List[FileResponse]
    total: int


class FileStatsResponse(BaseModel):
    total_size: int
    file_count: int
    type_distribution: dict
```

### 2.2 API 路由

```python
# main.py
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Optional, List
import os
import shutil
from pathlib import Path

from database import get_db, init_db
from models import FileRecord
from services import FileStorageService, FileStatisticsService

app = FastAPI(title="文件管理 API", version="1.0.0")

# 上传目录
UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.on_event("startup")
def startup():
    init_db()


# 获取文件列表
@app.get("/files", response_model=FileListResponse)
def get_files(
    parent_id: Optional[int] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """获取文件列表"""
    service = FileStorageService(db)
    files = service.get_files_by_parent(parent_id)

    return FileListResponse(
        items=files,
        total=len(files)
    )


# 获取文件详情
@app.get("/files/{file_id}", response_model=FileResponse)
def get_file(file_id: int, db: Session = Depends(get_db)):
    """获取文件详情"""
    service = FileStorageService(db)
    file = service.get_file(file_id)

    if not file:
        raise HTTPException(status_code=404, detail="文件不存在")

    return file


# 创建文件/目录
@app.post("/files", response_model=FileResponse)
def create_file(
    data: FileCreate,
    db: Session = Depends(get_db)
):
    """创建文件或目录"""
    service = FileStorageService(db)

    # 如果是目录，创建实际目录
    if data.is_directory:
        parent_path = ""
        if data.parent_id:
            parent = service.get_file(data.parent_id)
            if parent:
                parent_path = parent.path

        full_path = os.path.join(UPLOAD_DIR, parent_path, data.name)

        if os.path.exists(full_path):
            raise HTTPException(status_code=400, detail="文件已存在")

        os.makedirs(full_path, exist_ok=True)

    # 创建数据库记录
    parent_path = ""
    if data.parent_id:
        parent = service.get_file(data.parent_id)
        if parent:
            parent_path = parent.path

    file_path = os.path.join(UPLOAD_DIR, parent_path, data.name)

    file = service.create_file(
        name=data.name,
        path=file_path,
        parent_id=data.parent_id,
        is_directory=data.is_directory,
        owner_id=1  # 从认证获取
    )

    return file


# 更新文件
@app.put("/files/{file_id}", response_model=FileResponse)
def update_file(
    file_id: int,
    data: FileUpdate,
    db: Session = Depends(get_db)
):
    """更新文件"""
    service = FileStorageService(db)

    update_data = data.model_dump(exclude_unset=True)
    file = service.update_file(file_id, **update_data)

    if not file:
        raise HTTPException(status_code=404, detail="文件不存在")

    return file


# 删除文件
@app.delete("/files/{file_id}")
def delete_file(
    file_id: int,
    permanent: bool = Query(False),
    db: Session = Depends(get_db)
):
    """删除文件"""
    service = FileStorageService(db)
    file = service.get_file(file_id)

    if not file:
        raise HTTPException(status_code=404, detail="文件不存在")

    # 删除实际文件
    if os.path.exists(file.path):
        if file.is_directory:
            shutil.rmtree(file.path)
        else:
            os.remove(file.path)

    # 删除数据库记录
    service.delete_file(file_id, permanent)

    return {"message": "删除成功"}


# 上传文件
@app.post("/files/upload", response_model=FileResponse)
async def upload_file(
    file: UploadFile = File(...),
    parent_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """上传文件"""
    service = FileStorageService(db)

    # 获取父目录路径
    parent_path = ""
    if parent_id:
        parent = service.get_file(parent_id)
        if parent:
            parent_path = parent.path

    # 保存文件
    file_path = os.path.join(UPLOAD_DIR, parent_path, file.filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    content = await file.read()
    with open(file_path, 'wb') as f:
        f.write(content)

    # 创建数据库记录
    file_record = service.create_file(
        name=file.filename,
        path=file_path,
        parent_id=parent_id,
        size=len(content),
        mime_type=file.content_type,
        owner_id=1
    )

    return file_record


# 下载文件
@app.get("/files/{file_id}/download")
def download_file(file_id: int, db: Session = Depends(get_db)):
    """下载文件"""
    service = FileStorageService(db)
    file = service.get_file(file_id)

    if not file:
        raise HTTPException(status_code=404, detail="文件不存在")

    if file.is_directory:
        raise HTTPException(status_code=400, detail="目录不支持下载")

    if not os.path.exists(file.path):
        raise HTTPException(status_code=404, detail="文件不存在")

    return FileResponse(
        path=file.path,
        filename=file.name,
        media_type=file.mime_type
    )


# 搜索文件
@app.get("/files/search", response_model=FileListResponse)
def search_files(
    keyword: str = Query(..., min_length=1),
    file_type: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """搜索文件"""
    service = FileStorageService(db)
    files = service.search_files(
        keyword=keyword,
        file_type=file_type,
        limit=limit
    )

    return FileListResponse(
        items=files,
        total=len(files)
    )


# 获取收藏文件
@app.get("/files/starred", response_model=FileListResponse)
def get_starred_files(db: Session = Depends(get_db)):
    """获取收藏文件"""
    files = db.query(FileRecord).filter(
        FileRecord.is_starred == True,
        FileRecord.deleted_at == None
    ).all()

    return FileListResponse(
        items=files,
        total=len(files)
    )


# 获取存储统计
@app.get("/files/stats", response_model=FileStatsResponse)
def get_stats(db: Session = Depends(get_db)):
    """获取存储统计"""
    service = FileStatisticsService(db)

    usage = service.get_storage_usage()
    distribution = service.get_file_type_distribution()

    return FileStatsResponse(
        total_size=usage["total_size"],
        file_count=usage["file_count"],
        type_distribution=distribution
    )


# 移动文件
@app.post("/files/{file_id}/move")
def move_file(
    file_id: int,
    new_parent_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """移动文件"""
    service = FileStorageService(db)

    if service.move_file(file_id, new_parent_id):
        return {"message": "移动成功"}

    raise HTTPException(status_code=400, detail="移动失败")


# 健康检查
@app.get("/health")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## 第三部分 - 扩展功能

### 3.1 批量上传

```python
@app.post("/files/upload/batch")
async def upload_multiple_files(
    files: List[UploadFile] = File(...),
    parent_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """批量上传文件"""
    service = FileStorageService(db)
    results = []

    for file in files:
        content = await file.read()
        file_path = os.path.join(UPLOAD_DIR, str(parent_id or ""), file.filename)

        with open(file_path, 'wb') as f:
            f.write(content)

        file_record = service.create_file(
            name=file.filename,
            path=file_path,
            parent_id=parent_id,
            size=len(content),
            mime_type=file.content_type
        )

        results.append({"name": file.filename, "id": file_record.id})

    return {"uploaded": len(results), "files": results}
```

### 3.2 批量删除

```python
@app.post("/files/batch-delete")
def batch_delete_files(
    file_ids: List[int],
    db: Session = Depends(get_db)
):
    """批量删除文件"""
    service = FileStorageService(db)
    count = 0

    for file_id in file_ids:
        if service.delete_file(file_id):
            count += 1

    return {"deleted": count}
```

---

## 第四部分 - 项目总结

### 学到的技能

| 技能 | 说明 |
|------|------|
| FastAPI | Web 框架 |
| 文件上传 | UploadFile |
| 文件下载 | FileResponse |
| 批量操作 | 批量上传删除 |

### 下一步

在 [项目四](./04-文件管理系统.md) 中，我们将：
- 权限管理
- 文件分享
- 回收站

---

[← 上一篇](./02-文件存储服务.md) | [下一篇 →](./04-文件管理系统.md)