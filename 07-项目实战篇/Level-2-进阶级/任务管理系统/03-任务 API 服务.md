# 项目三：任务 API 服务

> 掌握 FastAPI 和 RESTful API 设计

---

## 项目目标

- 掌握 FastAPI 框架
- 学会设计 RESTful API
- 掌握 Pydantic 数据验证
- 理解分页和过滤

---

## 第一部分 - 需求分析

### API 设计

```
任务管理 API
├── GET    /tasks              # 获取任务列表
├── POST   /tasks              # 创建任务
├── GET    /tasks/{id}         # 获取任务详情
├── PUT    /tasks/{id}         # 更新任务
├── DELETE /tasks/{id}         # 删除任务
├── POST   /tasks/{id}/complete    # 完成任务
├── GET    /categories         # 获取分类列表
├── POST   /categories         # 创建分类
├── GET    /tags               # 获取标签列表
└── POST   /tags               # 创建标签
```

---

## 第二部分 - 实现步骤

### 2.1 安装依赖

```bash
pip install fastapi uvicorn pydantic
```

### 2.2 Pydantic 模型

```python
# schemas.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class PriorityEnum(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TaskStatusEnum(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class CategoryBase(BaseModel):
    """分类基础模型"""
    name: str = Field(..., min_length=1, max_length=50)
    color: str = Field(default="#3498db", pattern=r"^#[0-9A-Fa-f]{6}$")


class CategoryCreate(CategoryBase):
    """创建分类"""
    pass


class CategoryResponse(CategoryBase):
    """分类响应"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class TagBase(BaseModel):
    """标签基础模型"""
    name: str = Field(..., min_length=1, max_length=50)
    color: str = Field(default="#95a5a6", pattern=r"^#[0-9A-Fa-f]{6}$")


class TagCreate(TagBase):
    """创建标签"""
    pass


class TagResponse(TagBase):
    """标签响应"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class TaskBase(BaseModel):
    """任务基础模型"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    priority: PriorityEnum = PriorityEnum.MEDIUM
    category_id: Optional[int] = None
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    """创建任务"""
    tag_ids: Optional[List[int]] = None


class TaskUpdate(BaseModel):
    """更新任务"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    priority: Optional[PriorityEnum] = None
    category_id: Optional[int] = None
    due_date: Optional[datetime] = None
    tag_ids: Optional[List[int]] = None


class TaskResponse(TaskBase):
    """任务响应"""
    id: int
    completed: bool
    status: TaskStatusEnum
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    category: Optional[CategoryResponse] = None
    tags: List[TagResponse] = []

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    """任务列表响应"""
    items: List[TaskResponse]
    total: int
    page: int
    page_size: int


class TaskStatisticsResponse(BaseModel):
    """任务统计响应"""
    total: int
    completed: int
    pending: int
    completion_rate: float
    priority_stats: dict
    overdue: int
```

### 2.3 API 路由

