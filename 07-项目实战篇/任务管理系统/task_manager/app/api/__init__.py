"""API 路由"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core import get_db
from ..models.schemas import (
    TaskCreate, TaskUpdate, TaskResponse,
    ProjectCreate, ProjectResponse
)
from ..services import TaskService, ProjectService

router = APIRouter()


# 任务路由
@router.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    return TaskService.create(db, task)


@router.get("/tasks", response_model=list[TaskResponse])
def get_tasks(
    status: str = None,
    project_id: int = None,
    db: Session = Depends(get_db)
):
    return TaskService.get_list(db, status, project_id)


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = TaskService.get(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    return task


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    updated = TaskService.update(db, task_id, task)
    if not updated:
        raise HTTPException(status_code=404, detail="任务不存在")
    return updated


@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    if not TaskService.delete(db, task_id):
        raise HTTPException(status_code=404, detail="任务不存在")
    return {"message": "删除成功"}


# 项目路由
@router.post("/projects", response_model=ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    return ProjectService.create(db, project)


@router.get("/projects", response_model=list[ProjectResponse])
def get_projects(db: Session = Depends(get_db)):
    return ProjectService.get_all(db)