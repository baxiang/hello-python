"""策略选择测试"""

import asyncio
import time

import pytest

from app.core.strategy import (
    Benchmark,
    ConcurrencyStrategy,
    StrategySelector,
    benchmark_download,
    choose_strategy,
    compare_strategies,
)


def _mock_download_for_benchmark(url: str) -> str:
    """模块级mock函数"""
    time.sleep(0.01)
    return url


async def _mock_async_download(url: str) -> str:
    """模块级异步mock函数"""
    await asyncio.sleep(0.01)
    return url


class TestConcurrencyStrategy:
    def test_strategy_enum(self):
        assert ConcurrencyStrategy.THREADING.value == "threading"
        assert ConcurrencyStrategy.MULTIPROCESSING.value == "multiprocessing"
        assert ConcurrencyStrategy.ASYNCIO.value == "asyncio"


class TestStrategySelector:
    def test_init(self):
        selector = StrategySelector()
        assert selector is not None

    def test_choose_for_io_intensive(self):
        selector = StrategySelector()
        result = selector.choose_for_task("download_file")
        assert result in [ConcurrencyStrategy.THREADING, ConcurrencyStrategy.ASYNCIO]

    def test_choose_for_cpu_intensive(self):
        selector = StrategySelector()
        result = selector.choose_for_task("compute_primes")
        assert result == ConcurrencyStrategy.MULTIPROCESSING

    def test_choose_for_high_concurrency_io(self):
        selector = StrategySelector()
        result = selector.choose_for_high_concurrency_io(concurrent_count=1000)
        assert result == ConcurrencyStrategy.ASYNCIO

    def test_choose_for_few_io_tasks(self):
        selector = StrategySelector()
        result = selector.choose_for_few_io_tasks(task_count=5)
        assert result == ConcurrencyStrategy.THREADING


class TestChooseStrategy:
    def test_choose_strategy_io(self):
        result = choose_strategy(
            task_type="io_intensive", concurrent_count=100, expected_duration=1.0
        )
        assert result in [ConcurrencyStrategy.THREADING, ConcurrencyStrategy.ASYNCIO]

    def test_choose_strategy_cpu(self):
        result = choose_strategy(task_type="cpu_intensive", concurrent_count=10)
        assert result == ConcurrencyStrategy.MULTIPROCESSING

    def test_choose_strategy_high_concurrency(self):
        result = choose_strategy(task_type="io_intensive", concurrent_count=1000)
        assert result == ConcurrencyStrategy.ASYNCIO


class TestBenchmark:
    def test_init(self):
        benchmark = Benchmark()
        assert benchmark is not None

    def test_run_benchmark(self):
        benchmark = Benchmark()

        def mock_download(url: str) -> dict:
            time.sleep(0.01)
            return {"url": url}

        urls = ["http://a.com", "http://b.com"]
        result = benchmark.run_benchmark(
            mock_download, urls, strategy=ConcurrencyStrategy.THREADING
        )
        assert "duration" in result
        assert "success_count" in result
        assert result["success_count"] == 2


class TestBenchmarkDownload:
    def test_benchmark_download(self):
        urls = [f"http://test{i}.com" for i in range(3)]
        result = benchmark_download(_mock_download_for_benchmark, urls)
        assert "threading_time" in result
        assert "multiprocessing_time" in result
        assert "asyncio_time" in result


class TestCompareStrategies:
    @pytest.mark.asyncio
    async def test_compare_strategies(self):
        urls = [f"http://test{i}.com" for i in range(3)]
        result = await compare_strategies(
            _mock_async_download, _mock_download_for_benchmark, urls
        )
        assert "best_strategy" in result
        assert "results" in result
