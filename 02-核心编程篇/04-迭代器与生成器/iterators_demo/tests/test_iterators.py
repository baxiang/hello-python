"""迭代器测试"""

from app.core.iterators import Counter, countdown, fibonacci_generator, chain


def test_counter():
    c = Counter(1, 5)
    result = list(c)
    assert result == [1, 2, 3, 4]


def test_countdown():
    result = list(countdown(5))
    assert result == [5, 4, 3, 2, 1]


def test_fibonacci_generator():
    result = list(fibonacci_generator(10))
    assert result == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


def test_chain():
    result = list(chain([1, 2], [3, 4], [5, 6]))
    assert result == [1, 2, 3, 4, 5, 6]