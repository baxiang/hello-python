"""辅助函数"""

from contextlib import contextmanager
from typing import Generator


@contextmanager
def error_handler() -> Generator[None, None, None]:
    """错误处理上下文"""
    try:
        yield
    except Exception as e:
        print(f"捕获异常: {e}")