"""辅助函数"""

from typing import Any


def debug_print(*args, **kwargs) -> None:
    """调试打印"""
    import inspect
    caller = inspect.currentframe().f_back
    print(f"[{caller.f_code.co_filename}:{caller.f_lineno}] ", end="")
    print(*args, **kwargs)