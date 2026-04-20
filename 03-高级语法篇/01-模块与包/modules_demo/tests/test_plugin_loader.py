"""PluginLoader 测试 - 核心插件加载器"""

from pathlib import Path
from types import ModuleType
from unittest.mock import MagicMock

import pytest

from app.core.plugin_loader import PluginLoader


class TestPluginLoader:
    """测试 PluginLoader 类"""

    def test_load_plugin_from_path_returns_module(self, tmp_path: Path) -> None:
        """load_plugin_from_path 从路径加载插件"""
        plugin_dir = tmp_path / "my_plugin"
        plugin_dir.mkdir()
        (plugin_dir / "__init__.py").write_text("PLUGIN_NAME = 'test'")

        loader = PluginLoader(str(tmp_path))
        plugin = loader.load_plugin_from_path(str(plugin_dir))
        assert plugin is not None

    def test_load_plugin_from_path_nonexistent_returns_none(self) -> None:
        """load_plugin_from_path 不存在路径返回 None"""
        loader = PluginLoader("/tmp")
        plugin = loader.load_plugin_from_path("/nonexistent/path")
        assert plugin is None

    def test_load_all_plugins_returns_dict(self, tmp_path: Path) -> None:
        """load_all_plugins 加载所有插件"""
        plugins_dir = tmp_path / "plugins"
        plugins_dir.mkdir()

        plugin_a = plugins_dir / "plugin_a"
        plugin_a.mkdir()
        (plugin_a / "__init__.py").write_text("PLUGIN_NAME = 'a'")

        plugin_b = plugins_dir / "plugin_b"
        plugin_b.mkdir()
        (plugin_b / "__init__.py").write_text("PLUGIN_NAME = 'b'")

        loader = PluginLoader(str(plugins_dir))
        plugins = loader.load_all_plugins()
        assert isinstance(plugins, dict)
        assert "plugin_a" in plugins
        assert "plugin_b" in plugins

    def test_discover_plugins_returns_list(self, tmp_path: Path) -> None:
        """discover_plugins 发现所有插件"""
        plugins_dir = tmp_path / "plugins"
        plugins_dir.mkdir()

        for name in ["plugin_a", "plugin_b"]:
            pkg = plugins_dir / name
            pkg.mkdir()
            (pkg / "__init__.py").write_text("")

        loader = PluginLoader(str(plugins_dir))
        discovered = loader.discover_plugins()
        assert isinstance(discovered, list)
        assert len(discovered) == 2

    def test_is_valid_plugin_returns_bool(self, tmp_path: Path) -> None:
        """is_valid_plugin 验证插件"""
        valid_plugin = tmp_path / "valid"
        valid_plugin.mkdir()
        (valid_plugin / "__init__.py").write_text("")

        loader = PluginLoader(str(tmp_path))
        assert loader.is_valid_plugin(str(valid_plugin)) is True
        assert loader.is_valid_plugin(str(tmp_path / "invalid")) is False

    def test_get_plugin_metadata_returns_dict(self, tmp_path: Path) -> None:
        """get_plugin_metadata 获取插件元数据"""
        plugin_dir = tmp_path / "meta_plugin"
        plugin_dir.mkdir()
        (plugin_dir / "__init__.py").write_text(
            """PLUGIN_NAME = 'meta'
PLUGIN_VERSION = '1.0.0'
PLUGIN_AUTHOR = 'test'
"""
        )

        loader = PluginLoader(str(tmp_path))
        metadata = loader.get_plugin_metadata(str(plugin_dir))
        assert isinstance(metadata, dict)
        assert metadata.get("PLUGIN_NAME") == "meta"

    def test_reload_plugin_returns_module(self, tmp_path: Path) -> None:
        """reload_plugin 重新加载插件"""
        plugin_dir = tmp_path / "reload_plugin"
        plugin_dir.mkdir()
        (plugin_dir / "__init__.py").write_text("VALUE = 1")

        loader = PluginLoader(str(tmp_path))
        plugin = loader.load_plugin_from_path(str(plugin_dir))
        assert plugin is not None

        (plugin_dir / "__init__.py").write_text("VALUE = 2")
        reloaded = loader.reload_plugin(str(plugin_dir))
        assert reloaded is not None

    def test_unregister_plugin_removes_from_cache(self, tmp_path: Path) -> None:
        """unregister_plugin 从缓存移除插件"""
        plugin_dir = tmp_path / "unreg_plugin"
        plugin_dir.mkdir()
        (plugin_dir / "__init__.py").write_text("")

        loader = PluginLoader(str(tmp_path))
        loader.load_plugin_from_path(str(plugin_dir))

        result = loader.unregister_plugin("unreg_plugin")
        assert isinstance(result, bool)

    def test_get_loaded_plugins_returns_list(self, tmp_path: Path) -> None:
        """get_loaded_plugins 返回已加载插件列表"""
        plugins_dir = tmp_path / "plugins"
        plugins_dir.mkdir()

        plugin_a = plugins_dir / "plugin_a"
        plugin_a.mkdir()
        (plugin_a / "__init__.py").write_text("")

        loader = PluginLoader(str(plugins_dir))
        loader.load_all_plugins()

        loaded = loader.get_loaded_plugins()
        assert isinstance(loaded, list)

    def test_plugin_loader_init_sets_base_path(self, tmp_path: Path) -> None:
        """PluginLoader 初始化设置基础路径"""
        loader = PluginLoader(str(tmp_path))
        assert loader.base_path == str(tmp_path)

    def test_load_plugin_by_name_returns_module(self, tmp_path: Path) -> None:
        """load_plugin_by_name 通过名称加载插件"""
        plugins_dir = tmp_path / "plugins"
        plugins_dir.mkdir()

        plugin = plugins_dir / "my_plugin"
        plugin.mkdir()
        (plugin / "__init__.py").write_text("PLUGIN_NAME = 'my_plugin'")

        loader = PluginLoader(str(plugins_dir))
        mod = loader.load_plugin_by_name("my_plugin")
        assert mod is not None

    def test_load_plugin_by_name_not_found_returns_none(self, tmp_path: Path) -> None:
        """load_plugin_by_name 找不到插件返回 None"""
        loader = PluginLoader(str(tmp_path))
        mod = loader.load_plugin_by_name("nonexistent")
        assert mod is None

    def test_filter_plugins_by_criteria_returns_list(self, tmp_path: Path) -> None:
        """filter_plugins_by_criteria 根据条件过滤插件"""
        plugins_dir = tmp_path / "plugins"
        plugins_dir.mkdir()

        for name in ["plugin_active", "plugin_inactive"]:
            pkg = plugins_dir / name
            pkg.mkdir()
            (pkg / "__init__.py").write_text(f"PLUGIN_NAME = '{name}'")

        loader = PluginLoader(str(plugins_dir))
        loader.load_all_plugins()

        filtered = loader.filter_plugins_by_criteria(lambda m: True)
        assert isinstance(filtered, list)

    def test_get_plugin_dependencies_returns_list(self, tmp_path: Path) -> None:
        """get_plugin_dependencies 获取插件依赖"""
        plugin_dir = tmp_path / "dep_plugin"
        plugin_dir.mkdir()
        (plugin_dir / "__init__.py").write_text("import os\nimport sys")

        loader = PluginLoader(str(tmp_path))
        deps = loader.get_plugin_dependencies(str(plugin_dir))
        assert isinstance(deps, list)
        assert "os" in deps

    def test_has_plugin_returns_bool(self, tmp_path: Path) -> None:
        """has_plugin 检查是否有插件"""
        plugins_dir = tmp_path / "plugins"
        plugins_dir.mkdir()

        plugin = plugins_dir / "existing"
        plugin.mkdir()
        (plugin / "__init__.py").write_text("")

        loader = PluginLoader(str(plugins_dir))
        loader.load_all_plugins()

        assert loader.has_plugin("existing") is True
        assert loader.has_plugin("nonexistent") is False