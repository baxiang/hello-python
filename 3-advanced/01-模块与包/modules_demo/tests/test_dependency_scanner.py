"""DependencyScanner 测试 - 依赖分析"""

from pathlib import Path

from app.core.dependency_scanner import DependencyScanner


class TestDependencyScanner:
    """测试 DependencyScanner 类"""

    def test_scan_file_imports_returns_list(self, tmp_path: Path) -> None:
        """scan_file_imports 返回导入列表"""
        test_file = tmp_path / "test.py"
        test_file.write_text("import os\nimport sys\n")

        imports = DependencyScanner.scan_file_imports(str(test_file))
        assert isinstance(imports, list)
        assert "os" in imports
        assert "sys" in imports

    def test_scan_file_imports_with_from(self, tmp_path: Path) -> None:
        """scan_file_imports 处理 from 导入"""
        test_file = tmp_path / "test.py"
        test_file.write_text("from os import path\nfrom sys import argv\n")

        imports = DependencyScanner.scan_file_imports(str(test_file))
        assert "os" in imports
        assert "sys" in imports

    def test_scan_file_imports_nonexistent_file_returns_empty(self) -> None:
        """scan_file_imports 不存在的文件返回空列表"""
        imports = DependencyScanner.scan_file_imports("/nonexistent/file.py")
        assert imports == []

    def test_scan_module_imports_returns_list(self) -> None:
        """scan_module_imports 返回模块导入列表"""
        import json

        imports = DependencyScanner.scan_module_imports(json)
        assert isinstance(imports, list)

    def test_scan_package_dependencies_returns_list(self, tmp_path: Path) -> None:
        """scan_package_dependencies 返回包依赖列表"""
        pkg_dir = tmp_path / "my_package"
        pkg_dir.mkdir()
        (pkg_dir / "__init__.py").write_text("import os\n")
        (pkg_dir / "mod.py").write_text("import sys\nimport json\n")

        deps = DependencyScanner.scan_package_dependencies(str(pkg_dir))
        assert isinstance(deps, list)
        assert "os" in deps
        assert "sys" in deps
        assert "json" in deps

    def test_get_import_graph_returns_dict(self, tmp_path: Path) -> None:
        """get_import_graph 返回导入图字典"""
        pkg_dir = tmp_path / "my_package"
        pkg_dir.mkdir()
        (pkg_dir / "__init__.py").write_text("from . import mod_a\n")
        (pkg_dir / "mod_a.py").write_text("import os\n")
        (pkg_dir / "mod_b.py").write_text("import sys\nfrom . import mod_a\n")

        graph = DependencyScanner.get_import_graph(str(pkg_dir))
        assert isinstance(graph, dict)
        assert "mod_a" in graph
        assert "mod_b" in graph

    def test_detect_circular_imports_returns_list(self, tmp_path: Path) -> None:
        """detect_circular_imports 检测循环导入"""
        pkg_dir = tmp_path / "circular_pkg"
        pkg_dir.mkdir()
        (pkg_dir / "__init__.py").write_text("")
        (pkg_dir / "a.py").write_text("from .b import func_b\n")
        (pkg_dir / "b.py").write_text("from .a import func_a\n")

        circular = DependencyScanner.detect_circular_imports(str(pkg_dir))
        assert isinstance(circular, list)

    def test_detect_circular_imports_no_cycles(self, tmp_path: Path) -> None:
        """detect_circular_imports 无循环时返回空列表"""
        pkg_dir = tmp_path / "no_cycle_pkg"
        pkg_dir.mkdir()
        (pkg_dir / "__init__.py").write_text("")
        (pkg_dir / "a.py").write_text("import os\n")
        (pkg_dir / "b.py").write_text("import sys\n")

        circular = DependencyScanner.detect_circular_imports(str(pkg_dir))
        assert circular == []

    def test_get_stdlib_modules_returns_list(self) -> None:
        """get_stdlib_modules 返回标准库模块列表"""
        stdlib = DependencyScanner.get_stdlib_modules()
        assert isinstance(stdlib, list)
        assert "os" in stdlib
        assert "sys" in stdlib

    def test_is_stdlib_returns_bool(self) -> None:
        """is_stdlib 判断是否为标准库"""
        assert DependencyScanner.is_stdlib("os") is True
        assert DependencyScanner.is_stdlib("sys") is True
        assert DependencyScanner.is_stdlib("nonexistent_xyz") is False

    def test_get_third_party_deps_returns_list(self, tmp_path: Path) -> None:
        """get_third_party_deps 返回第三方依赖"""
        test_file = tmp_path / "test.py"
        test_file.write_text("import os\nimport pytest\n")

        deps = DependencyScanner.get_third_party_deps(str(test_file))
        assert isinstance(deps, list)
        assert "os" not in deps
        assert "pytest" in deps

    def test_scan_file_imports_with_alias(self, tmp_path: Path) -> None:
        """scan_file_imports 处理别名导入"""
        test_file = tmp_path / "test.py"
        test_file.write_text("import os as operating_system\n")

        imports = DependencyScanner.scan_file_imports(str(test_file))
        assert "os" in imports

    def test_scan_file_imports_with_relative(self, tmp_path: Path) -> None:
        """scan_file_imports 处理相对导入"""
        test_file = tmp_path / "test.py"
        test_file.write_text("from . import sibling\nfrom .. import parent\n")

        imports = DependencyScanner.scan_file_imports(str(test_file))
        assert isinstance(imports, list)
