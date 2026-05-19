"""策略选择 - ch06"""

import asyncio
import time
from collections.abc import Callable
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from enum import Enum
from typing import Any


class ConcurrencyStrategy(Enum):
    """并发策略枚举"""

    THREADING = "threading"
    MULTIPROCESSING = "multiprocessing"
    ASYNCIO = "asyncio"
    HYBRID = "hybrid"


class StrategySelector:
    """策略选择器"""

    ASYNC_THRESHOLD = 50

    def __init__(self):
        self._benchmarks: dict[str, float] = {}

    def choose_for_task(self, task_name: str) -> ConcurrencyStrategy:
        """根据任务名选择策略"""
        task_lower = task_name.lower()

        cpu_keywords = ["compute", "calculate", "process", "encode", "decode"]
        io_keywords = ["download", "upload", "request", "read", "write"]

        for keyword in cpu_keywords:
            if keyword in task_lower:
                return ConcurrencyStrategy.MULTIPROCESSING

        for keyword in io_keywords:
            if keyword in task_lower:
                return ConcurrencyStrategy.ASYNCIO

        return ConcurrencyStrategy.THREADING

    def choose_for_high_concurrency_io(
        self, concurrent_count: int
    ) -> ConcurrencyStrategy:
        """高并发IO选择asyncio"""
        if concurrent_count >= self.ASYNC_THRESHOLD:
            return ConcurrencyStrategy.ASYNCIO
        return ConcurrencyStrategy.THREADING

    def choose_for_few_io_tasks(self, task_count: int) -> ConcurrencyStrategy:
        """少量IO任务选择threading"""
        if task_count < self.ASYNC_THRESHOLD:
            return ConcurrencyStrategy.THREADING
        return ConcurrencyStrategy.ASYNCIO

    def choose_based_on_duration(
        self, expected_duration: float
    ) -> ConcurrencyStrategy:
        """根据预期时长选择"""
        if expected_duration > 1.0:
            return ConcurrencyStrategy.ASYNCIO
        return ConcurrencyStrategy.THREADING


def choose_strategy(
    task_type: str,
    concurrent_count: int = 10,
    expected_duration: float = 0.5,
) -> ConcurrencyStrategy:
    """综合选择策略"""
    if task_type == "cpu_intensive":
        return ConcurrencyStrategy.MULTIPROCESSING

    if task_type == "io_intensive":
        if concurrent_count >= StrategySelector.ASYNC_THRESHOLD:
            return ConcurrencyStrategy.ASYNCIO
        if expected_duration > 1.0:
            return ConcurrencyStrategy.ASYNCIO
        return ConcurrencyStrategy.THREADING

    return ConcurrencyStrategy.HYBRID


class Benchmark:
    """性能基准测试"""

    def __init__(self):
        self.results: dict[str, dict] = {}

    def run_benchmark(
        self,
        download_fn: Callable[[str], Any],
        urls: list[str],
        strategy: ConcurrencyStrategy,
        max_workers: int = 5,
    ) -> dict:
        """运行基准测试"""
        start = time.time()
        success_count = 0

        if strategy == ConcurrencyStrategy.THREADING:
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                results = list(executor.map(download_fn, urls))
                success_count = len(results)

        elif strategy == ConcurrencyStrategy.MULTIPROCESSING:
            with ProcessPoolExecutor(max_workers=max_workers) as executor:
                results = list(executor.map(download_fn, urls))
                success_count = len(results)

        else:
            results = asyncio.run(
                _async_benchmark(download_fn, urls, max_workers)
            )
            success_count = len(results)

        duration = time.time() - start
        self.results[strategy.value] = {
            "duration": duration,
            "success_count": success_count,
        }

        return {
            "strategy": strategy.value,
            "duration": round(duration, 4),
            "success_count": success_count,
            "avg_time": round(duration / len(urls), 4) if urls else 0,
        }


