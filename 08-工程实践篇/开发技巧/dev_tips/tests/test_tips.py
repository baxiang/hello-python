"""开发技巧测试"""

from app.core.tips import fibonacci_cached, Timer


def test_fibonacci_cached():
    assert fibonacci_cached(10) == 55
    assert fibonacci_cached(20) == 6765


def test_timer():
    with Timer("测试"):
        sum(range(10000))