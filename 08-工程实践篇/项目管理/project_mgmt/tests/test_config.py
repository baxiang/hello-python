"""配置测试"""

from app.core.config import Config, ConfigManager
from app.core.version import Version


def test_config():
    config = Config.from_env()
    assert config.app_name == "MyApp"
    assert config.debug is False


def test_config_manager():
    manager = ConfigManager()
    manager.load(Config())
    assert manager.get("app_name") == "MyApp"
    manager.set("app_name", "TestApp")
    assert manager.get("app_name") == "TestApp"


def test_version():
    v = Version.parse("1.2.3")
    assert str(v) == "1.2.3"
    assert str(v.bump_minor()) == "1.3.0"