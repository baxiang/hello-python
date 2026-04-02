"""迭代器示例"""

from typing import Iterator, Generator


class Counter:
    """自定义迭代器"""
    
    def __init__(self, start: int, end: int):
        self.current = start
        self.end = end
    
    def __iter__(self) -> "Counter":
        return self
    
    def __next__(self) -> int:
        if self.current >= self.end:
            raise StopIteration
        value = self.current
        self.current += 1
        return value


def countdown(n: int) -> Generator[int, None, None]:
    """倒计时生成器"""
    while n > 0:
        yield n
        n -= 1


def fibonacci_generator(n: int) -> Generator[int, None, None]:
    """斐波那契生成器"""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b


def chain(*iterables) -> Generator:
    """连接多个可迭代对象"""
    for iterable in iterables:
        yield from iterable


def infinite_counter() -> Generator[int, None, None]:
    """无限计数器"""
    n = 0
    while True:
        yield n
        n += 1