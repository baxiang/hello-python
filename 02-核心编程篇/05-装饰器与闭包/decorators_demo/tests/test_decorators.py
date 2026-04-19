"""装饰器与闭包测试套件 — API 请求处理中间件，覆盖第01-04章"""

import pytest

from app.core.decorators import (
    expensive_parse,
    log_call,
    make_counter,
    make_prefixed_logger,
    make_rate_limiter,
    retry,
    singleton,
    timer,
    validate_positive,
)


# ===========================================================================
# ch01: 装饰器基础
# ===========================================================================
class TestDecoratorBasics:
    """ch01: @语法糖；functools.wraps 保留 __name__ / __doc__"""

    def test_log_call_preserves_name(self):
        @log_call
        def my_handler():
            """处理请求"""
            return "ok"

        assert my_handler.__name__ == "my_handler"
        assert my_handler.__doc__ == "处理请求"

    def test_log_call_returns_result(self):
        @log_call
        def add(a: int, b: int) -> int:
            return a + b

        assert add(1, 2) == 3

    def test_log_call_marks_decorated(self):
        @log_call
        def fn():
            return 1

        assert fn._decorated is True  # type: ignore[attr-defined]

    def test_timer_preserves_name(self):
        @timer
        def process():
            """耗时处理"""
            return 42

        assert process.__name__ == "process"
        assert process.__doc__ == "耗时处理"

    def test_timer_records_elapsed(self):
        @timer
        def fast():
            return "fast"

        fast()
        assert fast.last_elapsed >= 0  # type: ignore[attr-defined]


# ===========================================================================
# ch02: 闭包与 nonlocal
# ===========================================================================
class TestClosureAndNonlocal:
    """ch02: 自由变量捕获；nonlocal 修改外层状态；每个闭包独立"""

    def test_make_counter_increments(self):
        inc = make_counter(0)
        assert inc() == 1
        assert inc() == 2
        assert inc() == 3

    def test_make_counter_initial_value(self):
        inc = make_counter(10)
        assert inc() == 11

    def test_two_counters_are_independent(self):
        a = make_counter(0)
        b = make_counter(0)
        a()
        a()
        assert b() == 1

    def test_rate_limiter_allows_calls_within_limit(self):
        limiter = make_rate_limiter(3)

        @limiter
        def api_call() -> str:
            return "ok"

        assert api_call() == "ok"
        assert api_call() == "ok"
        assert api_call() == "ok"

    def test_rate_limiter_raises_on_exceed(self):
        limiter = make_rate_limiter(2)

        @limiter
        def api_call() -> str:
            return "ok"

        api_call()
        api_call()
        with pytest.raises(RuntimeError, match="超限"):
            api_call()

    def test_rate_limiter_reset(self):
        limiter = make_rate_limiter(1)

        @limiter
        def fn() -> int:
            return 1

        fn()
        fn.reset()  # type: ignore[attr-defined]
        assert fn() == 1

    def test_rate_limiter_call_count(self):
        limiter = make_rate_limiter(5)

        @limiter
        def fn() -> None:
            pass

        fn()
        fn()
        assert fn.call_count() == 2  # type: ignore[attr-defined]


# ===========================================================================
# ch03: functools.lru_cache / partial
# ===========================================================================
class TestFunctools:
    """ch03: lru_cache 缓存；partial 偏函数"""

    def setup_method(self):
        expensive_parse.cache_clear()

    def test_lru_cache_returns_same_result(self):
        r1 = expensive_parse("/api/v1")
        r2 = expensive_parse("/api/v1")
        assert r1 == r2
        assert r1["path"] == "/api/v1"

    def test_lru_cache_caches_calls(self):
        expensive_parse("/api/v2")
        expensive_parse("/api/v2")
        info = expensive_parse.cache_info()
        assert info.hits >= 1

    def test_partial_prefixed_logger(self):
        warn = make_prefixed_logger("WARN")
        error = make_prefixed_logger("ERROR")
        assert warn("磁盘满") == "[WARN] 磁盘满"
        assert error("连接超时") == "[ERROR] 连接超时"

    def test_partial_loggers_independent(self):
        info = make_prefixed_logger("INFO")
        debug = make_prefixed_logger("DEBUG")
        assert info("启动") == "[INFO] 启动"
        assert debug("断点") == "[DEBUG] 断点"


# ===========================================================================
# ch04: 带参数的装饰器；叠加装饰器；类装饰器
# ===========================================================================
class TestAdvancedDecorators:
    """ch04: retry 带参数装饰器；@validate_positive + @retry 叠加；singleton 类装饰器"""

    def test_retry_succeeds_first_attempt(self):
        @retry(max_attempts=3)
        def flaky() -> str:
            return "ok"

        assert flaky() == "ok"

    def test_retry_retries_on_failure(self):
        call_count = 0

        @retry(max_attempts=3, exceptions=(ValueError,))
        def unstable() -> str:
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("暂时失败")
            return "success"

        result = unstable()
        assert result == "success"
        assert call_count == 3

    def test_retry_raises_after_max_attempts(self):
        @retry(max_attempts=2, exceptions=(RuntimeError,))
        def always_fail() -> None:
            raise RuntimeError("持续失败")

        with pytest.raises(RuntimeError):
            always_fail()

    def test_retry_preserves_name(self):
        @retry(max_attempts=2)
        def my_func() -> None:
            pass

        assert my_func.__name__ == "my_func"

    def test_validate_positive_passes(self):
        @validate_positive
        def sqrt(x: float) -> float:
            return x ** 0.5

        assert sqrt(4.0) == pytest.approx(2.0)

    def test_validate_positive_raises_on_zero(self):
        @validate_positive
        def sqrt(x: float) -> float:
            return x ** 0.5

        with pytest.raises(ValueError, match="正数"):
            sqrt(0)

    def test_stacked_decorators(self):
        """叠加装饰器：@validate_positive + @retry 组合使用"""
        attempt = 0

        @validate_positive
        @retry(max_attempts=2, exceptions=(RuntimeError,))
        def process(value: float) -> float:
            nonlocal attempt
            attempt += 1
            if attempt < 2:
                raise RuntimeError("临时错误")
            return value * 2

        result = process(5.0)
        assert result == pytest.approx(10.0)

    def test_singleton_class_decorator(self):
        @singleton
        class Config:
            def __init__(self, dsn: str) -> None:
                self.dsn = dsn

        c1 = Config("redis://localhost")
        c2 = Config("redis://other")
        assert c1 is c2

    def test_singleton_reset(self):
        @singleton
        class Service:
            def __init__(self, name: str) -> None:
                self.name = name

        s1 = Service("first")
        Service.reset()  # type: ignore[attr-defined]
        s2 = Service("second")
        assert s1 is not s2
        assert s2.name == "second"