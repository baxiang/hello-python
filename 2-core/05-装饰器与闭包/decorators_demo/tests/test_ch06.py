"""第 6 章测试 — 装饰器高级用法"""

import asyncio

from app.decorators.ch06_advanced import (
    CountCalls,
    Singleton,
    async_timer,
    get_original_func,
    is_decorated,
    timer_precise,
)


class TestAdvancedDecorators:
    """测试高级装饰器"""

    def test_timer_precise_preserves_signature(self):
        @timer_precise
        def add(a: int, b: int) -> int:
            return a + b

        assert add(1, 2) == 3
        assert add.__name__ == "add"

    def test_async_timer(self):
        @async_timer
        async def slow():
            await asyncio.sleep(0.01)
            return "done"

        result = asyncio.run(slow())
        assert result == "done"
        assert slow._last_elapsed > 0  # type: ignore[attr-defined]

    def test_count_calls(self):
        @CountCalls
        def greet(name: str) -> str:
            return f"Hello, {name}!"

        assert greet("Alice") == "Hello, Alice!"
        assert greet.count == 1
        assert greet("Bob") == "Hello, Bob!"
        assert greet.count == 2

    def test_count_calls_preserves_name(self):
        @CountCalls
        def my_func() -> None:
            pass

        assert my_func.__name__ == "my_func"

    def test_singleton(self):
        @Singleton
        class Config:
            def __init__(self, dsn: str) -> None:
                self.dsn = dsn

        c1 = Config("redis://localhost")
        c2 = Config("redis://other")
        assert c1 is c2
        assert c1.dsn == "redis://localhost"

    def test_singleton_reset(self):
        @Singleton
        class Service:
            def __init__(self, name: str) -> None:
                self.name = name

        s1 = Service("first")
        Service.reset()
        s2 = Service("second")
        assert s1 is not s2
        assert s2.name == "second"

    def test_is_decorated(self):
        @timer_precise
        def decorated():
            pass

        def plain():
            pass

        assert is_decorated(decorated) is True
        assert is_decorated(plain) is False

    def test_get_original_func(self):
        def original():
            """Original doc"""
            pass

        decorated = timer_precise(original)
        recovered = get_original_func(decorated)
        assert recovered is original
        assert recovered.__doc__ == "Original doc"
