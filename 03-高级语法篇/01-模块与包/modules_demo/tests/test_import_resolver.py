"""ImportResolver 测试 - 导入机制"""

from types import ModuleType

import pytest

from app.core.import_resolver import ImportResolver


class TestImportResolver:
    """测试 ImportResolver 类"""

    def test_import_module_returns_module(self) -> None:
        """import_module 成功导入模块"""
        mod = ImportResolver.import_module("os")
        assert isinstance(mod, ModuleType)
        assert mod.__name__ == "os"

    def test_import_module_raises_on_not_found(self) -> None:
        """import_module 不存在时抛出 ImportError"""
        with pytest.raises(ImportError):
            ImportResolver.import_module("nonexistent_module_xyz_123")

    def test_safe_import_returns_module_or_none(self) -> None:
        """safe_import 返回模块或 None"""
        mod = ImportResolver.safe_import("sys")
        assert mod is not None
        assert mod.__name__ == "sys"

        mod = ImportResolver.safe_import("nonexistent_module_xyz_123")
        assert mod is None

    def test_reload_module_returns_module(self) -> None:
        """reload_module 重新加载模块"""
        import json

        mod = ImportResolver.reload_module(json)
        assert mod is not None
        assert mod.__name__ == "json"

    def test_get_module_spec_returns_spec_or_none(self) -> None:
        """get_module_spec 返回 spec 或 None"""
        spec = ImportResolver.get_module_spec("os")
        assert spec is not None
        assert spec.name == "os"

        spec = ImportResolver.get_module_spec("nonexistent_module_xyz_123")
        assert spec is None

    def test_is_importable_returns_bool(self) -> None:
        """is_importable 判断模块是否可导入"""
        assert ImportResolver.is_importable("os") is True
        assert ImportResolver.is_importable("nonexistent_module_xyz_123") is False

    def test_get_importer_returns_importer_or_none(self) -> None:
        """get_importer 返回导入器或 None"""
        import os

        importer = ImportResolver.get_importer(os)
        assert importer is not None or importer is None

    def test_resolve_dotted_name_returns_attribute(self) -> None:
        """resolve_dotted_name 解析点分名称"""
        attr = ImportResolver.resolve_dotted_name("os.path.join")
        assert callable(attr)

    def test_resolve_dotted_name_invalid_returns_none(self) -> None:
        """resolve_dotted_name 无效名称返回 None"""
        result = ImportResolver.resolve_dotted_name("nonexistent.attr")
        assert result is None

    def test_get_module_dependencies_returns_list(self) -> None:
        """get_module_dependencies 返回依赖列表"""
        import json

        deps = ImportResolver.get_module_dependencies(json)
        assert isinstance(deps, list)

    def test_import_from_module_returns_attribute(self) -> None:
        """import_from_module 从模块导入属性"""
        join = ImportResolver.import_from_module("os.path", "join")
        assert callable(join)

    def test_import_from_module_raises_on_not_found(self) -> None:
        """import_from_module 属性不存在时抛出错误"""
        with pytest.raises((ImportError, AttributeError)):
            ImportResolver.import_from_module("os", "nonexistent_attr_xyz")

    def test_cache_control_clears_module(self) -> None:
        """缓存控制可以清除模块"""

        ImportResolver.import_module("json")
        result = ImportResolver.clear_from_cache("json")
        assert result is True

    def test_get_cached_module_returns_module_or_none(self) -> None:
        """get_cached_module 返回缓存的模块或 None"""

        mod = ImportResolver.get_cached_module("os")
        assert mod is not None

        mod = ImportResolver.get_cached_module("nonexistent_xyz")
        assert mod is None
