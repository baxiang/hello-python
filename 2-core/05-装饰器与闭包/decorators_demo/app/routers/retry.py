"""第 4 章重试路由 — @retry 装饰器演示"""

from fastapi import APIRouter

from app.decorators.ch04_parameterized import retry

router = APIRouter(prefix="/api/v1/retry", tags=["ch04: 重试机制"])

_attempt_count = 0


@retry(max_attempts=3, delay=0.0, exceptions=(ConnectionError,))
def _unstable_api() -> dict:
    global _attempt_count
    _attempt_count += 1
    if _attempt_count < 3:
        raise ConnectionError("连接失败")
    return {"status": "success", "attempts": _attempt_count}


@router.post("/fetch")
def api_retry_demo() -> dict:
    """演示重试机制"""
    global _attempt_count
    _attempt_count = 0
    return _unstable_api()
