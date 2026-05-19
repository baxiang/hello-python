"""第 7 章调试路由 — 边界情况与调试实战演示"""

import asyncio
import time

from fastapi import APIRouter

from app.decorators.ch07_edge_cases import (
    async_timer_fixed,
    bad_decorator,
    catch_errors,
    catch_errors_preserve,
    catch_errors_swallow,
    create_api_handlers_fixed,
    create_api_handlers_wrong,
    create_callbacks_fixed,
    create_callbacks_wrong,
    demo_async_fetch,
    demo_process_with_sleep,
    good_decorator,
    log_decorator_usage,
    retry_simple,
    sync_timer_wrong,
    timer_a,
    timer_b,
    timer_inner,
    timer_outer,
)
from app.decorators.ch07_debug_tools import (
    diagnose_async_decorator,
    diagnose_signature,
    inspect_closure_trap,
    test_async_result,
)

router = APIRouter(prefix="/api/v1/debug", tags=["ch07: 边界情况与调试"])


# ─────────────────────────────────────
# 7.1 装饰器叠加顺序问题
# ─────────────────────────────────────

@timer_a
@timer_b
def _process_wrong_order():
    time.sleep(0.01)
    return "done"


@timer_outer
@timer_inner
def _process_fixed_order():
    time.sleep(0.01)
    return "done"


@router.get("/order-conflict")
def demo_order_conflict() -> dict:
    """装饰器叠加顺序 — 属性冲突演示"""
    wrong_result = _process_wrong_order()
    fixed_result = _process_fixed_order()

    inner_elapsed = getattr(
        getattr(_process_wrong_order, "__wrapped__", None),
        "_last_elapsed",
        None,
    )

    return {
        "result": wrong_result,
        "wrong_order": {
            "elapsed_ms": f"{_process_wrong_order._last_elapsed * 1000:.2f}",
            "source": _process_wrong_order._source,
            "inner_elapsed_accessible": inner_elapsed is not None,
            "inner_elapsed_ms": f"{inner_elapsed * 1000:.2f}" if inner_elapsed else None,
        },
        "fixed_order": {
            "outer_elapsed_ms": f"{_process_fixed_order._outer_elapsed * 1000:.2f}",
            "inner_elapsed_ms": f"{_process_fixed_order._inner_elapsed * 1000:.2f}",
        },
    }


@catch_errors
@retry_simple
def _unstable_api_call():
    raise ValueError("模拟失败")


@router.get("/exception-order")
def demo_exception_order() -> dict:
    """异常处理顺序演示"""
    result = _unstable_api_call()
    return {
        "result": result,
        "note": "catch_errors 在外层捕获 retry_simple 放弃后的异常",
    }


# ─────────────────────────────────────
# 7.2 装饰器嵌套与元装饰器
# ─────────────────────────────────────

@log_decorator_usage
def _simple_timer(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"耗时: {time.perf_counter() - start:.4f}s")
        return result
    return wrapper


@router.get("/meta-decorator")
def demo_meta_decorator() -> dict:
    """元装饰器演示"""

    @_simple_timer
    def greet(name: str = "World"):
        return f"Hello, {name}!"

    return {
        "decorator_name": getattr(_simple_timer, "_last_decorator", None),
        "decorated_func": getattr(_simple_timer, "_last_decorated", None),
        "result": greet("Python"),
    }


# ─────────────────────────────────────
# 7.3 闭包变量绑定陷阱
# ─────────────────────────────────────

@router.get("/closure-trap")
def demo_closure_trap() -> dict:
    """循环变量陷阱演示"""
    wrong_handlers = create_api_handlers_wrong()
    fixed_handlers = create_api_handlers_fixed()

    wrong_results = {k: v() for k, v in wrong_handlers.items()}
    fixed_results = {k: v() for k, v in fixed_handlers.items()}

    wrong_inspection = {
        k: inspect_closure_trap(v) for k, v in wrong_handlers.items()
    }
    fixed_inspection = {
        k: inspect_closure_trap(v) for k, v in fixed_handlers.items()
    }

    return {
        "wrong_handlers": wrong_results,
        "wrong_closure_inspection": wrong_inspection,
        "fixed_handlers": fixed_results,
        "fixed_closure_inspection": fixed_inspection,
    }


@router.get("/binding-time")
def demo_binding_time() -> dict:
    """late-binding vs early-binding 对比"""
    wrong_callbacks = create_callbacks_wrong()
    fixed_callbacks = create_callbacks_fixed()

    wrong_results = [cb() for cb in wrong_callbacks]
    fixed_results = [cb() for cb in fixed_callbacks]

    return {
        "wrong_results": wrong_results,
        "wrong_note": "late-binding: 全是 4 (循环结束后 i=2)",
        "fixed_results": fixed_results,
        "fixed_note": "early-binding: 默认参数在定义时捕获",
    }


# ─────────────────────────────────────
# 7.4 async 与方法装饰器兼容性
# ─────────────────────────────────────

