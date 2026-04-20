"""辅助函数"""

import asyncio
import time
from collections.abc import Callable
from typing import Any


async def run_with_timeout(coro: Any, timeout: float) -> Any:
    """带超时运行协程"""
    return await asyncio.wait_for(coro, timeout=timeout)


def measure_time(func: Callable) -> Callable:
    """测量函数执行时间的装饰器"""
    def wrapper(*args, **kwargs) -> Any:
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        if hasattr(wrapper, "_elapsed_times"):
            wrapper._elapsed_times.append(elapsed)
        else:
            wrapper._elapsed_times = [elapsed]
        return result
    return wrapper


async def measure_async_time(func: Callable) -> Callable:
    """测量异步函数执行时间的装饰器"""
    async def wrapper(*args, **kwargs) -> Any:
        start = time.time()
        result = await func(*args, **kwargs)
        elapsed = time.time() - start
        if hasattr(wrapper, "_elapsed_times"):
            wrapper._elapsed_times.append(elapsed)
        else:
            wrapper._elapsed_times = [elapsed]
        return result
    return wrapper


def format_duration(seconds: float) -> str:
    """格式化持续时间"""
    if seconds < 1:
        return f"{seconds * 1000:.2f}ms"
    if seconds < 60:
        return f"{seconds:.2f}s"
    minutes = seconds // 60
    secs = seconds % 60
    return f"{int(minutes)}m {secs:.2f}s"


def generate_urls(base_url: str, count: int) -> list[str]:
    """生成URL列表"""
    return [f"{base_url}/{i}" for i in range(count)]


def chunk_list(items: list[Any], chunk_size: int) -> list[list[Any]]:
    """分块列表"""
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]


def flatten_list(nested_list: list[list[Any]]) -> list[Any]:
    """扁平化列表"""
    return [item for sublist in nested_list for item in sublist]


def count_success_failures(results: list[dict]) -> dict:
    """统计成功和失败"""
    success = sum(1 for r in results if r.get("success", False))
    failures = sum(1 for r in results if not r.get("success", False))
    return {"success": success, "failures": failures, "total": len(results)}


def calculate_average_duration(results: list[dict]) -> float:
    """计算平均耗时"""
    durations = [r.get("duration", 0) for r in results]
    if not durations:
        return 0.0
    return sum(durations) / len(durations)


def print_summary(results: list[dict]) -> None:
    """打印摘要"""
    counts = count_success_failures(results)
    avg_duration = calculate_average_duration(results)
    print(f"Total: {counts['total']}")
    print(f"Success: {counts['success']}")
    print(f"Failures: {counts['failures']}")
    print(f"Average duration: {format_duration(avg_duration)}")


class Timer:
    """计时器"""

    def __init__(self):
        self._start_time: float | None = None
        self._end_time: float | None = None

    def start(self) -> None:
        self._start_time = time.time()

    def stop(self) -> float:
        self._end_time = time.time()
        return self.elapsed

    @property
    def elapsed(self) -> float:
        if self._start_time is None:
            return 0.0
        if self._end_time is None:
            return time.time() - self._start_time
        return self._end_time - self._start_time

    def __enter__(self) -> "Timer":
        self.start()
        return self

    def __exit__(self, *args) -> None:
        self.stop()


class AsyncTimer:
    """异步计时器"""

    def __init__(self):
        self._start_time: float | None = None
        self._end_time: float | None = None

    async def start(self) -> None:
        self._start_time = time.time()

    async def stop(self) -> float:
        self._end_time = time.time()
        return self.elapsed

    @property
    def elapsed(self) -> float:
        if self._start_time is None:
            return 0.0
        if self._end_time is None:
            return time.time() - self._start_time
        return self._end_time - self._start_time

    async def __aenter__(self) -> "AsyncTimer":
        await self.start()
        return self

    async def __aexit__(self, *args) -> None:
        await self.stop()
