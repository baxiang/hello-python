"""任务服务"""

from sqlalchemy.orm import Session
from typing import Optional
from .models import Task, Project
from .models.schemas import TaskCreate, TaskUpdate


class TaskService:
    """任务服务"""
    
    @staticmethod
    def create(db: Session, task: TaskCreate) -> Task:
        db_task = Task(**task.model_dump())
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    
    @staticmethod
    def get(db: Session, task_id: int) -> Task | None:
        return db.query(Task).filter(Task.id == task_id).first()
    
    @staticmethod
    def get_list(
        db: Session,
        status: Optional[str] = None,
        project_id: Optional[int] = None
    ) -> list[Task]:
        query = db.query(Task)
        if status:
            query = query.filter(Task.status == status)
        if project_id:
            query = query.filter(Task.project_id == project_id)
        return query.order_by(Task.created_at.desc()).all()
    
    @staticmethod
    def update(db: Session, task_id: int, task: TaskUpdate) -> Task | None:
        db_task = TaskService.get(db, task_id)
        if not db_task:
            return None
        
        for key, value in task.model_dump(exclude_unset=True).items():
            setattr(db_task, key, value)
        
        db.commit()
        db.refresh(db_task)
        return db_task
    
    @staticmethod
    def delete(db: Session, task_id: int) -> bool:
        db_task = TaskService.get(db, task_id)
        if not db_task:
            return False
        db.delete(db_task)
        db.commit()
        return True


class ProjectService:
    """项目服务"""
    
    @staticmethod
    def create(db: Session, project: ProjectCreate) -> Project:
        db_project = Project(**project.model_dump())
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        return db_project
    
    @staticmethod
    def get_all(db: Session) -> list[Project]:
        return db.query(Project).all()