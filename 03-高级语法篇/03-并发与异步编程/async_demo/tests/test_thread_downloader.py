"""多线程下载器测试"""

import time
from concurrent.futures import Future
from unittest.mock import MagicMock, patch

from app.core.thread_downloader import (
    ThreadDownloader,
    download_with_thread_pool,
    download_with_threads,
)


class TestThreadDownloader:
    def test_init(self):
        downloader = ThreadDownloader(max_workers=4)
        assert downloader.max_workers == 4

    def test_init_default(self):
        downloader = ThreadDownloader()
        assert downloader.max_workers == 10

    def test_submit_task(self):
        downloader = ThreadDownloader(max_workers=2)

        def mock_download(url: str) -> str:
            return f"content_{url}"

        future = downloader.submit_task(mock_download, "http://example.com")
        assert isinstance(future, Future)
        result = future.result(timeout=5)
        assert result == "content_http://example.com"

    def test_submit_multiple_tasks(self):
        downloader = ThreadDownloader(max_workers=4)

        def mock_download(url: str) -> str:
            time.sleep(0.01)
            return f"content_{url}"

        urls = [f"http://example{i}.com" for i in range(3)]
        futures = [downloader.submit_task(mock_download, url) for url in urls]

        results = [f.result(timeout=5) for f in futures]
        assert len(results) == 3
        assert all("content_" in r for r in results)

    def test_shutdown(self):
        downloader = ThreadDownloader(max_workers=2)
        downloader.shutdown(wait=True)


class TestDownloadWithThreads:
    def test_download_with_threads_basic(self):
        def mock_download(url: str) -> dict:
            return {"url": url, "status": 200, "content": f"data_{url}"}

        urls = ["http://a.com", "http://b.com"]
        results = download_with_threads(mock_download, urls, max_workers=2)
        assert len(results) == 2
        assert all(r["status"] == 200 for r in results)

    def test_download_with_threads_exception(self):
        def mock_download(url: str) -> dict:
            if "error" in url:
                raise ValueError("Download failed")
            return {"url": url, "status": 200}

        urls = ["http://ok.com", "http://error.com"]
        results = download_with_threads(mock_download, urls, max_workers=2)
        assert len(results) == 2
        success_count = sum(1 for r in results if r.get("status") == 200)
        error_count = sum(1 for r in results if "error" in r.get("url", ""))
        assert success_count == 1
        assert error_count == 1


class TestDownloadWithThreadPool:
    def test_download_with_thread_pool_map(self):
        def mock_download(url: str) -> dict:
            return {"url": url, "status": 200}

        urls = [f"http://test{i}.com" for i in range(5)]
        results = download_with_thread_pool(mock_download, urls, max_workers=3)
        assert len(results) == 5
        assert all(r["status"] == 200 for r in results)

    def test_concurrent_execution(self):
        def slow_download(url: str) -> float:
            time.sleep(0.1)
            return time.time()

        urls = [f"http://test{i}.com" for i in range(3)]
        start = time.time()
        results = download_with_thread_pool(slow_download, urls, max_workers=3)
        elapsed = time.time() - start

        assert elapsed < 0.5, "Tasks should run concurrently"
        assert len(results) == 3