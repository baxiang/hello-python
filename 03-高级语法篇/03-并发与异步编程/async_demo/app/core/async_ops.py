"""异步编程示例"""

import asyncio
from typing import Any
import time


async def async_task(name: str, delay: float) -> dict[str, Any]:
    """异步任务"""
    start = time.time()
    await asyncio.sleep(delay)
    end = time.time()
    return {
        "name": name,
        "delay": delay,
        "actual_time": end - start
    }


async def run_concurrent_tasks(tasks: list[tuple[str, float]]) -> list[dict[str, Any]]:
    """并发运行多个任务"""
    coroutines = [async_task(name, delay) for name, delay in tasks]
    return await asyncio.gather(*coroutines)


async def async_generator(count: int):
    """异步生成器"""
    for i in range(count):
        await asyncio.sleep(0.01)
        yield i


class AsyncCounter:
    """异步计数器"""
    
    def __init__(self, start: int = 0):
        self._value = start
        self._lock = asyncio.Lock()
    
    async def increment(self) -> int:
        async with self._lock:
            self._value += 1
            return self._value
    
    async def get_value(self) -> int:
        async with self._lock:
            return self._value