async def _async_benchmark(
    download_fn: Callable[[str], Any], urls: list[str], max_concurrent: int
) -> list:
    """异步基准测试辅助函数"""
    semaphore = asyncio.Semaphore(max_concurrent)

    async def limited_download(url: str):
        async with semaphore:
            if asyncio.iscoroutinefunction(download_fn):
                return await download_fn(url)
            else:
                return download_fn(url)

    return await asyncio.gather(*[limited_download(url) for url in urls])


def benchmark_download(
    download_fn: Callable[[str], Any], urls: list[str], max_workers: int = 5
) -> dict:
    """对比三种策略的性能"""
    results = {}

    start = time.time()
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        list(executor.map(download_fn, urls))
    results["threading_time"] = round(time.time() - start, 4)

    start = time.time()
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        list(executor.map(download_fn, urls))
    results["multiprocessing_time"] = round(time.time() - start, 4)

    start = time.time()
    asyncio.run(_async_benchmark(download_fn, urls, max_workers))
    results["asyncio_time"] = round(time.time() - start, 4)

    best = min(
        results["threading_time"],
        results["multiprocessing_time"],
        results["asyncio_time"],
    )
    if best == results["threading_time"]:
        results["best_strategy"] = "threading"
    elif best == results["multiprocessing_time"]:
        results["best_strategy"] = "multiprocessing"
    else:
        results["best_strategy"] = "asyncio"

    return results


async def compare_strategies(
    async_download_fn: Callable[[str], Any],
    sync_download_fn: Callable[[str], Any],
    urls: list[str],
    max_concurrent: int = 5,
) -> dict:
    """异步对比策略"""
    results = {}

    start = time.time()
    await asyncio.gather(*[async_download_fn(url) for url in urls])
    results["asyncio_time"] = round(time.time() - start, 4)

    start = time.time()
    with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
        list(executor.map(sync_download_fn, urls))
    results["threading_time"] = round(time.time() - start, 4)

    best = min(results["asyncio_time"], results["threading_time"])
    results["best_strategy"] = (
        "asyncio" if best == results["asyncio_time"] else "threading"
    )

    return {
        "best_strategy": results["best_strategy"],
        "results": results,
    }


def get_strategy_recommendation(task_type: str, scale: str = "medium") -> dict:
    """获取策略推荐"""
    recommendations = {
        "cpu_intensive": {
            "small": ConcurrencyStrategy.THREADING,
            "medium": ConcurrencyStrategy.MULTIPROCESSING,
            "large": ConcurrencyStrategy.MULTIPROCESSING,
        },
        "io_intensive": {
            "small": ConcurrencyStrategy.THREADING,
            "medium": ConcurrencyStrategy.THREADING,
            "large": ConcurrencyStrategy.ASYNCIO,
        },
        "mixed": {
            "small": ConcurrencyStrategy.THREADING,
            "medium": ConcurrencyStrategy.HYBRID,
            "large": ConcurrencyStrategy.HYBRID,
        },
    }

    strategy = recommendations.get(task_type, {}).get(
        scale, ConcurrencyStrategy.THREADING
    )

    return {
        "task_type": task_type,
        "scale": scale,
        "recommended_strategy": strategy.value,
        "reason": _get_reason(task_type, scale, strategy),
    }


def _get_reason(
    task_type: str, scale: str, strategy: ConcurrencyStrategy
) -> str:
    """获取推荐理由"""
    reasons = {
        (ConcurrencyStrategy.MULTIPROCESSING, "cpu_intensive"): (
            "CPU密集型任务需要真正的并行执行，绕过GIL限制"
        ),
        (ConcurrencyStrategy.ASYNCIO, "io_intensive"): (
            "高并发IO任务适合单线程异步模型，减少线程开销"
        ),
        (ConcurrencyStrategy.THREADING, "io_intensive"): (
            "少量IO任务使用线程池简单高效"
        ),
        (ConcurrencyStrategy.HYBRID, "mixed"): (
            "混合型任务建议结合多种策略"
        ),
    }
    return reasons.get((strategy, task_type), "根据任务特性选择")
