"""第 7 章 Part D — 生产环境调试实战

提供生产级调试工具：
- 日志分析（wrapper 问题排查）
- 性能追踪（PerformanceTracker）
- 错误定位（locate_error_in_chain）
- 命名装饰器（named_decorator）
- 组合装饰器（combined_decorator）
"""

from __future__ import annotations

import functools
import logging
import time
import traceback
from collections.abc import Callable
from typing import Any, ParamSpec, TypeVar

P = ParamSpec("P")
T = TypeVar("T")


# ─────────────────────────────────────
# 7.11 日志追踪问题
# ─────────────────────────────────────

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
log = logging.getLogger(__name__)


def log_call_wrong(func: Callable[P, T]) -> Callable[..., Any]:
    """❌ 硬编码 wrapper 名字的装饰器"""
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        log.info(f"Calling wrapper with args={args}")
        try:
            result = func(*args, **kwargs)
            log.info(f"wrapper returned")
            return result
        except Exception as e:
            log.error(f"wrapper failed: {e}")
            raise
    return wrapper


def log_call_fixed(func: Callable[P, T]) -> Callable[P, T]:
    """✅ 使用 func.__name__ 记录真实函数名"""
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        func_name = func.__name__
        log.info(f"Calling {func_name} with args={args}")
        try:
            result = func(*args, **kwargs)
            log.info(f"{func_name} returned")
            return result
        except Exception as e:
            log.error(f"{func_name} failed: {e}")
            raise
    return wrapper


def production_log(
    level: str = "INFO",
    include_args: bool = True,
    include_result: bool = False,
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """生产级日志装饰器工厂"""
    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            func_name = func.__name__
            log_func = getattr(logging, level.lower())
            
            if include_args:
                log_func(f"[{func_name}] 调用: args={args}, kwargs={kwargs}")
            else:
                log_func(f"[{func_name}] 调用")
            
            try:
                result = func(*args, **kwargs)
                
                if include_result:
                    log_func(f"[{func_name}] 返回: {result}")
                else:
                    log_func(f"[{func_name}] 完成")
                
                return result
                
            except Exception as e:
                logging.error(f"[{func_name}] 异常: {type(e).__name__}: {e}")
                raise
        
        wrapper._log_config = {
            "level": level,
            "include_args": include_args,
            "include_result": include_result,
        }
        
        return wrapper
    return decorator


def analyze_logs(log_entries: list[str]) -> dict[str, Any]:
    """分析日志条目，统计 wrapper 问题"""
    wrapper_calls = sum(1 for entry in log_entries if "wrapper" in entry)
    named_calls = sum(1 for entry in log_entries if "Calling " in entry and "wrapper" not in entry)
    
    return {
        "wrapper_calls": wrapper_calls,
        "named_calls": named_calls,
        "has_problem": wrapper_calls > named_calls,
        "recommendation": "检查装饰器是否使用 func.__name__ 而非硬编码 'wrapper'",
    }


# ─────────────────────────────────────
# 7.12 性能瓶颈追踪
# ─────────────────────────────────────

class PerformanceTracker:
    """性能追踪器 — 记录每个函数的耗时分布"""
    
    def __init__(self) -> None:
        self._stats: dict[str, list[float]] = {}
    
    def track(self, func_name: str, elapsed: float) -> None:
        if func_name not in self._stats:
            self._stats[func_name] = []
        self._stats[func_name].append(elapsed)
    
    def get_report(self) -> dict[str, dict[str, float]]:
        report = {}
        for func_name, times in self._stats.items():
            if times:
                report[func_name] = {
                    "count": len(times),
                    "total": sum(times),
                    "avg": sum(times) / len(times),
                    "max": max(times),
                    "min": min(times),
                }
        return report
    
    def get_slowest(self, threshold: float = 0.1) -> list[tuple[str, float]]:
        """获取超过阈值的慢调用"""
        slow = []
        for func_name, times in self._stats.items():
            for t in times:
                if t > threshold:
                    slow.append((func_name, t))
        return sorted(slow, key=lambda x: x[1], reverse=True)
    
    def clear(self) -> None:
        """清空统计数据"""
        self._stats.clear()


tracker = PerformanceTracker()


def track_performance(func: Callable[P, T]) -> Callable[P, T]:
    """性能追踪装饰器"""
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        tracker.track(func.__name__, elapsed)
        wrapper._last_elapsed = elapsed
        return result
    wrapper._last_elapsed = 0.0
    return wrapper


def diagnose_performance(func: Callable, call_count: int = 100) -> dict[str, Any]:
    """诊断函数性能"""
    times = []
    for _ in range(call_count):
        start = time.perf_counter()
        func()
        times.append(time.perf_counter() - start)
    
    return {
        "func_name": func.__name__,
        "call_count": call_count,
        "avg_ms": sum(times) / len(times) * 1000,
        "max_ms": max(times) * 1000,
        "min_ms": min(times) * 1000,
        "variance_ms": (max(times) - min(times)) * 1000,
    }


# ─────────────────────────────────────
# 7.13 复杂装饰器链错误定位
# ─────────────────────────────────────

def named_decorator(name: str) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """命名装饰器工厂 — 为调试添加标识"""
    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            return func(*args, **kwargs)
        wrapper.__decorator_name__ = name
        return wrapper
    return decorator


def locate_error_in_chain(func: Callable, *args: Any, **kwargs: Any) -> dict[str, Any]:
    """定位装饰器链中的错误位置"""
    try:
        result = func(*args, **kwargs)
        return {"success": True, "result": result}
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        
        layers: list[dict[str, Any]] = []
        original_func_line: dict[str, Any] | None = None
        
        for frame in tb:
            func_name = frame.name
            if func_name == "wrapper":
                decorator_name = _identify_decorator(func, frame.lineno)
                layers.append({
                    "type": "decorator",
                    "name": decorator_name or "unknown_decorator",
                    "file": frame.filename,
                    "line": frame.lineno,
                })
            else:
                original_func_line = {
                    "type": "original",
                    "name": func_name,
                    "file": frame.filename,
                    "line": frame.lineno,
                    "code": frame.line or "",
                }
                layers.append(original_func_line)
        
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
            "decorator_layers": layers[:-1] if original_func_line else layers,
            "original_location": original_func_line,
        }


