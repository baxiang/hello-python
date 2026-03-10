# 项目三：日志 API 服务

> 掌握 FastAPI 日志查询接口设计

---

## 项目目标

- 掌握 FastAPI 框架
- 设计日志查询 API
- 实现分页和过滤
- API 文档

---

## 第一部分 - API 设计

```
日志 API
├── GET  /logs              # 日志列表
├── GET  /logs/{id}         # 日志详情
├── GET  /logs/stats        # 统计信息
├── GET  /logs/errors       # 错误日志
├── GET  /logs/slow         # 慢请求
├── GET  /logs/search       # 搜索
├── POST /logs              # 添加日志
├── POST /logs/batch        # 批量导入
└── DELETE /logs/cleanup    # 清理旧日志
```

---

## 第二部分 - 实现步骤

### 2.1 Pydantic 模型

```python
# schemas.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class LogBase(BaseModel):
    timestamp: datetime
    level: str = "INFO"
    ip: str
    method: str
    path: str
    status: int
    response_time: int = 0
    user_agent: Optional[str] = None
    size: int = 0


class LogCreate(LogBase):
    pass


class LogResponse(LogBase):
    id: int

    class Config:
        from_attributes = True


class LogListResponse(BaseModel):
    items: List[LogResponse]
    total: int
    page: int
    page_size: int


class LogStatsResponse(BaseModel):
    total_count: int
    status_distribution: dict
    top_ips: List[dict]
    top_paths: List[dict]
    response_time_stats: dict
    error_count: int
    slow_request_count: int


class LogQueryParams(BaseModel):
    """日志查询参数"""
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    ip: Optional[str] = None
    status: Optional[int] = None
    path: Optional[str] = None
    keyword: Optional[str] = None
    page: int = 1
    page_size: int = 20
```

### 2.2 API 路由

