"""pytest配置"""

import pytest

from app import create_app
from app.extensions import db


@pytest.fixture
def app():
    """测试应用"""
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """测试客户端"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """CLI测试runner"""
    return app.test_cli_runner()
