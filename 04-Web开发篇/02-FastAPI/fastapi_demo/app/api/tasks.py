"""任务API"""

import logging
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskListResponse, TaskResponse, TaskUpdate
from app.services.task import task_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/tasks", tags=["任务"])


def log_task_event(event: str, task_id: int, user_id: int) -> None:
    """后台任务：记录任务事件"""
    logger.info(f"Task event: {event}, task_id={task_id}, user_id={user_id}")


def send_completion_notification(task_id: int, task_title: str, user_id: int) -> None:
    """后台任务：发送完成通知"""
    logger.info(f"Task completed: {task_title} (id={task_id}) by user {user_id}")


@router.get("", response_model=TaskListResponse)
async def list_tasks(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    status_filter: Annotated[str | None, Query(alias="status")] = None,
    priority: str | None = None,
) -> TaskListResponse:
    """获取任务列表"""
    tasks = await task_service.get_list(
        db,
        owner_id=current_user.id,
        status=status_filter,
        priority=priority,
    )
    return TaskListResponse(tasks=tasks, total=len(tasks))


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Task:
    """创建任务"""
    task = await task_service.create(db, task_data, current_user.id)
    background_tasks.add_task(log_task_event, "created", task.id, current_user.id)
    return task


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Task:
    """获取单个任务"""
    task = await task_service.get_by_id(db, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="任务不存在",
        )
    if task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问此任务",
        )
    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Task:
    """更新任务"""
    task = await task_service.get_by_id(db, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="任务不存在",
        )
    if task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权修改此任务",
        )

    old_status = task.status
    updated_task = await task_service.update(db, task_id, task_data)
    background_tasks.add_task(log_task_event, "updated", task_id, current_user.id)

    if task_data.status == "completed" and old_status != "completed":
        background_tasks.add_task(
            send_completion_notification, task_id, task.title, current_user.id
        )

    return updated_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """删除任务"""
    task = await task_service.get_by_id(db, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="任务不存在",
        )
    if task.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权删除此任务",
        )

    success = await task_service.delete(db, task_id)
    if success:
        background_tasks.add_task(log_task_event, "deleted", task_id, current_user.id)