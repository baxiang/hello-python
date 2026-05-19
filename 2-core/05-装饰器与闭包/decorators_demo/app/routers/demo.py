"""第 3 章演示路由 — 日志 + 计时装饰器

访问 /api/v1/demo/hello 观察日志和计时效果。
"""

from fastapi import APIRouter

from app.decorators.ch03_basics import log_call, timer

router = APIRouter(prefix="/api/v1/demo", tags=["ch03: 装饰器核心原理"])


@log_call
@timer
def _process_data(data: str) -> dict[str, str]:
    """模拟数据处理 — 被两个装饰器包装"""
    return {"processed": data, "status": "ok"}


@router.get("/hello")
def demo_hello(name: str = "World") -> dict[str, str]:
    """演示：被装饰器包装的函数

    观察响应中的 elapsed_ms 字段，以及控制台输出的日志。
    访问 /docs 可查看交互式 API 文档。
    """
    result = _process_data(name)
    return {**result, "elapsed_ms": f"{_process_data._last_elapsed * 1000:.2f}"}  # type: ignore[attr-defined]


@router.get("/wraps-comparison")
def demo_wraps_comparison() -> dict[str, dict[str, str | None]]:
    """演示：@wraps 保留元信息 vs 不用 @wraps 丢失元信息"""
    from app.decorators.ch03_basics import bad_decorator, simple_decorator

    def my_func() -> str:
        """这是原函数的文档字符串"""
        return "result"

    good_version = simple_decorator(my_func)
    bad_version = bad_decorator(my_func)

    return {
        "with_wraps": {
            "__name__": good_version.__name__,
            "__doc__": good_version.__doc__,
        },
        "without_wraps": {
            "__name__": bad_version.__name__,
            "__doc__": bad_version.__doc__,
        },
    }