def _identify_decorator(func: Callable, line_no: int) -> str | None:
    """通过 __wrapped__ 链识别装饰器"""
    current = func
    while hasattr(current, "__wrapped__"):
        code = current.__code__
        if hasattr(current, "__decorator_name__"):
            return current.__decorator_name__
        if code.co_firstlineno <= line_no <= code.co_firstlineno + 20:
            return getattr(current, "__decorator_name__", current.__name__)
        current = current.__wrapped__
    return None


def get_decorator_chain(func: Callable) -> list[str]:
    """获取装饰器链名称列表"""
    chain = []
    current = func
    while hasattr(current, "__wrapped__"):
        name = getattr(current, "__decorator_name__", "unknown")
        chain.append(name)
        current = current.__wrapped__
    chain.append(current.__name__)
    return chain


# ─────────────────────────────────────
# 组合装饰器（简化复杂链）
# ─────────────────────────────────────

def combined_decorator(
    log_calls: bool = True,
    track_performance: bool = True,
    retry_count: int = 0,
) -> Callable[[Callable[P, T]], Callable[P, T]]:
    """组合装饰器 — 减少嵌套层数"""
    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            func_name = func.__name__
            
            if log_calls:
                log.info(f"[{func_name}] 调用")
            
            attempts = retry_count + 1
            last_error = None
            
            for attempt in range(attempts):
                try:
                    if track_performance:
                        start = time.perf_counter()
                    
                    result = func(*args, **kwargs)
                    
                    if track_performance:
                        elapsed = time.perf_counter() - start
                        wrapper._last_elapsed = elapsed
                    
                    if log_calls:
                        log.info(f"[{func_name}] 完成")
                    
                    return result
                    
                except Exception as e:
                    last_error = e
                    if attempt < attempts - 1:
                        log.warning(f"[{func_name}] 重试 {attempt + 1}/{attempts}")
                        time.sleep(0.01)
            
            if last_error:
                log.error(f"[{func_name}] 最终失败: {last_error}")
                raise last_error
            
            wrapper._last_elapsed = 0.0
            wrapper.__decorator_name__ = "combined"
            return wrapper
        
        wrapper._config = {
            "log_calls": log_calls,
            "track_performance": track_performance,
            "retry_count": retry_count,
        }
        wrapper.__decorator_name__ = "combined"
        return wrapper
    return decorator


# ─────────────────────────────────────
# 辅助函数
# ─────────────────────────────────────

def demo_service_func(data: str) -> str:
    """演示服务函数"""
    if data == "error":
        raise ValueError("数据处理失败")
    return f"processed: {data}"


def demo_slow_func() -> str:
    """演示慢函数"""
    time.sleep(0.01)
    return "done"


def demo_fast_func() -> str:
    """演示快函数"""
    return "done"