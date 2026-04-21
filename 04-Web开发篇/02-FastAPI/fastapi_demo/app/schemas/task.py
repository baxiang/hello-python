"""任务Pydantic模型"""

from datetime import datetime

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    """任务创建模型"""

    title: str = Field(..., min_length=1, max_length=200, description="任务标题")
    description: str | None = Field(None, max_length=1000, description="任务描述")
    status: str = Field("draft", description="状态: draft/pending/in_progress/completed")
    priority: str = Field("medium", description="优先级: low/medium/high")


class TaskUpdate(BaseModel):
    """任务更新模型"""

    title: str | None = Field(None, min_length=1, max_length=200, description="任务标题")
    description: str | None = Field(None, max_length=1000, description="任务描述")
    status: str | None = Field(None, description="状态: draft/pending/in_progress/completed")
    priority: str | None = Field(None, description="优先级: low/medium/high")


class TaskResponse(BaseModel):
    """任务响应模型"""

    id: int
    title: str
    description: str | None
    status: str
    priority: str
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TaskListResponse(BaseModel):
    """任务列表响应"""

    tasks: list[TaskResponse]
    total: int