from functools import (
    cached_property,
    lru_cache,
    partial,
    reduce,
    singledispatch,
    total_ordering,
    wraps,
)
from typing import Any


@lru_cache(maxsize=128)
def fibonacci_cached(n: int) -> int:
    if n <= 1:
        return n
    return fibonacci_cached(n - 1) + fibonacci_cached(n - 2)


def get_cache_info():
    return fibonacci_cached.cache_info()


def clear_cache():
    fibonacci_cached.cache_clear()


def create_multiplier(factor: int):
    return partial(lambda x, f: x * f, f=factor)


def multiply_all(numbers: list, initial: int = 1) -> int:
    return reduce(lambda x, y: x * y, numbers, initial)


def preserve_decorator_info(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


@total_ordering
class ComparablePoint:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)


def create_comparable_point(x: int, y: int) -> ComparablePoint:
    return ComparablePoint(x, y)


@singledispatch
def process_data(data: Any) -> str:
    return f"Unknown type: {type(data).__name__}"


@process_data.register
def _(data: int) -> str:
    return f"Integer: {data}"


@process_data.register
def _(data: str) -> str:
    return f"String: {data}"


@process_data.register(list)
def _(data: list) -> str:
    return f"List with {len(data)} items"


class CachedPropertyDemo:
    def __init__(self):
        self.call_count = 0

    @cached_property
    def expensive_value(self) -> int:
        self.call_count += 1
        return 42


def cached_property_demo() -> CachedPropertyDemo:
    return CachedPropertyDemo()
