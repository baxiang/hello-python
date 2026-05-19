"""健康检查API测试"""

from fastapi.testclient import TestClient


class TestHealthCheck:
    """健康检查测试"""

    def test_health_check(self, client: TestClient) -> None:
        """测试健康检查端点"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "Task Manager API"
