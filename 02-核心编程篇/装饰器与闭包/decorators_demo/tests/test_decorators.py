"""装饰器测试"""

from app.core.decorators import memoize, repeat
from app.utils.helpers import counter


def test_memoize():
    @memoize
    def fib(n):
        if n <= 1:
            return n
        return fib(n - 1) + fib(n - 2)
    
    assert fib(10) == 55


def test_repeat():
    @repeat(3)
    def say_hello():
        return "hello"
    
    result = say_hello()
    assert len(result) == 3
    assert result[0] == "hello"


def test_counter():
    cnt = counter()
    assert cnt() == 1
    assert cnt() == 2
    assert cnt() == 3