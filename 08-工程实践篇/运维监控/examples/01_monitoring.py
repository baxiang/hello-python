# 运维监控示例

"""
运维监控示例
包含：日志记录、健康检查、性能监控
"""

import logging
import time
import json
from datetime import datetime
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from functools import wraps


# 1. 日志配置
def setup_logging(
    name: str = "app",
    level: int = logging.INFO,
    log_file: Optional[str] = None
) -> logging.Logger:
    """配置日志"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 文件处理器
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


logger = setup_logging("monitor")


# 2. 健康检查
@dataclass
class HealthStatus:
    """健康状态"""
    status: str = "healthy"
    checks: Dict[str, bool] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "checks": self.checks,
            "timestamp": self.timestamp
        }


class HealthChecker:
    """健康检查器"""
    
    def __init__(self):
        self._checks: Dict[str, Callable[[], bool]] = {}
    
    def register(self, name: str, check_func: Callable[[], bool]) -> None:
        """注册检查"""
        self._checks[name] = check_func
    
    def check(self) -> HealthStatus:
        """执行检查"""
        results = {}
        all_healthy = True
        
        for name, check_func in self._checks.items():
            try:
                results[name] = check_func()
                if not results[name]:
                    all_healthy = False
            except Exception as e:
                logger.error(f"健康检查失败: {name} - {e}")
                results[name] = False
                all_healthy = False
        
        return HealthStatus(
            status="healthy" if all_healthy else "unhealthy",
            checks=results
        )


# 3. 性能监控
@dataclass
class Metric:
    """指标"""
    name: str
    value: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    tags: Dict[str, str] = field(default_factory=dict)


class MetricsCollector:
    """指标收集器"""
    
    def __init__(self):
        self._metrics: list[Metric] = []
    
    def record(
        self,
        name: str,
        value: float,
        tags: Optional[Dict[str, str]] = None
    ) -> None:
        """记录指标"""
        self._metrics.append(Metric(
            name=name,
            value=value,
            tags=tags or {}
        ))
    
    def get_metrics(self) -> list[Dict[str, Any]]:
        """获取所有指标"""
        return [m.__dict__ for m in self._metrics]
    
    def clear(self) -> None:
        """清空指标"""
        self._metrics.clear()


# 4. 请求监控装饰器
def monitor_request(collector: MetricsCollector):
    """请求监控装饰器"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            try:
                result = func(*args, **kwargs)
                collector.record(
                    f"{func.__name__}.success",
                    1,
                    {"function": func.__name__}
                )
                return result
            except Exception as e:
                collector.record(
                    f"{func.__name__}.error",
                    1,
                    {"function": func.__name__, "error": type(e).__name__}
                )
                raise
            finally:
                duration = time.time() - start
                collector.record(
                    f"{func.__name__}.duration",
                    duration,
                    {"function": func.__name__}
                )
        return wrapper
    return decorator


# 5. 告警系统
class AlertManager:
    """告警管理器"""
    
    def __init__(self):
        self._alerts: list[Dict[str, Any]] = []
    
    def alert(
        self,
        level: str,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        """发送告警"""
        alert = {
            "level": level,
            "message": message,
            "details": details or {},
            "timestamp": datetime.now().isoformat()
        }
        self._alerts.append(alert)
        logger.warning(f"[{level.upper()}] {message}")
    
    def get_alerts(self, level: Optional[str] = None) -> list:
        """获取告警"""
        if level:
            return [a for a in self._alerts if a["level"] == level]
        return self._alerts.copy()


# 6. 系统监控
def get_system_info() -> Dict[str, Any]:
    """获取系统信息"""
    import platform
    import os
    
    return {
        "platform": platform.platform(),
        "python_version": platform.python_version(),
        "cpu_count": os.cpu_count(),
        "hostname": platform.node()
    }


if __name__ == "__main__":
    print("=" * 40)
    print("运维监控示例")
    print("=" * 40)
    
    # 日志
    print("\n【日志记录】")
    logger.info("应用启动")
    logger.warning("这是一个警告")
    logger.error("这是一个错误")
    
    # 健康检查
    print("\n【健康检查】")
    checker = HealthChecker()
    checker.register("database", lambda: True)
    checker.register("cache", lambda: False)
    
    status = checker.check()
    print(f"健康状态: {json.dumps(status.to_dict(), indent=2)}")
    
    # 指标收集
    print("\n【指标收集】")
    metrics = MetricsCollector()
    metrics.record("requests", 100)
    metrics.record("latency", 0.05)
    
    print(f"指标: {json.dumps(metrics.get_metrics(), indent=2)}")
    
    # 请求监控
    print("\n【请求监控】")
    
    @monitor_request(metrics)
    def process_data(data: list) -> int:
        return len(data)
    
    process_data([1, 2, 3, 4, 5])
    print(f"新增指标数: {len(metrics.get_metrics())}")
    
    # 告警
    print("\n【告警系统】")
    alerts = AlertManager()
    alerts.alert("warning", "内存使用率过高", {"usage": "85%"})
    alerts.alert("error", "数据库连接失败", {"host": "localhost"})
    
    print(f"告警数: {len(alerts.get_alerts())}")
    
    # 系统信息
    print("\n【系统信息】")
    print(json.dumps(get_system_info(), indent=2))