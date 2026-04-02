"""FastAPI 测试"""

from fastapi.testclient import TestClient
from fastapi import FastAPI
from app.api.routes import router


def create_app() -> FastAPI:
    """创建应用"""
    app = FastAPI()
    app.include_router(router, prefix="/api")
    return app


def test_hello():
    app = create_app()
    client = TestClient(app)
    response = client.get("/api/hello")
    assert response.status_code == 200
    assert "Hello" in response.json()["message"]