"""函数测试"""

from app.core.functions import greet, factorial, fibonacci, apply_operation


def test_greet():
    assert greet("Python") == "Hello, Python!"


def test_factorial():
    assert factorial(5) == 120
    assert factorial(0) == 1


def test_fibonacci():
    assert fibonacci(10) == 55


def test_apply_operation():
    assert apply_operation(5, 3, lambda x, y: x + y) == 8