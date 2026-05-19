"""辅助函数 — 错误处理上下文"""

from collections.abc import Generator
from contextlib import contextmanager


@contextmanager
def safe_execute() -> Generator[None, None, None]:
    """安全执行上下文：捕获并记录异常，但不吞掉异常

    用法：
        with safe_execute():
            do_something_risky()
        # 异常会被打印但仍会向上传播
    """
    try:
        yield
    except Exception as e:
        print(f"[safe_execute] 捕获异常: {type(e).__name__}: {e}")
        raise
