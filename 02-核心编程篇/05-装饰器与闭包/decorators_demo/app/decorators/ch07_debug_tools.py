"""第 7 章 — 谅试工具函数

提供用于诊断装饰器问题的工具函数：签名检查、闭包陷阱检测、async await 遗漏排查等。
"""

from __future__ import annotations

import asyncio
import inspect
import sys
import traceback
from collections.abc import Callable
from typing import Any


# ─────────────────────────────────────
# 7.5 函数签名丢失调试
# ─────────────────────────────────────

def diagnose_signature(func: Callable) -> dict[str, Any]:
    """诊断函数签名状态"""
    return {
        "name": func.__name__,
        "doc": func.__doc__,
        "annotations": str(func.__annotations__) if func.__annotations__ else {},
        "has_wrapped": hasattr(func, "__wrapped__"),
        "signature": str(inspect.signature(func)) if callable(func) else "N/A",
        "is_preserved": func.__name__ != "wrapper",
    }


def get_original(func: Callable) -> Callable:
    """获取原始函数（通过 __wrapped__ 链）"""
    while hasattr(func, "__wrapped__"):
        func = func.__wrapped__
    return func


def count_wrapper_depth(func: Callable) -> int:
    """计算装饰器嵌套深度"""
    depth = 0
    while hasattr(func, "__wrapped__"):
        depth += 1
        func = func.__wrapped__
    return depth


# ─────────────────────────────────────
# 7.6 异常栈被吞掉调试
# ─────────────────────────────────────

def diagnose_exception(func: Callable) -> dict[str, Any]:
    """捕获并分析异常栈"""
    try:
        func()
        return {"error": None, "frames": []}
    except Exception as e:
        tb = sys.exc_info()[2]
        frames = traceback.extract_tb(tb) if tb else []
        return {
            "error": str(e),
            "error_type": type(e).__name__,
            "frames": [
                {
                    "file": f.filename,
                    "line": f.lineno,
                    "func": f.name,
                    "code": f.line or "",
                }
                for f in frames
            ],
            "has_original_func": any(
                "process" in f.func or "demo" in f.func for f in frames
            ),
        }


def format_exception_chain(e: Exception) -> str:
    """格式化异常链（包括 __cause__）"""
    lines = []
    current = e
    while current:
        lines.append(f"{type(current).__name__}: {current}")
        if current.__cause__:
            lines.append("  caused by:")
            current = current.__cause__
        else:
            break
    return "\n".join(lines)


# ─────────────────────────────────────
# 7.7 循环变量陷阱现场排查
# ─────────────────────────────────────

def inspect_closure_trap(func: Callable) -> dict[str, Any]:
    """检查闭包陷阱"""
    code = func.__code__
    closure = func.__closure__

    freevars = list(code.co_freevars) if code.co_freevars else []
    contents = [cell.cell_contents for cell in closure] if closure else []

    trap_detected = False
    trap_value = None

    if len(contents) > 1:
        trap_detected = all(contents[i] == contents[0] for i in range(len(contents)))
        trap_value = contents[0] if trap_detected else None
    elif len(contents) == 1 and len(freevars) == 1:
        trap_detected = True
        trap_value = contents[0]

    return {
        "freevars": freevars,
        "contents": contents,
        "trap_detected": trap_detected,
        "trap_value": trap_value,
    }


def compare_closures(funcs: list[Callable]) -> dict[str, Any]:
    """比较多个函数的闭包状态"""
    results = []
    shared_values: list[Any] = []

    for func in funcs:
        info = inspect_closure_trap(func)
        results.append({
            "name": func.__name__,
            "freevars": info["freevars"],
            "contents": info["contents"],
        })
        if info["contents"]:
            shared_values.extend(info["contents"])

    has_trap = len(set(shared_values)) == 1 and len(shared_values) > 1

    return {
        "functions": results,
        "has_shared_trap": has_trap,
        "shared_value": shared_values[0] if has_trap and shared_values else None,
    }


# ─────────────────────────────────────
# 7.8 async await 遗漏排查
# ─────────────────────────────────────

def diagnose_async_decorator(func: Callable) -> dict[str, Any]:
    """诊断 async 装饰器问题"""
    is_async = inspect.iscoroutinefunction(func)
    is_callable = callable(func)

    if not is_callable:
        return {"is_callable": False, "issue": "不是可调用对象"}

    if not is_async:
        return {"is_async": False, "issue": "函数不是 async"}

    return {
        "is_async": True,
        "is_coroutinefunction": True,
        "check_hint": "调用后检查返回值是否为 coroutine",
    }


async def test_async_result(func: Callable, *args: Any, **kwargs: Any) -> dict[str, Any]:
    """测试 async 函数的返回值类型"""
    if not inspect.iscoroutinefunction(func):
        return {"error": "函数不是 async"}

    try:
        result = func(*args, **kwargs)

        if inspect.iscoroutine(result):
            actual_result = await result
            return {
                "first_call_type": "coroutine",
                "await_missing": False,
                "actual_result_type": type(actual_result).__name__,
                "actual_result": str(actual_result)[:100],
            }
        else:
            return {
                "first_call_type": type(result).__name__,
                "await_missing": False,
                "actual_result": str(result)[:100],
            }
    except Exception as e:
        return {"error": str(e)}


async def detect_await_missing(func: Callable) -> dict[str, Any]:
    """检测 async 装饰器是否遗漏 await"""
    if not inspect.iscoroutinefunction(func):
        return {"is_async": False}

    try:
        raw_result = func()
        if inspect.iscoroutine(raw_result):
            inner = raw_result
            while inspect.iscoroutine(inner):
                try:
                    inner = await inner
                except Exception:
                    break

            if inspect.iscoroutine(inner):
                return {
                    "is_async": True,
                    "await_missing": True,
                    "depth": "多层 coroutine",
                }
            else:
                return {
                    "is_async": True,
                    "await_missing": False,
                    "final_type": type(inner).__name__,
                }
        return {"is_async": True, "await_missing": False}
    except Exception as e:
        return {"is_async": True, "error": str(e)}


# ─────────────────────────────────────
# 综合诊断工具
# ─────────────────────────────────────

def full_diagnosis(func: Callable) -> dict[str, Any]:
    """对函数进行完整诊断"""
    diagnosis = {
        "signature": diagnose_signature(func),
        "closure": inspect_closure_trap(func),
        "async_info": diagnose_async_decorator(func),
        "wrapper_depth": count_wrapper_depth(func),
    }

    diagnosis["issues"] = []

    if not diagnosis["signature"]["is_preserved"]:
        diagnosis["issues"].append("签名未保留：缺少 @wraps")

    if diagnosis["closure"]["trap_detected"]:
        diagnosis["issues"].append(
            f"闭包陷阱：变量共享，值为 {diagnosis['closure']['trap_value']}"
        )

    if diagnosis["async_info"]["is_async"]:
        diagnosis["issues"].append("async 函数：请检查 await 遗漏")

    diagnosis["has_issues"] = len(diagnosis["issues"]) > 0

    return diagnosis


def batch_diagnosis(funcs: list[Callable]) -> list[dict[str, Any]]:
    """批量诊断多个函数"""
    return [full_diagnosis(func) for func in funcs]