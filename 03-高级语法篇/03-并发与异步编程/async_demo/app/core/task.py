"""任务定义"""

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class TaskStatus(Enum):
    """任务状态"""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(Enum):
    """任务优先级"""

    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class DownloadTask:
    """下载任务"""

    url: str
    priority: TaskPriority = TaskPriority.NORMAL
    max_retries: int = 3
    status: TaskStatus = TaskStatus.PENDING
    result: Any = None
    error: str | None = None
    retry_count: int = 0
    started_at: float | None = None
    completed_at: float | None = None

    def start(self) -> None:
        """开始任务"""
        self.status = TaskStatus.RUNNING
        self.started_at = time.time()

    def complete(self, result: Any) -> None:
        """完成任务"""
        self.status = TaskStatus.COMPLETED
        self.result = result
        self.completed_at = time.time()

    def fail(self, error: str) -> None:
        """任务失败"""
        self.status = TaskStatus.FAILED
        self.error = error
        self.completed_at = time.time()

    def cancel(self) -> None:
        """取消任务"""
        self.status = TaskStatus.CANCELLED
        self.completed_at = time.time()

    def increment_retry(self) -> int:
        """增加重试次数"""
        self.retry_count += 1
        return self.retry_count

    def can_retry(self) -> bool:
        """是否可以重试"""
        return self.retry_count < self.max_retries

    def duration(self) -> float:
        """任务持续时间"""
        if self.started_at is None:
            return 0.0
        if self.completed_at is None:
            return time.time() - self.started_at
        return self.completed_at - self.started_at

    def reset(self) -> None:
        """重置任务"""
        self.status = TaskStatus.PENDING
        self.result = None
        self.error = None
        self.retry_count = 0
        self.started_at = None
        self.completed_at = None


@dataclass
class DownloadResult:
    """下载结果"""

    url: str
    success: bool
    data: Any = None
    error: str | None = None
    duration: float = 0.0
    retry_count: int = 0

    @classmethod
    def from_task(cls, task: DownloadTask) -> "DownloadResult":
        """从任务创建结果"""
        return cls(
            url=task.url,
            success=task.status == TaskStatus.COMPLETED,
            data=task.result,
            error=task.error,
            duration=task.duration(),
            retry_count=task.retry_count,
        )


def create_download_task(
    url: str,
    priority: TaskPriority = TaskPriority.NORMAL,
    max_retries: int = 3,
) -> DownloadTask:
    """创建下载任务"""
    return DownloadTask(url=url, priority=priority, max_retries=max_retries)


def create_task_batch(urls: list[str], priority: TaskPriority = TaskPriority.NORMAL) -> list[DownloadTask]:
    """批量创建任务"""
    return [create_download_task(url, priority) for url in urls]