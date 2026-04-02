"""指标"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional


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
    
    def record(self, name: str, value: float, tags: Optional[Dict[str, str]] = None) -> None:
        """记录指标"""
        self._metrics.append(Metric(name=name, value=value, tags=tags or {}))
    
    def get_metrics(self) -> list[Dict[str, Any]]:
        """获取所有指标"""
        return [m.__dict__ for m in self._metrics]
    
    def clear(self) -> None:
        """清空指标"""
        self._metrics.clear()


class HealthChecker:
    """健康检查器"""
    
    def __init__(self):
        self._checks: Dict[str, callable] = {}
    
    def register(self, name: str, check_func: callable) -> None:
        """注册检查"""
        self._checks[name] = check_func
    
    def check(self) -> Dict[str, Any]:
        """执行检查"""
        results = {}
        all_healthy = True
        
        for name, check_func in self._checks.items():
            try:
                results[name] = check_func()
                if not results[name]:
                    all_healthy = False
            except Exception:
                results[name] = False
                all_healthy = False
        
        return {
            "status": "healthy" if all_healthy else "unhealthy",
            "checks": results,
            "timestamp": datetime.now().isoformat()
        }