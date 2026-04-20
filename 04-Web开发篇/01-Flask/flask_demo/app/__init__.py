"""Flask CMS API应用"""

from flask import Flask
from app.extensions import db, jwt, migrate
from app.api import register_blueprints


def create_app(config_name: str = "development") -> Flask:
    """Flask应用工厂"""
    app = Flask(__name__, instance_relative_config=True)
    
    from app.config import config
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    
    register_blueprints(app)
    
    return app