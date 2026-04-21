"""任务服务"""

from typing import Any
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    """任务服务类"""

    async def create(
        self,
        db: AsyncSession,
        task_data: TaskCreate,
        owner_id: int,
    ) -> Task:
        """创建任务"""
        task = Task(
            title=task_data.title,
            description=task_data.description,
            status=task_data.status,
            priority=task_data.priority,
            owner_id=owner_id,
        )
        db.add(task)
        await db.commit()
        await db.refresh(task)
        return task

    async def get_by_id(self, db: AsyncSession, task_id: int) -> Task | None:
        """根据ID获取任务"""
        result = await db.execute(select(Task).where(Task.id == task_id))
        return result.scalar_one_or_none()

    async def get_list(
        self,
        db: AsyncSession,
        owner_id: int,
        status: str | None = None,
        priority: str | None = None,
    ) -> list[Task]:
        """获取任务列表"""
        query = select(Task).where(Task.owner_id == owner_id)
        if status:
            query = query.where(Task.status == status)
        if priority:
            query = query.where(Task.priority == priority)
        query = query.order_by(Task.created_at.desc())
        result = await db.execute(query)
        return list(result.scalars().all())

    async def update(
        self,
        db: AsyncSession,
        task_id: int,
        task_data: TaskUpdate,
    ) -> Task | None:
        """更新任务"""
        task = await self.get_by_id(db, task_id)
        if not task:
            return None

        update_data: dict[str, Any] = {}
        if task_data.title is not None:
            update_data["title"] = task_data.title
        if task_data.description is not None:
            update_data["description"] = task_data.description
        if task_data.status is not None:
            update_data["status"] = task_data.status
        if task_data.priority is not None:
            update_data["priority"] = task_data.priority

        if update_data:
            await db.execute(
                update(Task).where(Task.id == task_id).values(**update_data)
            )
            await db.commit()
            await db.refresh(task)

        return task

    async def delete(self, db: AsyncSession, task_id: int) -> bool:
        """删除任务"""
        result = await db.execute(delete(Task).where(Task.id == task_id))
        await db.commit()
        return result.rowcount > 0


task_service = TaskService()