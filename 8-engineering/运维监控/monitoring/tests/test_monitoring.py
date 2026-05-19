"""监控测试"""

from app.core.metrics import MetricsCollector, HealthChecker


def test_metrics_collector():
    collector = MetricsCollector()
    collector.record("requests", 100)
    collector.record("latency", 0.05)
    
    metrics = collector.get_metrics()
    assert len(metrics) == 2
    assert metrics[0]["name"] == "requests"


def test_health_checker():
    checker = HealthChecker()
    checker.register("database", lambda: True)
    checker.register("cache", lambda: False)
    
    result = checker.check()
    assert result["status"] == "unhealthy"
    assert result["checks"]["database"] is True