```python
# main.py
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, timedelta

from database import get_db, init_db
from models import AccessLog
from services import LogStorageService, StatisticsService

app = FastAPI(title="日志分析 API", version="1.0.0")


@app.on_event("startup")
def startup():
    init_db()


# 日志列表
@app.get("/logs", response_model=LogListResponse)
def get_logs(
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    ip: Optional[str] = Query(None),
    status: Optional[int] = Query(None),
    path: Optional[str] = Query(None),
    keyword: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """获取日志列表"""
    service = LogStorageService(db)

    offset = (page - 1) * page_size
    logs, total = service.query_logs(
        start_time=start_time,
        end_time=end_time,
        ip=ip,
        status=status,
        path=path,
        keyword=keyword,
        limit=page_size,
        offset=offset
    )

    return LogListResponse(
        items=logs,
        total=total,
        page=page,
        page_size=page_size
    )


# 日志详情
@app.get("/logs/{log_id}", response_model=LogResponse)
def get_log(log_id: int, db: Session = Depends(get_db)):
    """获取日志详情"""
    log = db.query(AccessLog).filter(AccessLog.id == log_id).first()

    if not log:
        raise HTTPException(status_code=404, detail="日志不存在")

    return log


# 统计信息
@app.get("/logs/stats", response_model=LogStatsResponse)
def get_stats(
    hours: int = Query(24, ge=1, le=168),
    db: Session = Depends(get_db)
):
    """获取统计信息"""
    start_time = datetime.now() - timedelta(hours=hours)

    stats_service = StatisticsService(db)

    return LogStatsResponse(
        total_count=stats_service.get_total_count(start_time=start_time),
        status_distribution=stats_service.get_status_distribution(start_time=start_time),
        top_ips=stats_service.get_top_ips(limit=10, start_time=start_time),
        top_paths=stats_service.get_top_paths(limit=10, start_time=start_time),
        response_time_stats=stats_service.get_response_time_stats(start_time=start_time),
        error_count=db.query(AccessLog).filter(
            AccessLog.timestamp >= start_time,
            AccessLog.status >= 400
        ).count(),
        slow_request_count=db.query(AccessLog).filter(
            AccessLog.timestamp >= start_time,
            AccessLog.response_time >= 1000
        ).count()
    )


# 错误日志
@app.get("/logs/errors", response_model=LogListResponse)
def get_error_logs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """获取错误日志"""
    service = LogStorageService(db)
    offset = (page - 1) * page_size

    logs = service.get_error_logs(limit=page_size)
    total = len(logs)  # 简化处理

    return LogListResponse(
        items=logs,
        total=total,
        page=page,
        page_size=page_size
    )


# 慢请求
@app.get("/logs/slow", response_model=LogListResponse)
def get_slow_requests(
    threshold: int = Query(1000, ge=100, le=30000),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """获取慢请求"""
    service = LogStorageService(db)
    offset = (page - 1) * page_size

    logs = service.get_slow_requests(threshold=threshold, limit=page_size)

    return LogListResponse(
        items=logs,
        total=len(logs),
        page=page,
        page_size=page_size
    )


# 搜索
@app.get("/logs/search", response_model=LogListResponse)
def search_logs(
    keyword: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """搜索日志"""
    service = LogStorageService(db)
    offset = (page - 1) * page_size

    logs, total = service.query_logs(
        keyword=keyword,
        limit=page_size,
        offset=offset
    )

    return LogListResponse(
        items=logs,
        total=total,
        page=page,
        page_size=page_size
    )


# 添加日志
@app.post("/logs", response_model=LogResponse)
def create_log(log_data: LogCreate, db: Session = Depends(get_db)):
    """添加日志"""
    service = LogStorageService(db)
    log = service.save_log(log_data.model_dump())
    return log


# 批量导入
@app.post("/logs/batch")
def batch_import_logs(logs: List[LogCreate], db: Session = Depends(get_db)):
    """批量导入日志"""
    service = LogStorageService(db)
    log_dicts = [log.model_dump() for log in logs]
    count = service.batch_save_logs(log_dicts)
    return {"message": f"成功导入 {count} 条日志"}


# 清理旧日志
@app.delete("/logs/cleanup")
def cleanup_logs(days: int = Query(30, ge=1, le=365), db: Session = Depends(get_db)):
    """清理旧日志"""
    service = LogStorageService(db)
    count = service.delete_old_logs(days)
    return {"message": f"已删除 {count} 条 {days} 天前的日志"}


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

### 3.1 实时日志导入

```python
# 导入模拟日志
@app.post("/logs/import")
def import_from_file(
    file_path: str = Query(...),
    db: Session = Depends(get_db)
):
    """从文件导入日志"""
    from log_parser import LogParser

    logs = LogParser.parse_file(file_path)
    service = LogStorageService(db)
    count = service.batch_save_logs(logs)

    return {"message": f"成功导入 {count} 条日志"}
```

### 3.2 导出功能

```python
@app.get("/logs/export")
def export_logs(
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    format: str = Query("json", regex="^(json|csv)$"),
    db: Session = Depends(get_db)
):
    """导出日志"""
    service = LogStorageService(db)
    logs, _ = service.query_logs(
        start_time=start_time,
        end_time=end_time,
        limit=10000
    )

    if format == "csv":
        import csv
        import io

        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=[
            "timestamp", "ip", "method", "path", "status", "response_time"
        ])
        writer.writeheader()

        for log in logs:
            writer.writerow({
                "timestamp": log.timestamp,
                "ip": log.ip,
                "method": log.method,
                "path": log.path,
                "status": log.status,
                "response_time": log.response_time
            })

        return Response(
            content=output.getvalue(),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=logs.csv"}
        )

    return [{"timestamp": str(log.timestamp), "ip": log.ip,
             "method": log.method, "path": log.path,
             "status": log.status, "response_time": log.response_time}
            for log in logs]
```

---

## 第四部分 - 项目总结

### 学到的技能

| 技能 | 说明 |
|------|------|
| FastAPI | Web 框架 |
| RESTful | API 设计 |
| 分页 | 列表分页 |
| 过滤查询 | 条件查询 |
| 导出 | CSV/JSON 导出 |

### 下一步

在 [项目四](./04-日志分析系统.md) 中，我们将：
- 实时统计
- 告警功能
- 定时任务

---

[← 上一篇](./02-日志存储服务.md) | [下一篇 →](./04-日志分析系统.md)