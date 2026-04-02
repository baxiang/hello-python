"""Flask 测试"""

from flask import Flask
from app.api.routes import api_bp


def create_app() -> Flask:
    """创建应用"""
    app = Flask(__name__)
    app.register_blueprint(api_bp)
    return app


def test_hello():
    app = create_app()
    client = app.test_client()
    response = client.get("/api/hello")
    assert response.status_code == 200
    assert b"Hello" in response.data