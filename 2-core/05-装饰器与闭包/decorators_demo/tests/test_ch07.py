"""第 7 章测试 — 装饰器边界情况与调试实战"""

import asyncio
import time

from app.decorators.ch07_edge_cases import (
    async_timer_fixed,
    bad_decorator,
    create_api_handlers_fixed,
    create_api_handlers_wrong,
    create_callbacks_fixed,
    create_callbacks_wrong,
    good_decorator,
    sync_timer_wrong,
    timer_a,
    timer_b,
    timer_inner,
    timer_outer,
)
from app.decorators.ch07_debug_tools import (
    count_wrapper_depth,
    diagnose_async_decorator,
    diagnose_signature,
    get_original,
    inspect_closure_trap,
)
from app.decorators.ch07_production import PerformanceTracker


class TestDecoratorOrder:
    """测试装饰器叠加顺序"""

    def test_timer_conflict_wrong_order(self):
        @timer_a
        @timer_b
        def process():
            return "done"

        result = process()
        assert result == "done"
        assert process._source == "timer_a"
        inner = getattr(process, "__wrapped__", None)
        assert inner is not None
        assert hasattr(inner, "_last_elapsed")

    def test_timer_fixed_order_different_attrs(self):
        @timer_outer
        @timer_inner
        def process():
            return "done"

        result = process()
        assert result == "done"
        assert hasattr(process, "_outer_elapsed")
        assert hasattr(process, "_inner_elapsed")


class TestClosureTrap:
    """测试闭包变量绑定陷阱"""

    def test_callbacks_wrong_late_binding(self):
        callbacks = create_callbacks_wrong()
        results = [cb() for cb in callbacks]
        assert results == [4, 4, 4]

    def test_callbacks_fixed_early_binding(self):
        callbacks = create_callbacks_fixed()
        results = [cb() for cb in callbacks]
        assert results == [0, 2, 4]

    def test_api_handlers_wrong_shared_endpoint(self):
        handlers = create_api_handlers_wrong()
        results = {k: v() for k, v in handlers.items()}
        assert all(r == "处理 orders" for r in results.values())

    def test_api_handlers_fixed(self):
        handlers = create_api_handlers_fixed()
        results = {k: v() for k, v in handlers.items()}
        assert results["users"] == "处理 users"
        assert results["products"] == "处理 products"
        assert results["orders"] == "处理 orders"

    def test_inspect_closure_trap_detects_shared(self):
        handlers = create_api_handlers_wrong()
        for handler in handlers.values():
            info = inspect_closure_trap(handler)
            assert info["trap_detected"] is True
            assert info["trap_value"] == "orders"


class TestAsyncDecoratorCompatibility:
    """测试 async 装饰器兼容性"""

    def test_sync_timer_wrong_missing_await(self):
        @sync_timer_wrong
        async def fetch():
            await asyncio.sleep(0.01)
            return {"status": "ok"}

        coro = fetch()
        assert asyncio.iscoroutine(coro)
        inner = asyncio.run(coro)
        assert asyncio.iscoroutine(inner)

    def test_async_timer_fixed_correct_await(self):
        @async_timer_fixed
        async def fetch():
            await asyncio.sleep(0.01)
            return {"status": "ok"}

        result = asyncio.run(fetch())
        assert result == {"status": "ok"}
        assert fetch._elapsed > 0

    def test_diagnose_async_decorator(self):
        @async_timer_fixed
        async def async_func():
            return "result"

        info = diagnose_async_decorator(async_func)
        assert info["is_async"] is True


class TestSignaturePreservation:
    """测试函数签名保留"""

    def test_bad_decorator_loses_signature(self):
        @bad_decorator
        def add(a: int, b: int) -> int:
            """Add two numbers"""
            return a + b

        assert add.__name__ == "wrapper"
        assert add.__doc__ is None
        assert add.__annotations__ == {}

    def test_good_decorator_preserves_signature(self):
        @good_decorator
        def add(a: int, b: int) -> int:
            """Add two numbers"""
            return a + b

        assert add.__name__ == "add"
        assert add.__doc__ == "Add two numbers"
        assert hasattr(add, "__wrapped__")

    def test_diagnose_signature(self):
        @bad_decorator
        def func_bad():
            """Bad doc"""
            pass

        @good_decorator
        def func_good():
            """Good doc"""
            pass

        bad_info = diagnose_signature(func_bad)
        good_info = diagnose_signature(func_good)

        assert bad_info["is_preserved"] is False
        assert good_info["is_preserved"] is True


class TestDebugTools:
    """测试调试工具函数"""

    def test_get_original(self):
        @good_decorator
        def original():
            """Original"""
            pass

        recovered = get_original(original)
        assert recovered.__name__ == "original"

    def test_count_wrapper_depth(self):
        @good_decorator
        @good_decorator
        @good_decorator
        def deep():
            pass

        assert count_wrapper_depth(deep) == 3

    def test_inspect_closure_trap_no_trap(self):
        def simple():
            return 42

        info = inspect_closure_trap(simple)
        assert info["freevars"] == []
        assert info["trap_detected"] is False


class TestEdgeCasesIntegration:
    """边界情况集成测试"""

    def test_full_flow_order_conflict(self):
        @timer_outer
        @timer_inner
        def process():
            return "result"

        result = process()
        assert result == "result"
        assert process._outer_elapsed >= 0
        assert process._inner_elapsed >= 0

    def test_full_flow_closure_trap_detection(self):
        handlers = create_api_handlers_wrong()
        diagnosis_results = []

        for handler in handlers.values():
            info = inspect_closure_trap(handler)
            if info["trap_detected"]:
                diagnosis_results.append(info["trap_value"])

        assert len(diagnosis_results) == 3
        assert all(v == "orders" for v in diagnosis_results)

    def test_full_flow_async_timer(self):
        @async_timer_fixed
        async def operation():
            await asyncio.sleep(0.05)
            return "done"

        result = asyncio.run(operation())
        elapsed = operation._elapsed

        assert result == "done"
        assert elapsed >= 0.05


