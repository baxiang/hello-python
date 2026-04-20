"""进度跟踪"""

import asyncio
from dataclasses import dataclass, field
from threading import Lock


@dataclass
class ProgressTracker:
    """进度跟踪器"""

    total: int
    completed: int = 0
    failed: int = 0
    _start_time: float = field(default_factory=lambda: 0.0)

    def __post_init__(self):
        import time
        self._start_time = time.time()

    def increment(self, count: int = 1) -> int:
        """增加完成数"""
        self.completed += count
        return self.completed

    def increment_failed(self, count: int = 1) -> int:
        """增加失败数"""
        self.failed += count
        return self.failed

    def percentage(self) -> float:
        """完成百分比"""
        if self.total == 0:
            return 100.0
        return round(self.completed / self.total * 100, 2)

    def remaining(self) -> int:
        """剩余数量"""
        return self.total - self.completed

    def is_complete(self) -> bool:
        """是否完成"""
        return self.completed >= self.total

    def elapsed_time(self) -> float:
        """已耗时"""
        import time
        return time.time() - self._start_time

    def report(self) -> dict:
        """生成报告"""
        return {
            "total": self.total,
            "completed": self.completed,
            "failed": self.failed,
            "remaining": self.remaining(),
            "percentage": self.percentage(),
            "elapsed_time": round(self.elapsed_time(), 2),
        }


class ThreadSafeProgress:
    """线程安全进度"""

    def __init__(self, total: int):
        self._total = total
        self._completed = 0
        self._failed = 0
        self._lock = Lock()
        self._start_time = 0.0
        import time
        self._start_time = time.time()

    @property
    def total(self) -> int:
        """总数"""
        return self._total

    def increment(self, count: int = 1) -> int:
        """增加完成数"""
        with self._lock:
            self._completed += count
            return self._completed

    def increment_failed(self, count: int = 1) -> int:
        """增加失败数"""
        with self._lock:
            self._failed += count
            return self._failed

    def get_completed(self) -> int:
        """获取完成数"""
        with self._lock:
            return self._completed

    def get_failed(self) -> int:
        """获取失败数"""
        with self._lock:
            return self._failed

    def set_completed(self, value: int) -> None:
        """设置完成数"""
        with self._lock:
            self._completed = value

    def percentage(self) -> float:
        """完成百分比"""
        with self._lock:
            if self._total == 0:
                return 100.0
            return round(self._completed / self._total * 100, 2)

    def remaining(self) -> int:
        """剩余数量"""
        with self._lock:
            return self._total - self._completed

    def is_complete(self) -> bool:
        """是否完成"""
        with self._lock:
            return self._completed >= self._total

    def elapsed_time(self) -> float:
        """已耗时"""
        import time
        return time.time() - self._start_time

    def report(self) -> dict:
        """生成报告"""
        with self._lock:
            return {
                "total": self._total,
                "completed": self._completed,
                "failed": self._failed,
                "remaining": self._total - self._completed,
                "percentage": self.percentage(),
                "elapsed_time": round(self.elapsed_time(), 2),
            }


class AsyncProgressTracker:
    """异步进度跟踪器"""

    def __init__(self, total: int):
        self._total = total
        self._completed = 0
        self._failed = 0
        self._lock = asyncio.Lock()
        import time
        self._start_time = time.time()

    @property
    def total(self) -> int:
        """总数"""
        return self._total

    async def increment(self, count: int = 1) -> int:
        """增加完成数"""
        async with self._lock:
            self._completed += count
            return self._completed

    async def increment_failed(self, count: int = 1) -> int:
        """增加失败数"""
        async with self._lock:
            self._failed += count
            return self._failed

    async def get_completed(self) -> int:
        """获取完成数"""
        async with self._lock:
            return self._completed

    async def get_failed(self) -> int:
        """获取失败数"""
        async with self._lock:
            return self._failed

    async def set_completed(self, value: int) -> None:
        """设置完成数"""
        async with self._lock:
            self._completed = value

    async def percentage(self) -> float:
        """完成百分比"""
        async with self._lock:
            if self._total == 0:
                return 100.0
            return round(self._completed / self._total * 100, 2)

    async def remaining(self) -> int:
        """剩余数量"""
        async with self._lock:
            return self._total - self._completed

    async def is_complete(self) -> bool:
        """是否完成"""
        async with self._lock:
            return self._completed >= self._total

    def elapsed_time(self) -> float:
        """已耗时"""
        import time
        return time.time() - self._start_time

    async def report(self) -> dict:
        """生成报告"""
        async with self._lock:
            return {
                "total": self._total,
                "completed": self._completed,
                "failed": self._failed,
                "remaining": self._total - self._completed,
                "percentage": await self.percentage(),
                "elapsed_time": round(self.elapsed_time(), 2),
            }


def create_progress_tracker(total: int, thread_safe: bool = True) -> ProgressTracker | ThreadSafeProgress:
    """创建进度跟踪器"""
    if thread_safe:
        return ThreadSafeProgress(total=total)
    return ProgressTracker(total=total)