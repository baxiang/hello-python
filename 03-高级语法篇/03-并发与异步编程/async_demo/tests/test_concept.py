"""并发概念演示测试"""

from app.core.concept import (
    ConceptDemo,
    classify_task,
    demo_gil_impact,
    explain_concurrency_vs_parallelism,
)


class TestConceptDemo:
    def test_init(self):
        demo = ConceptDemo()
        assert demo.name == "ConceptDemo"

    def test_show_threading_basics(self):
        demo = ConceptDemo()
        result = demo.show_threading_basics()
        assert "threads_created" in result
        assert result["threads_created"] > 0

    def test_show_multiprocessing_basics(self):
        demo = ConceptDemo()
        result = demo.show_multiprocessing_basics()
        assert "processes_created" in result
        assert result["processes_created"] > 0

    def test_show_async_basics(self):
        demo = ConceptDemo()
        result = demo.show_async_basics()
        assert "coroutines_created" in result
        assert result["coroutines_created"] > 0


class TestClassifyTask:
    def test_classify_cpu_intensive(self):
        result = classify_task("compute_primes")
        assert result["type"] == "cpu_intensive"
        assert result["recommended"] in ["multiprocessing", "process_pool"]

    def test_classify_io_intensive(self):
        result = classify_task("download_file")
        assert result["type"] == "io_intensive"
        assert result["recommended"] in ["threading", "asyncio"]

    def test_classify_mixed(self):
        result = classify_task("process_data")
        assert result["type"] == "mixed"
        assert "hybrid" in result["recommended"] or result["recommended"] == "depends"


class TestGILDemo:
    def test_demo_gil_impact(self):
        result = demo_gil_impact(iterations=1000)
        assert "thread_time" in result
        assert "process_time" in result
        assert result["thread_time"] >= 0
        assert result["process_time"] >= 0


class TestConcurrencyVsParallelism:
    def test_explain_concurrency_vs_parallelism(self):
        explanation = explain_concurrency_vs_parallelism()
        assert "concurrency" in str(explanation).lower()
        assert "parallelism" in str(explanation).lower()
        assert "definition" in explanation
        assert "example" in explanation