@sync_timer_wrong
async def _async_fetch_wrong():
    await asyncio.sleep(0.1)
    return {"status": "ok"}


@async_timer_fixed
async def _async_fetch_fixed():
    await asyncio.sleep(0.1)
    return {"status": "ok"}


@router.get("/async-await-missing")
async def demo_async_await_missing() -> dict:
    """async 装饰器 await 遗漏演示"""
    wrong_coroutine = _async_fetch_wrong()
    wrong_type = type(wrong_coroutine).__name__

    fixed_result = await _async_fetch_fixed()

    try:
        wrong_inner = await wrong_coroutine
        wrong_inner_type = type(wrong_inner).__name__
    except Exception:
        wrong_inner = None
        wrong_inner_type = "error"

    return {
        "wrong_result_type": wrong_type,
        "wrong_elapsed": f"{_async_fetch_wrong._elapsed * 1000:.2f}ms",
        "wrong_inner_type": wrong_inner_type,
        "wrong_note": "sync_timer_wrong 没有 await，返回 coroutine",
        "fixed_result_type": type(fixed_result).__name__,
        "fixed_result": fixed_result,
        "fixed_elapsed_ms": f"{_async_fetch_fixed._elapsed * 1000:.2f}",
    }


# ─────────────────────────────────────
# 7.5 函数签名丢失调试
# ─────────────────────────────────────

@bad_decorator
def _add_bad(a: int, b: int) -> int:
    """计算两个数的和"""
    return a + b


@good_decorator
def _add_good(a: int, b: int) -> int:
    """计算两个数的和"""
    return a + b


@router.get("/signature-lost")
def demo_signature_lost() -> dict:
    """函数签名丢失调试"""
    bad_info = diagnose_signature(_add_bad)
    good_info = diagnose_signature(_add_good)

    return {
        "bad_decorator_info": bad_info,
        "good_decorator_info": good_info,
        "bad_result": _add_bad(1, 2),
        "good_result": _add_good(1, 2),
    }


# ─────────────────────────────────────
# 7.6 异常栈被吞掉调试
# ─────────────────────────────────────

@catch_errors_swallow
def _raise_error_swallow():
    raise ValueError("数据无效")


@catch_errors_preserve
def _raise_error_preserve():
    raise ValueError("数据无效")


@router.get("/stack-swallowed")
def demo_stack_swallowed() -> dict:
    """异常栈被吞掉调试"""
    swallow_result = _raise_error_swallow()

    preserve_error = None
    preserve_traceback = None
    try:
        _raise_error_preserve()
    except RuntimeError as e:
        preserve_error = str(e)
        preserve_traceback = getattr(_raise_error_preserve, "_last_traceback", None)

    return {
        "swallow_result": swallow_result,
        "swallow_note": "异常栈丢失，只返回 error 字典",
        "preserve_error": preserve_error,
        "preserve_traceback": preserve_traceback,
        "preserve_note": "使用 raise ... from e 保留异常链",
    }


# ─────────────────────────────────────
# 7.7 循环变量陷阱现场排查
# ─────────────────────────────────────

@router.get("/closure-diagnosis")
def demo_closure_diagnosis() -> dict:
    """闭包陷阱诊断工具演示"""
    handlers = create_api_handlers_wrong()

    diagnosis = {}
    for name, handler in handlers.items():
        info = inspect_closure_trap(handler)
        diagnosis[name] = {
            "freevars": info["freevars"],
            "contents": info["contents"],
            "trap_detected": info["trap_detected"],
        }

    return {
        "handlers_result": {k: v() for k, v in handlers.items()},
        "diagnosis": diagnosis,
        "summary": "所有 handler 的 contents 都是 ['orders']，共享同一个变量",
    }


# ─────────────────────────────────────
# 7.8 async await 遗漏排查
# ─────────────────────────────────────

@router.get("/async-diagnosis")
async def demo_async_diagnosis() -> dict:
    """async await 遗漏诊断演示"""

    async def correct_async():
        await asyncio.sleep(0.05)
        return {"type": "dict"}

    async def broken_async():
        await asyncio.sleep(0.05)
        return {"type": "dict"}

    broken_wrapper = sync_timer_wrong(broken_async)
    correct_wrapper = async_timer_fixed(correct_async)

    broken_info = diagnose_async_decorator(broken_wrapper)
    correct_info = diagnose_async_decorator(correct_wrapper)

    broken_test = await test_async_result(broken_wrapper)
    correct_test = await test_async_result(correct_wrapper)

    return {
        "broken_decorator_info": broken_info,
        "broken_test": broken_test,
        "correct_decorator_info": correct_info,
        "correct_test": correct_test,
    }


# ─────────────────────────────────────
# Part D: 生产环境调试实战
# ─────────────────────────────────────

from app.decorators.ch07_production import (
    analyze_logs,
    combined_decorator,
    diagnose_performance,
    get_decorator_chain,
    locate_error_in_chain,
    log_call_fixed,
    log_call_wrong,
    named_decorator,
    tracker,
    track_performance,
)


