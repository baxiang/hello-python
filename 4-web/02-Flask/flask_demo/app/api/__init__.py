"""API蓝图注册"""

from flask import Flask
from app.api.auth import auth_bp
from app.api.users import users_bp
from app.api.articles import articles_bp
from app.api.files import files_bp


def register_blueprints(app: Flask) -> None:
    """注册所有蓝图"""
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(articles_bp, url_prefix="/api/articles")
    app.register_blueprint(files_bp, url_prefix="/api/files")