"""异步下载器测试"""

import asyncio
import time

import pytest

from app.core.async_downloader import (
    AsyncDownloader,
    AsyncLockDemo,
    AsyncQueueDemo,
    AsyncSemaphoreDemo,
    async_download_with_gather,
    async_download_with_queue,
    async_for_demo,
    async_timeout_demo,
)


class TestAsyncDownloader:
    def test_init(self):
        downloader = AsyncDownloader(max_concurrent=5)
        assert downloader.max_concurrent == 5

    def test_init_default(self):
        downloader = AsyncDownloader()
        assert downloader.max_concurrent == 10

    @pytest.mark.asyncio
    async def test_download_single(self):
        downloader = AsyncDownloader()

        async def mock_download(url: str) -> dict:
            await asyncio.sleep(0.01)
            return {"url": url, "status": 200}

        result = await downloader.download_single(mock_download, "http://example.com")
        assert result["status"] == 200

    @pytest.mark.asyncio
    async def test_download_multiple(self):
        downloader = AsyncDownloader(max_concurrent=3)

        async def mock_download(url: str) -> dict:
            await asyncio.sleep(0.01)
            return {"url": url, "status": 200}

        urls = [f"http://test{i}.com" for i in range(5)]
        results = await downloader.download_multiple(mock_download, urls)
        assert len(results) == 5
        assert all(r["status"] == 200 for r in results)


class TestAsyncDownloadWithGather:
    @pytest.mark.asyncio
    async def test_async_download_with_gather_basic(self):
        async def mock_download(url: str) -> dict:
            await asyncio.sleep(0.01)
            return {"url": url, "status": 200}

        urls = ["http://a.com", "http://b.com", "http://c.com"]
        results = await async_download_with_gather(mock_download, urls)
        assert len(results) == 3
        assert all(r["status"] == 200 for r in results)

    @pytest.mark.asyncio
    async def test_concurrent_execution(self):
        async def slow_download(url: str) -> float:
            await asyncio.sleep(0.1)
            return time.time()

        urls = [f"http://test{i}.com" for i in range(4)]
        start = time.time()
        results = await async_download_with_gather(slow_download, urls)
        elapsed = time.time() - start

        assert elapsed < 0.5, "Tasks should run concurrently"
        assert len(results) == 4


class TestAsyncDownloadWithQueue:
    @pytest.mark.asyncio
    async def test_async_download_with_queue_basic(self):
        async def mock_download(url: str) -> dict:
            await asyncio.sleep(0.01)
            return {"url": url, "status": 200}

        urls = [f"http://test{i}.com" for i in range(5)]
        results = await async_download_with_queue(mock_download, urls, max_concurrent=2)
        assert len(results) == 5
        assert all(r["status"] == 200 for r in results)


class TestAsyncLockDemo:
    @pytest.mark.asyncio
    async def test_async_lock_demo(self):
        demo = AsyncLockDemo()
        result = await demo.demo_async_lock()
        assert result["success"] is True
        assert result["final_value"] == result["expected"]


class TestAsyncSemaphoreDemo:
    @pytest.mark.asyncio
    async def test_async_semaphore_demo(self):
        demo = AsyncSemaphoreDemo(max_concurrent=2)
        result = await demo.demo_async_semaphore()
        assert result["success"] is True
        assert result["max_concurrent"] <= 2


class TestAsyncQueueDemo:
    @pytest.mark.asyncio
    async def test_async_queue_demo(self):
        demo = AsyncQueueDemo()
        result = await demo.demo_async_queue()
        assert result["success"] is True
        assert result["items_produced"] == result["items_consumed"]


class TestAsyncForDemo:
    @pytest.mark.asyncio
    async def test_async_for_demo(self):
        result = await async_for_demo(count=5)
        assert result["success"] is True
        assert len(result["items"]) == 5


class TestAsyncTimeoutDemo:
    @pytest.mark.asyncio
    async def test_async_timeout_success(self):
        async def quick_task() -> str:
            await asyncio.sleep(0.01)
            return "done"

        result = await async_timeout_demo(quick_task, timeout=1.0)
        assert result["success"] is True
        assert result["result"] == "done"

    @pytest.mark.asyncio
    async def test_async_timeout_expired(self):
        async def slow_task() -> str:
            await asyncio.sleep(2.0)
            return "done"

        result = await async_timeout_demo(slow_task, timeout=0.1)
        assert result["success"] is False
        assert result["timed_out"] is True