class TestProductionLogTracking:
    """测试生产环境日志追踪"""

    def test_log_call_wrong_hardcoded_wrapper(self):
        from app.decorators.ch07_production import log_call_wrong

        @log_call_wrong
        def service(data):
            return f"processed: {data}"

        result = service("test")
        assert result == "processed: test"
        assert service.__name__ == "wrapper"

    def test_log_call_fixed_uses_func_name(self):
        from app.decorators.ch07_production import log_call_fixed

        @log_call_fixed
        def service(data):
            return f"processed: {data}"

        result = service("test")
        assert result == "processed: test"
        assert service.__name__ == "service"

    def test_analyze_logs_detects_wrapper_problem(self):
        from app.decorators.ch07_production import analyze_logs

        wrong_logs = [
            "Calling wrapper with args=('test',)",
            "wrapper returned",
        ]
        analysis = analyze_logs(wrong_logs)
        assert analysis["has_problem"] is True
        assert analysis["wrapper_calls"] == 2

        good_logs = [
            "Calling service with args=('test',)",
            "service returned",
        ]
        analysis = analyze_logs(good_logs)
        assert analysis["has_problem"] is False

    def test_production_log_decorator(self):
        from app.decorators.ch07_production import production_log

        @production_log(level="INFO", include_args=True)
        def service(data):
            return f"processed: {data}"

        result = service("test")
        assert result == "processed: test"
        assert hasattr(service, "_log_config")
        assert service._log_config["level"] == "INFO"


class TestPerformanceTracking:
    """测试性能追踪"""

    def test_performance_tracker_collects_stats(self):
        tracker = PerformanceTracker()

        def track(func):
            def wrapper(*args, **kwargs):
                start = time.time()
                result = func(*args, **kwargs)
                tracker.track(func.__name__, time.time() - start)
                return result
            return wrapper

        @track
        def fast_func():
            return "done"

        for _ in range(10):
            fast_func()

        report = tracker.get_report()
        assert "fast_func" in report
        assert report["fast_func"]["count"] == 10

    def test_performance_tracker_slowest(self):
        from app.decorators.ch07_production import PerformanceTracker

        tracker = PerformanceTracker()
        tracker.track("slow_func", 0.5)
        tracker.track("slow_func", 0.6)
        tracker.track("fast_func", 0.01)

        slowest = tracker.get_slowest(threshold=0.1)
        assert len(slowest) == 2
        assert slowest[0][0] == "slow_func"

    def test_diagnose_performance(self):
        from app.decorators.ch07_production import diagnose_performance

        def fast_func():
            return "done"

        report = diagnose_performance(fast_func, call_count=50)
        assert report["func_name"] == "fast_func"
        assert report["call_count"] == 50
        assert report["avg_ms"] < 1


class TestDecoratorChainErrorLocation:
    """测试装饰器链错误定位"""

    def test_named_decorator_adds_name(self):
        from app.decorators.ch07_production import named_decorator

        @named_decorator("auth")
        def service():
            return "done"

        assert hasattr(service, "__decorator_name__")
        assert service.__decorator_name__ == "auth"

    def test_locate_error_in_chain_success(self):
        from app.decorators.ch07_production import (
            locate_error_in_chain,
            named_decorator,
        )

        @named_decorator("auth")
        @named_decorator("log")
        def service(data):
            return f"processed: {data}"

        info = locate_error_in_chain(service, "ok")
        assert info["success"] is True
        assert info["result"] == "processed: ok"

    def test_locate_error_in_chain_error(self):
        from app.decorators.ch07_production import (
            locate_error_in_chain,
            named_decorator,
        )

        @named_decorator("auth")
        @named_decorator("log")
        def service(data):
            if data == "error":
                raise ValueError("服务错误")
            return "ok"

        info = locate_error_in_chain(service, "error")
        assert info["success"] is False
        assert info["error_type"] == "ValueError"
        assert info["original_location"]["name"] == "service"

    def test_get_decorator_chain(self):
        from app.decorators.ch07_production import (
            get_decorator_chain,
            named_decorator,
        )

        @named_decorator("auth")
        @named_decorator("rate_limit")
        @named_decorator("log")
        def service():
            return "done"

        chain = get_decorator_chain(service)
        assert chain == ["auth", "rate_limit", "log", "service"]


class TestCombinedDecorator:
    """测试组合装饰器"""

    def test_combined_decorator_basic(self):
        from app.decorators.ch07_production import combined_decorator

        @combined_decorator(log_calls=True, track_performance=True)
        def service(data):
            return f"processed: {data}"

        result = service("test")
        assert result == "processed: test"
        assert hasattr(service, "__decorator_name__")
        assert service.__decorator_name__ == "combined"

    def test_combined_decorator_retry(self):
        from app.decorators.ch07_production import combined_decorator

        call_count = 0

        @combined_decorator(log_calls=True, retry_count=2)
        def flaky_service():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ValueError("临时失败")
            return "success"

        result = flaky_service()
        assert result == "success"
        assert call_count == 2

    def test_combined_decorator_config(self):
        from app.decorators.ch07_production import combined_decorator

        @combined_decorator(log_calls=False, track_performance=True)
        def service():
            return "done"

        result = service()
        assert result == "done"
        assert hasattr(service, "_config")
        assert service._config["log_calls"] is False