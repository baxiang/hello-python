"""多进程下载器测试"""

import time
from multiprocessing import Manager

from app.core.process_downloader import (
    ProcessDownloader,
    download_with_process_pool,
    download_with_processes,
    shared_queue_demo,
    shared_value_demo,
)


def _mock_process_download(url: str) -> dict:
    """模块级函数用于进程pickle"""
    return {"url": url, "status": 200, "content": f"data_{url}"}


def _cpu_intensive_task(n: int) -> int:
    """CPU密集型任务 - 模块级函数"""
    result = 0
    for i in range(n):
        result += i
    return result


class TestProcessDownloader:
    def test_init(self):
        downloader = ProcessDownloader(max_workers=4)
        assert downloader.max_workers == 4

    def test_init_default(self):
        downloader = ProcessDownloader()
        assert downloader.max_workers is None or downloader.max_workers > 0

    def test_submit_task(self):
        downloader = ProcessDownloader(max_workers=2)
        future = downloader.submit_task(_cpu_intensive_task, 1000)
        result = future.result(timeout=10)
        assert result == sum(range(1000))

    def test_map_tasks(self):
        downloader = ProcessDownloader(max_workers=2)
        results = downloader.map_tasks(_cpu_intensive_task, [100, 200, 300])
        assert len(results) == 3
        assert results[0] == sum(range(100))

    def test_shutdown(self):
        downloader = ProcessDownloader(max_workers=2)
        downloader.shutdown(wait=True)


def _slow_task(url: str) -> float:
    """慢任务 - 模块级函数"""
    time.sleep(0.1)
    return time.time()


class TestDownloadWithProcesses:
    def test_download_with_processes_basic(self):
        urls = ["http://a.com", "http://b.com"]
        results = download_with_processes(_mock_process_download, urls, max_workers=2)
        assert len(results) == 2
        assert all(r["status"] == 200 for r in results)

    def test_download_with_processes_parallel(self):
        urls = [f"http://test{i}.com" for i in range(3)]
        start = time.time()
        results = download_with_processes(_slow_task, urls, max_workers=3)
        elapsed = time.time() - start

        assert elapsed < 0.5, "Tasks should run in parallel"
        assert len(results) == 3


class TestDownloadWithProcessPool:
    def test_download_with_process_pool_map(self):
        urls = [f"http://test{i}.com" for i in range(4)]
        results = download_with_process_pool(_mock_process_download, urls, max_workers=2)
        assert len(results) == 4
        assert all(r["status"] == 200 for r in results)

    def test_process_pool_vs_thread_pool(self):
        iterations = 10000

        start = time.time()
        from concurrent.futures import ThreadPoolExecutor

        with ThreadPoolExecutor(max_workers=4) as executor:
            list(executor.map(_cpu_intensive_task, [iterations] * 4))
        thread_time = time.time() - start

        start = time.time()
        results = download_with_process_pool(
            _cpu_intensive_task, [iterations] * 4, max_workers=4
        )
        process_time = time.time() - start

        assert len(results) == 4


class TestSharedQueue:
    def test_shared_queue_demo(self):
        result = shared_queue_demo()
        assert result["success"] is True
        assert result["items_sent"] == result["items_received"]

    def test_shared_queue_basic(self):
        result = shared_queue_demo(items=5)
        assert result["items_received"] == 5


class TestSharedValue:
    def test_shared_value_demo(self):
        result = shared_value_demo()
        assert result["success"] is True
        assert result["final_value"] == result["expected"]

    def test_shared_value_increment(self):
        result = shared_value_demo(increment_by=10)
        assert result["final_value"] == 10