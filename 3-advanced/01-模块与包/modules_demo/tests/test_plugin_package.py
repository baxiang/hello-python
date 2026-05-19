"""PluginPackage 测试 - 包结构处理"""

from pathlib import Path

from app.core.plugin_package import PluginPackage


class TestPluginPackage:
    """测试 PluginPackage 类"""

    def test_is_package_returns_bool(self, tmp_path: Path) -> None:
        """is_package 判断是否为包"""
        pkg_dir = tmp_path / "my_package"
        pkg_dir.mkdir()
        (pkg_dir / "__init__.py").write_text("")

        assert PluginPackage.is_package(str(pkg_dir)) is True
        assert PluginPackage.is_package(str(tmp_path / "nonexistent")) is False

    def test_is_package_with_py_file_returns_false(self, tmp_path: Path) -> None:
        """is_package 对普通 .py 文件返回 False"""
        py_file = tmp_path / "module.py"
        py_file.write_text("")

        assert PluginPackage.is_package(str(py_file)) is False

    def test_get_package_info_returns_dict(self, tmp_path: Path) -> None:
        """get_package_info 返回包信息字典"""
        pkg_dir = tmp_path / "my_package"
        pkg_dir.mkdir()
        (pkg_dir / "__init__.py").write_text('"""My package docstring"""')

        info = PluginPackage.get_package_info(str(pkg_dir))
        assert isinstance(info, dict)
        assert "name" in info
        assert "path" in info
        assert info["name"] == "my_package"

    def test_list_modules_returns_list(self, tmp_path: Path) -> None:
        """list_modules 列出包中的模块"""
        pkg_dir = tmp_path / "my_package"
        pkg_dir.mkdir()
        (pkg_dir / "__init__.py").write_text("")
        (pkg_dir / "module_a.py").write_text("")
        (pkg_dir / "module_b.py").write_text("")
        (pkg_dir / "_private.py").write_text("")

        modules = PluginPackage.list_modules(str(pkg_dir))
        assert isinstance(modules, list)
        assert "module_a" in modules
        assert "module_b" in modules
        assert "_private" not in modules

    def test_list_modules_includes_subpackages(self, tmp_path: Path) -> None:
        """list_modules 包含子包"""
        pkg_dir = tmp_path / "my_package"
        pkg_dir.mkdir()
        (pkg_dir / "__init__.py").write_text("")
        sub_pkg = pkg_dir / "subpkg"
        sub_pkg.mkdir()
        (sub_pkg / "__init__.py").write_text("")

        modules = PluginPackage.list_modules(str(pkg_dir))
        assert "subpkg" in modules

    def test_create_package_creates_structure(self, tmp_path: Path) -> None:
        """create_package 创建包目录结构"""
        pkg_path = tmp_path / "new_package"

        result = PluginPackage.create_package(str(pkg_path))
        assert result is True
        assert pkg_path.exists()
        assert (pkg_path / "__init__.py").exists()

    def test_create_package_with_docstring(self, tmp_path: Path) -> None:
        """create_package 创建带文档字符串的包"""
        pkg_path = tmp_path / "new_package"

        PluginPackage.create_package(str(pkg_path), docstring="My Package")
        init_content = (pkg_path / "__init__.py").read_text()
        assert "My Package" in init_content

    def test_is_namespace_package_returns_bool(self, tmp_path: Path) -> None:
        """is_namespace_package 判断命名空间包"""
        pkg_dir = tmp_path / "namespace_pkg"
        pkg_dir.mkdir()

        assert PluginPackage.is_namespace_package(str(pkg_dir)) is True

        (pkg_dir / "__init__.py").write_text("")
        assert PluginPackage.is_namespace_package(str(pkg_dir)) is False

    def test_get_package_version_returns_string_or_none(self, tmp_path: Path) -> None:
        """get_package_version 返回版本字符串或 None"""
        pkg_dir = tmp_path / "my_package"
        pkg_dir.mkdir()
        (pkg_dir / "__init__.py").write_text("__version__ = '1.0.0'")

        version = PluginPackage.get_package_version(str(pkg_dir))
        assert version == "1.0.0"

    def test_get_package_version_no_version_returns_none(self, tmp_path: Path) -> None:
        """get_package_version 无版本时返回 None"""
        pkg_dir = tmp_path / "my_package"
        pkg_dir.mkdir()
        (pkg_dir / "__init__.py").write_text("")

        version = PluginPackage.get_package_version(str(pkg_dir))
        assert version is None

    def test_from_module_returns_pluginpackage(self) -> None:
        """from_module 从模块对象创建 PluginPackage"""
        import os

        pkg = PluginPackage.from_module(os)
        assert isinstance(pkg, PluginPackage)

    def test_package_name_property(self, tmp_path: Path) -> None:
        """name 属性返回包名"""
        pkg_dir = tmp_path / "my_package"
        pkg_dir.mkdir()
        (pkg_dir / "__init__.py").write_text("")

        pkg = PluginPackage(str(pkg_dir))
        assert pkg.name == "my_package"

    def test_package_path_property(self, tmp_path: Path) -> None:
        """path 属性返回包路径"""
        pkg_dir = tmp_path / "my_package"
        pkg_dir.mkdir()
        (pkg_dir / "__init__.py").write_text("")

        pkg = PluginPackage(str(pkg_dir))
        assert pkg.path == str(pkg_dir)

    def test_package_modules_property(self, tmp_path: Path) -> None:
        """modules 属性返回模块列表"""
        pkg_dir = tmp_path / "my_package"
        pkg_dir.mkdir()
        (pkg_dir / "__init__.py").write_text("")
        (pkg_dir / "mod.py").write_text("")

        pkg = PluginPackage(str(pkg_dir))
        assert "mod" in pkg.modules
