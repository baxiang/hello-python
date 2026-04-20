"""PluginInfo 测试 - 模块属性"""

import sys
from dataclasses import is_dataclass
from types import ModuleType

from app.core.plugin_info import ModuleInfo, PluginInfo


class TestModuleAttributes:
    """测试模块属性相关功能"""

    def test_get_module_info_returns_moduleinfo(self) -> None:
        """get_module_info 返回 ModuleInfo 实例"""
        info = PluginInfo.get_module_info(sys)
        assert isinstance(info, ModuleInfo)
        assert info.name == "sys"

    def test_get_module_info_has_required_fields(self) -> None:
        """ModuleInfo 包含必需字段"""
        import os

        info = PluginInfo.get_module_info(os)
        assert info.name == "os"
        assert info.file is not None or info.file == ""
        assert info.doc is not None or info.doc == ""

    def test_get_exports_returns_list(self) -> None:
        """get_exports 返回导出列表"""
        import json

        exports = PluginInfo.get_exports(json)
        assert isinstance(exports, list)
        assert len(exports) > 0

    def test_get_exports_respects_all(self) -> None:
        """get_exports 尊重 __all__ 定义"""
        import json

        exports = PluginInfo.get_exports(json)
        if hasattr(json, "__all__"):
            assert set(exports) == set(json.__all__)

    def test_get_doc_returns_string(self) -> None:
        """get_doc 返回文档字符串"""
        import os

        doc = PluginInfo.get_doc(os)
        assert isinstance(doc, str)

    def test_get_doc_returns_none_for_no_doc(self) -> None:
        """无文档字符串时返回 None 或空字符串"""
        mod = ModuleType("test_no_doc")
        doc = PluginInfo.get_doc(mod)
        assert doc is None or doc == ""

    def test_get_path_returns_string_or_none(self) -> None:
        """get_path 返回路径或 None"""
        import os

        path = PluginInfo.get_path(os)
        assert path is None or isinstance(path, str)

    def test_get_path_builtin_returns_none(self) -> None:
        """内置模块返回 None"""
        path = PluginInfo.get_path(sys)
        assert path is None

    def test_get_package_returns_string_or_none(self) -> None:
        """get_package 返回包名或 None"""
        import os

        package = PluginInfo.get_package(os)
        assert package is None or isinstance(package, str)

    def test_get_namespace_returns_dict(self) -> None:
        """get_namespace 返回命名空间字典"""
        import math

        ns = PluginInfo.get_namespace(math)
        assert isinstance(ns, dict)
        assert "sqrt" in ns
        assert "pi" in ns

    def test_is_loaded_returns_bool(self) -> None:
        """is_loaded 返回布尔值"""

        assert PluginInfo.is_loaded("os") is True
        assert PluginInfo.is_loaded("nonexistent_module_xyz") is False

    def test_is_loaded_cached_module(self) -> None:
        """已缓存模块返回 True"""

        assert PluginInfo.is_loaded("json") is True


class TestModuleInfoClass:
    """测试 ModuleInfo 数据类"""

    def test_moduleinfo_is_dataclass(self) -> None:
        """ModuleInfo 是 dataclass"""
        assert is_dataclass(ModuleInfo)

    def test_moduleinfo_repr(self) -> None:
        """ModuleInfo 有 repr 方法"""
        info = ModuleInfo(
            name="test",
            file="/path/to/test.py",
            doc="Test module",
            package="test_pkg",
        )
        repr_str = repr(info)
        assert "ModuleInfo" in repr_str
        assert "name='test'" in repr_str

    def test_plugininfo_list_loaded_modules(self) -> None:
        """list_loaded_modules 返回已加载模块列表"""
        modules = PluginInfo.list_loaded_modules()
        assert isinstance(modules, list)
        assert "sys" in modules
        assert len(modules) > 0

    def test_plugininfo_get_mode_main(self) -> None:
        """get_mode 返回 main 当 __name__ == '__main__'"""
        mod = ModuleType("__main__")
        assert PluginInfo.get_mode(mod) == "main"

    def test_plugininfo_get_mode_imported(self) -> None:
        """get_mode 返回 imported 当模块被导入"""
        mod = ModuleType("my_module")
        assert PluginInfo.get_mode(mod) == "imported"
