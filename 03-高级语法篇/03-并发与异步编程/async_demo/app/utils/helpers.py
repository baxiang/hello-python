"""辅助函数"""

import asyncio
from typing import Callable, Any


async def run_with_timeout(coro: Any, timeout: float) -> Any:
    """带超时运行协程"""
    return await asyncio.wait_for(coro, timeout=timeout)