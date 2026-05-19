"""异步下载器 - ch05"""

import asyncio
import contextlib
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass
class AsyncDownloadResult:
    """异步下载结果"""

    url: str
    success: bool
    data: Any = None
    error: str | None = None


class AsyncDownloader:
    """异步下载器"""

    def __init__(self, max_concurrent: int = 10):
        self.max_concurrent = max_concurrent
        self._semaphore: asyncio.Semaphore | None = None

    async def download_single(
        self, download_fn: Callable[[str], Any], url: str
    ) -> Any:
        """下载单个URL"""
        return await download_fn(url)

    async def download_multiple(
        self, download_fn: Callable[[str], Any], urls: list[str]
    ) -> list[Any]:
        """并发下载多个URL"""
        semaphore = asyncio.Semaphore(self.max_concurrent)

        async def limited_download(url: str):
            async with semaphore:
                return await download_fn(url)

        return await asyncio.gather(*[limited_download(url) for url in urls])

    async def download_with_queue(
        self, download_fn: Callable[[str], Any], urls: list[str]
    ) -> list[AsyncDownloadResult]:
        """使用Queue下载"""
        queue: asyncio.Queue[str] = asyncio.Queue()
        for url in urls:
            await queue.put(url)

        results: list[AsyncDownloadResult] = []

        async def worker():
            while True:
                try:
                    url = queue.get_nowait()
                except asyncio.QueueEmpty:
                    break
                try:
                    data = await download_fn(url)
                    results.append(
                        AsyncDownloadResult(url=url, success=True, data=data)
                    )
                except Exception as e:
                    results.append(
                        AsyncDownloadResult(url=url, success=False, error=str(e))
                    )
                queue.task_done()

        workers = [asyncio.create_task(worker()) for _ in range(self.max_concurrent)]
        await queue.join()
        for w in workers:
            w.cancel()
        return results


async def async_download_with_gather(
    download_fn: Callable[[str], Any], urls: list[str]
) -> list[Any]:
    """使用asyncio.gather并发下载"""
    return await asyncio.gather(*[download_fn(url) for url in urls])


async def async_download_with_queue(
    download_fn: Callable[[str], Any], urls: list[str], max_concurrent: int = 5
) -> list[Any]:
    """使用asyncio.Queue限流下载"""
    queue: asyncio.Queue[str] = asyncio.Queue()
    results: list[Any] = []
    results_lock = asyncio.Lock()

    for url in urls:
        await queue.put(url)

    async def worker():
        while True:
            url = await queue.get()
            try:
                result = await download_fn(url)
                async with results_lock:
                    results.append(result)
            finally:
                queue.task_done()

    workers = [asyncio.create_task(worker()) for _ in range(max_concurrent)]
    await queue.join()
    for w in workers:
        w.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await w

    return results


class AsyncLockDemo:
    """asyncio.Lock演示"""

    def __init__(self):
        self._lock = asyncio.Lock()
        self._counter = 0

    async def demo_async_lock(self) -> dict:
        """演示asyncio.Lock"""
        self._counter = 0
        iterations = 100

        async def increment():
            for _ in range(iterations):
                async with self._lock:
                    self._counter += 1

        await asyncio.gather(*[increment() for _ in range(5)])

        return {
            "success": True,
            "final_value": self._counter,
            "expected": 500,
        }


class AsyncSemaphoreDemo:
    """asyncio.Semaphore演示"""

    def __init__(self, max_concurrent: int = 3):
        self._semaphore = asyncio.Semaphore(max_concurrent)
        self._max_concurrent = max_concurrent
        self._current_concurrent = 0
        self._max_observed = 0

    async def demo_async_semaphore(self) -> dict:
        """演示asyncio.Semaphore"""
        self._current_concurrent = 0
        self._max_observed = 0

        async def worker():
            async with self._semaphore:
                self._current_concurrent += 1
                self._max_observed = max(self._max_observed, self._current_concurrent)
                await asyncio.sleep(0.01)
                self._current_concurrent -= 1

        await asyncio.gather(*[worker() for _ in range(6)])

        return {
            "success": True,
            "max_concurrent": self._max_observed,
        }


class AsyncQueueDemo:
    """asyncio.Queue演示"""

    def __init__(self):
        self._queue: asyncio.Queue[int] = asyncio.Queue()

    async def demo_async_queue(self) -> dict:
        """演示asyncio.Queue生产者-消费者"""
        items_count = 10
        consumed = []

        async def producer():
            for i in range(items_count):
                await self._queue.put(i)
            await self._queue.put(None)

        async def consumer():
            while True:
                item = await self._queue.get()
                if item is None:
                    self._queue.task_done()
                    break
                consumed.append(item)
                self._queue.task_done()

        await asyncio.gather(producer(), consumer())

        return {
            "success": True,
            "items_produced": items_count,
            "items_consumed": len(consumed),
        }


async def async_for_demo(count: int = 5) -> dict:
    """演示async for"""

    async def async_generator(n: int):
        for i in range(n):
            await asyncio.sleep(0.01)
            yield i

    items = []
    async for item in async_generator(count):
        items.append(item)

    return {"success": True, "items": items}


async def async_timeout_demo(
    coro: Callable[[], Any], timeout: float
) -> dict:
    """演示asyncio.wait_for超时"""
    try:
        result = await asyncio.wait_for(coro(), timeout=timeout)
        return {"success": True, "result": result, "timed_out": False}
    except TimeoutError:
        return {"success": False, "result": None, "timed_out": True}


async def async_context_manager_demo() -> dict:
    """演示async with"""

    class AsyncResource:
        async def __aenter__(self):
            await asyncio.sleep(0.01)
            return "resource"

        async def __aexit__(self, *args):
            await asyncio.sleep(0.01)

    async with AsyncResource() as resource:
        return {"success": True, "resource": resource}