# 7.11 日志追踪问题

@log_call_wrong
def _service_wrong(data: str) -> str:
    return f"processed: {data}"


@log_call_fixed
def _service_fixed(data: str) -> str:
    return f"processed: {data}"


@router.get("/log-tracking")
def demo_log_tracking() -> dict:
    """日志追踪问题演示"""
    wrong_logs = [
        "Calling wrapper with args=('test',)",
        "wrapper returned",
    ]
    fixed_logs = [
        "Calling _service_fixed with args=('test',)",
        "_service_fixed returned",
    ]
    
    wrong_analysis = analyze_logs(wrong_logs)
    fixed_analysis = analyze_logs(fixed_logs)
    
    wrong_result = _service_wrong("test")
    fixed_result = _service_fixed("test")
    
    return {
        "wrong_logs": wrong_logs,
        "wrong_analysis": wrong_analysis,
        "fixed_logs": fixed_logs,
        "fixed_analysis": fixed_analysis,
        "wrong_result": wrong_result,
        "fixed_result": fixed_result,
    }


# 7.12 性能瓶颈追踪

@track_performance
def _slow_api_call() -> str:
    import time
    time.sleep(0.02)
    return "done"


@track_performance
def _fast_api_call() -> str:
    return "done"


@router.get("/performance-analysis")
def demo_performance_analysis() -> dict:
    """性能瓶颈追踪演示"""
    tracker.clear()
    
    for _ in range(10):
        _slow_api_call()
    
    for _ in range(20):
        _fast_api_call()
    
    report = tracker.get_report()
    slowest = tracker.get_slowest(threshold=0.01)
    
    slow_perf = diagnose_performance(lambda: _slow_api_call(), call_count=5)
    fast_perf = diagnose_performance(lambda: _fast_api_call(), call_count=100)
    
    return {
        "tracker_report": report,
        "slowest_calls": slowest[:5],
        "slow_function_perf": slow_perf,
        "fast_function_perf": fast_perf,
    }


# 7.13 复杂装饰器链错误定位

@named_decorator("auth")
@named_decorator("rate_limit")
@named_decorator("cache")
@named_decorator("log")
def _chain_service(data: str) -> str:
    if data == "error":
        raise ValueError("服务错误")
    return f"result: {data}"


@router.post("/locate-error")
def demo_locate_error(data: str = "ok") -> dict:
    """复杂装饰器链错误定位"""
    chain = get_decorator_chain(_chain_service)
    
    if data == "error":
        error_info = locate_error_in_chain(_chain_service, data)
        return {
            "decorator_chain": chain,
            "error_info": error_info,
        }
    
    result = _chain_service(data)
    return {
        "decorator_chain": chain,
        "success": True,
        "result": result,
    }


# 组合装饰器演示

@combined_decorator(log_calls=True, track_performance=True, retry_count=2)
def _combined_service(data: str) -> str:
    if data == "fail_once":
        import time
        if not hasattr(_combined_service, "_attempt"):
            _combined_service._attempt = 0
        _combined_service._attempt += 1
        if _combined_service._attempt < 2:
            raise ValueError("临时失败")
        return "success after retry"
    return f"processed: {data}"


@router.get("/combined-decorator")
def demo_combined_decorator(data: str = "ok") -> dict:
    """组合装饰器演示"""
    result = _combined_service(data)
    config = getattr(_combined_service, "_config", {})
    elapsed = getattr(_combined_service, "_last_elapsed", 0.0)
    
    return {
        "result": result,
        "config": config,
        "elapsed_ms": f"{elapsed * 1000:.2f}",
        "decorator_name": getattr(_combined_service, "__decorator_name__", "unknown"),
    }


# ─────────────────────────────────────
# 综合端点
# ─────────────────────────────────────

@router.get("/summary")
def demo_summary() -> dict:
    """第 7 章综合摘要"""
    return {
        "chapter": "第 7 章 — 装饰器边界情况与调试实战",
        "topics": [
            "7.1 装饰器叠加顺序问题",
            "7.2 装饰器嵌套与元装饰器",
            "7.3 闭包变量绑定陷阱",
            "7.4 async 与方法装饰器兼容性",
            "7.5 函数签名丢失调试",
            "7.6 异常栈被吞掉调试",
            "7.7 循环变量陷阱现场排查",
            "7.8 async await 遗漏排查",
            "7.11 日志追踪问题",
            "7.12 性能瓶颈追踪",
            "7.13 复杂装饰器链错误定位",
        ],
        "endpoints": {
            "order-conflict": "装饰器叠加顺序",
            "closure-trap": "循环变量陷阱",
            "async-await-missing": "async await 遗漏",
            "signature-lost": "函数签名丢失",
            "stack-swallowed": "异常栈被吞掉",
            "log-tracking": "日志追踪问题",
            "performance-analysis": "性能瓶颈追踪",
            "locate-error": "装饰器链错误定位",
            "combined-decorator": "组合装饰器演示",
        },
    }