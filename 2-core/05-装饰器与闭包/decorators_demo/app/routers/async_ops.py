"""第 6 章异步路由 — async 装饰器演示"""

import asyncio

from fastapi import APIRouter

from app.decorators.ch06_advanced import async_timer, timer_precise

router = APIRouter(prefix="/api/v1/async", tags=["ch06: 高级用法"])


@async_timer
async def _slow_operation(delay_ms: float) -> dict:
    """模拟异步操作"""
    await asyncio.sleep(delay_ms / 1000)
    return {"delay_ms": delay_ms, "status": "done"}


@timer_precise
def _sync_slow_operation(delay_ms: float) -> dict:
    """同步对比"""
    import time
    time.sleep(delay_ms / 1000)
    return {"delay_ms": delay_ms, "status": "done"}


@router.get("/call/{delay_ms}")
async def demo_async(delay_ms: float = 100) -> dict:
    """异步操作 — 装饰器正确 await"""
    result = await _slow_operation(delay_ms)
    return {
        **result,
        "elapsed_ms": f"{_slow_operation._last_elapsed * 1000:.2f}",  # type: ignore[attr-defined]
    }


@router.get("/sync/{delay_ms}")
def demo_sync(delay_ms: float = 100) -> dict:
    """同步操作对比"""
    result = _sync_slow_operation(delay_ms)
    return {
        **result,
        "elapsed_ms": f"{_sync_slow_operation._last_elapsed * 1000:.2f}",  # type: ignore[attr-defined]
    }


@router.get("/count-calls")
def demo_count_calls() -> dict:
    """类装饰器 — 调用次数统计"""
    from app.decorators.ch06_advanced import CountCalls

    @CountCalls
    def greet(name: str) -> str:
        return f"Hello, {name}!"

    greet("Alice")
    greet("Bob")
    greet("Charlie")

    return {
        "greeting": greet("Final"),
        "total_calls": greet.count,
    }
