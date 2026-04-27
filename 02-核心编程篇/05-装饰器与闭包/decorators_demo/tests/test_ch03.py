"""第 3 章测试 — 装饰器核心原理"""

from app.decorators.ch03_basics import (
    bad_decorator,
    clear_call_log,
    get_call_log,
    log_call,
    simple_decorator,
    timer,
)


class TestDecoratorBasics:
    """测试装饰器的核心概念"""

    def setup_method(self):
        clear_call_log()

    def test_simple_decorator_preserves_name(self):
        """@wraps 保留 __name__"""

        @simple_decorator
        def my_func() -> str:
            return "ok"

        assert my_func.__name__ == "my_func"

    def test_simple_decorator_preserves_docstring(self):
        """@wraps 保留 __doc__"""

        @simple_decorator
        def my_func() -> str:
            """这是文档"""
            return "ok"

        assert my_func.__doc__ == "这是文档"

    def test_bad_decorator_loses_metadata(self):
        """不用 @wraps 丢失元信息"""

        @bad_decorator
        def my_func() -> str:
            """这是文档"""
            return "ok"

        assert my_func.__name__ == "wrapper"
        assert my_func.__doc__ is None

    def test_log_call_records_calls(self):
        """日志装饰器记录调用信息"""

        @log_call
        def add(a: int, b: int) -> int:
            return a + b

        result = add(1, 2)
        assert result == 3

        log = get_call_log()
        assert len(log) == 2
        assert log[0]["func"] == "add"
        assert log[0]["status"] == "calling"
        assert log[1]["status"] == "returned"
        assert log[1]["result"] == 3

    def test_timer_records_elapsed(self):
        """计时装饰器记录耗时"""

        @timer
        def fast() -> str:
            return "fast"

        fast()
        assert fast._last_elapsed >= 0  # type: ignore[attr-defined]

    def test_stacked_decorators(self):
        """多层装饰器：从下往上包装，从上往下执行"""
        call_order: list[str] = []

        def deco_a(func):
            def wrapper(*args, **kwargs):
                call_order.append("A-before")
                result = func(*args, **kwargs)
                call_order.append("A-after")
                return result

            return wrapper

        def deco_b(func):
            def wrapper(*args, **kwargs):
                call_order.append("B-before")
                result = func(*args, **kwargs)
                call_order.append("B-after")
                return result

            return wrapper

        @deco_a
        @deco_b
        def target():
            call_order.append("target")

        target()
        assert call_order == ["A-before", "B-before", "target", "B-after", "A-after"]