```python
# main.py
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime

from database import get_db, init_db
from models import Task, Category, Tag, Priority, TaskStatus
from services import TaskService, CategoryService, TagService
from schemas import (
    TaskCreate, TaskUpdate, TaskResponse, TaskListResponse,
    CategoryCreate, CategoryResponse,
    TagCreate, TagResponse,
    TaskStatisticsResponse,
    PriorityEnum, TaskStatusEnum
)

app = FastAPI(title="任务管理 API", version="1.0.0")


@app.on_event("startup")
def startup():
    init_db()


# 任务路由
@app.get("/tasks", response_model=TaskListResponse)
def get_tasks(
    category_id: Optional[int] = None,
    priority: Optional[PriorityEnum] = None,
    status: Optional[TaskStatusEnum] = None,
    completed: Optional[bool] = None,
    keyword: Optional[str] = None,
    tag_id: Optional[int] = None,
    due_date_before: Optional[datetime] = None,
    due_date_after: Optional[datetime] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    order_by: str = Query("created_at"),
    desc: bool = Query(True),
    db: Session = Depends(get_db)
):
    """获取任务列表"""
    service = TaskService(db)

    # 转换枚举
    priority_enum = Priority[priority.value.upper()] if priority else None
    status_enum = TaskStatus[status.value.upper()] if status else None

    skip = (page - 1) * page_size
    tasks, total = service.get_tasks(
        category_id=category_id,
        priority=priority_enum,
        status=status_enum,
        completed=completed,
        keyword=keyword,
        tag_id=tag_id,
        due_date_before=due_date_before,
        due_date_after=due_date_after,
        skip=skip,
        limit=page_size,
        order_by=order_by,
        desc=desc
    )

    return TaskListResponse(
        items=tasks,
        total=total,
        page=page,
        page_size=page_size
    )


@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db)
):
    """创建任务"""
    service = TaskService(db)

    # 转换枚举
    priority_enum = Priority[task_data.priority.value.upper()]

    task = service.create_task(
        title=task_data.title,
        description=task_data.description,
        priority=priority_enum,
        category_id=task_data.category_id,
        due_date=task_data.due_date,
        tag_ids=task_data.tag_ids
    )

    return task


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """获取任务详情"""
    service = TaskService(db)
    task = service.get_task(task_id)

    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    return task


@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db)
):
    """更新任务"""
    service = TaskService(db)

    # 转换更新数据
    update_dict = task_data.model_dump(exclude_unset=True)
    if "priority" in update_dict and update_dict["priority"]:
        update_dict["priority"] = Priority[update_dict["priority"].value.upper()]

    task = service.update_task(task_id, **update_dict)

    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    return task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """删除任务"""
    service = TaskService(db)

    if not service.delete_task(task_id):
        raise HTTPException(status_code=404, detail="任务不存在")

    return {"message": "删除成功"}


@app.post("/tasks/{task_id}/complete", response_model=TaskResponse)
def complete_task(task_id: int, db: Session = Depends(get_db)):
    """完成任务"""
    service = TaskService(db)
    task = service.complete_task(task_id)

    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")

    return task


@app.get("/tasks/statistics", response_model=TaskStatisticsResponse)
def get_statistics(
    category_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """获取任务统计"""
    service = TaskService(db)
    stats = service.get_statistics(category_id)

    return TaskStatisticsResponse(**stats)


# 分类路由
@app.get("/categories", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    """获取分类列表"""
    service = CategoryService(db)
    return service.get_categories()


@app.post("/categories", response_model=CategoryResponse, status_code=201)
def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db)
):
    """创建分类"""
    service = CategoryService(db)
    return service.create_category(
        name=category_data.name,
        color=category_data.color
    )


# 标签路由
@app.get("/tags", response_model=List[TagResponse])
def get_tags(db: Session = Depends(get_db)):
    """获取标签列表"""
    service = TagService(db)
    return service.get_tags()


@app.post("/tags", response_model=TagResponse, status_code=201)
def create_tag(
    tag_data: TagCreate,
    db: Session = Depends(get_db)
):
    """创建标签"""
    service = TagService(db)
    return service.create_tag(
        name=tag_data.name,
        color=tag_data.color
    )


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

### 3.1 批量操作

```python
@app.post("/tasks/batch-complete")
def batch_complete(
    task_ids: List[int],
    db: Session = Depends(get_db)
):
    """批量完成任务"""
    service = TaskService(db)
    count = service.batch_complete(task_ids)
    return {"message": f"已完成 {count} 个任务"}


@app.post("/tasks/batch-delete")
def batch_delete(
    task_ids: List[int],
    db: Session = Depends(get_db)
):
    """批量删除任务"""
    service = TaskService(db)
    count = service.batch_delete(task_ids)
    return {"message": f"已删除 {count} 个任务"}


@app.post("/tasks/batch-move")
def batch_move(
    task_ids: List[int],
    category_id: int,
    db: Session = Depends(get_db)
):
    """批量移动分类"""
    service = TaskService(db)
    count = service.batch_move_category(task_ids, category_id)
    return {"message": f"已移动 {count} 个任务"}
```

### 3.2 导出功能

```python
@app.get("/tasks/export")
def export_tasks(
    format: str = Query("json", regex="^(json|csv)$"),
    db: Session = Depends(get_db)
):
    """导出任务"""
    service = TaskService(db)
    tasks, _ = service.get_tasks(limit=10000)

    if format == "csv":
        import csv
        import io

        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=[
            "id", "title", "description", "priority",
            "completed", "category_id", "due_date", "created_at"
        ])
        writer.writeheader()

        for task in tasks:
            writer.writerow({
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "priority": task.priority.value,
                "completed": task.completed,
                "category_id": task.category_id,
                "due_date": task.due_date,
                "created_at": task.created_at
            })

        return Response(
            content=output.getvalue(),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=tasks.csv"}
        )

    return tasks
```

---

## 第四部分 - 项目总结

### 学到的技能

| 技能 | 说明 |
|------|------|
| FastAPI | Web 框架 |
| RESTful | API 设计规范 |
| Pydantic | 数据验证 |
| 分页 | 列表分页 |
| 批量操作 | 批量增删改 |

### 下一步

在 [项目四](./04-团队协作系统.md) 中，我们将：
- 多用户支持
- 权限管理
- 任务分享
- 评论功能

---

[← 上一篇](./02-任务管理服务.md) | [下一篇 →](./04-团队协作系统.md)