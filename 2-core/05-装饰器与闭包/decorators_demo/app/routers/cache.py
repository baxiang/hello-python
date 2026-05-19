"""第 5 章缓存路由 — @lru_cache 装饰器演示"""

import time

from fastapi import APIRouter

from app.decorators.ch05_functools import (
    fibonacci,
    fibonacci_without_cache,
    parse_config,
)

router = APIRouter(prefix="/api/v1/cache", tags=["ch05: functools 缓存"])


@router.get("/fibonacci/{n}")
def demo_fibonacci(n: int) -> dict:
    """斐波那契 — 有缓存 vs 无缓存"""
    start = time.perf_counter()
    result = fibonacci(n)
    cached_time = time.perf_counter() - start

    start = time.perf_counter()
    fibonacci_without_cache(n)
    no_cache_time = time.perf_counter() - start

    return {
        "n": n,
        "result": result,
        "cached_time_ms": f"{cached_time * 1000:.4f}",
        "no_cache_time_ms": f"{no_cache_time * 1000:.4f}",
        "speedup": f"{no_cache_time / max(cached_time, 1e-9):.0f}x",
    }


@router.get("/config/{key}")
def demo_config(key: str) -> dict:
    """配置缓存 — 首次慢、后续快"""
    start = time.perf_counter()
    result = parse_config(key)
    elapsed = time.perf_counter() - start

    info = parse_config.cache_info()

    return {
        **result,
        "elapsed_ms": f"{elapsed * 1000:.4f}",
        "cache_info": {
            "hits": info.hits,
            "misses": info.misses,
            "maxsize": info.maxsize,
            "currsize": info.currsize,
        },
    }
