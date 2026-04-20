"""多线程下载器 - ch02"""

import time
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class DownloadResult:
    """下载结果"""

    url: str
    success: bool
    data: Any = None
    error: str | None = None
    duration: float = 0.0


class ThreadDownloader:
    """线程池下载器"""

    def __init__(self, max_workers: int = 10):
        self.max_workers = max_workers
        self._executor: ThreadPoolExecutor | None = None

    @property
    def executor(self) -> ThreadPoolExecutor:
        if self._executor is None:
            self._executor = ThreadPoolExecutor(max_workers=self.max_workers)
        return self._executor

    def submit_task(self, fn: Callable, *args, **kwargs) -> Future:
        """提交单个任务"""
        return self.executor.submit(fn, *args, **kwargs)

    def submit_tasks(
        self, fn: Callable, tasks: list[tuple]
    ) -> list[Future]:
        """提交多个任务"""
        return [self.executor.submit(fn, *task) for task in tasks]

    def map_tasks(self, fn: Callable, items: list) -> list:
        """使用map方式执行任务"""
        return list(self.executor.map(fn, items))

    def gather_results(self, futures: list[Future], timeout: float | None = None) -> list:
        """收集所有结果"""
        return [f.result(timeout=timeout) for f in futures]

    def shutdown(self, wait: bool = True):
        """关闭线程池"""
        if self._executor:
            self._executor.shutdown(wait=wait)
            self._executor = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.shutdown(wait=True)


def download_with_threads(
    download_fn: Callable[[str], Any],
    urls: list[str],
    max_workers: int = 10,
) -> list[dict]:
    """使用Thread创建线程下载"""
    results = []

    def worker(url: str):
        try:
            result = download_fn(url)
            results.append(result)
        except Exception as e:
            results.append({"url": url, "error": str(e)})

    from threading import Thread

    threads = [Thread(target=worker, args=(url,)) for url in urls]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    return results


def download_with_thread_pool(
    download_fn: Callable[[str], Any],
    urls: list[str],
    max_workers: int = 10,
) -> list:
    """使用ThreadPoolExecutor下载"""
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        return list(executor.map(download_fn, urls))


def download_with_as_completed(
    download_fn: Callable[[str], Any],
    urls: list[str],
    max_workers: int = 10,
) -> list[DownloadResult]:
    """使用as_completed收集结果"""
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {
            executor.submit(download_fn, url): url for url in urls
        }
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
                results.append(
                    DownloadResult(url=url, success=True, data=data)
                )
            except Exception as e:
                results.append(
                    DownloadResult(url=url, success=False, error=str(e))
                )
    return results


def download_with_submit(
    download_fn: Callable[[str], Any],
    urls: list[str],
    max_workers: int = 10,
) -> list[DownloadResult]:
    """使用submit提交任务"""
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(download_fn, url) for url in urls]
        for i, future in enumerate(futures):
            try:
                data = future.result()
                results.append(
                    DownloadResult(url=urls[i], success=True, data=data)
                )
            except Exception as e:
                results.append(
                    DownloadResult(url=urls[i], success=False, error=str(e))
                )
    return results