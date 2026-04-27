"""pytest 配置 — 提供 FastAPI TestClient fixture"""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    """提供测试用 HTTP 客户端"""
    return TestClient(app)
