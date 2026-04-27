"""第 7 章测试 — 装饰器边界情况与调试实战"""

import asyncio

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