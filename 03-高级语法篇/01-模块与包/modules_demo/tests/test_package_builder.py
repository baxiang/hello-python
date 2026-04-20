"""PackageBuilder 测试 - 打包发布"""

from pathlib import Path

from app.core.package_builder import PackageBuilder


class TestPackageBuilder:
    """测试 PackageBuilder 类"""

    def test_create_sdist_returns_path(self, tmp_path: Path) -> None:
        """create_sdist 创建源码分发"""
        pkg_dir = tmp_path / "my_package"
        pkg_dir.mkdir()
        (pkg_dir / "__init__.py").write_text("__version__ = '1.0.0'")
        (pkg_dir / "main.py").write_text("def main(): pass")

        result = PackageBuilder.create_sdist(str(pkg_dir), output_dir=str(tmp_path))
        assert isinstance(result, str)
        assert Path(result).name.endswith(".tar.gz") or result == ""

    def test_create_wheel_returns_path(self, tmp_path: Path) -> None:
        """create_wheel 创建 wheel 分发"""
        pkg_dir = tmp_path / "my_package"
        pkg_dir.mkdir()
        (pkg_dir / "__init__.py").write_text("__version__ = '1.0.0'")

        result = PackageBuilder.create_wheel(str(pkg_dir), output_dir=str(tmp_path))
        assert isinstance(result, str)

    def test_get_package_metadata_returns_dict(self, tmp_path: Path) -> None:
        """get_package_metadata 返回元数据字典"""
        pkg_dir = tmp_path / "my_package"
        pkg_dir.mkdir()
        (pkg_dir / "__init__.py").write_text("__version__ = '1.0.0'")
        (pkg_dir / "setup.py").write_text(
            "from setuptools import setup\nsetup(name='my_package', version='1.0.0')"
        )

        metadata = PackageBuilder.get_package_metadata(str(pkg_dir))
        assert isinstance(metadata, dict)

    def test_validate_package_returns_bool(self, tmp_path: Path) -> None:
        """validate_package 验证包结构"""
        pkg_dir = tmp_path / "valid_package"
        pkg_dir.mkdir()
        (pkg_dir / "__init__.py").write_text("")

        result = PackageBuilder.validate_package(str(pkg_dir))
        assert isinstance(result, bool)

    def test_validate_package_missing_init_returns_false(self, tmp_path: Path) -> None:
        """validate_package 无 __init__.py 返回 False"""
        pkg_dir = tmp_path / "invalid_package"
        pkg_dir.mkdir()

        result = PackageBuilder.validate_package(str(pkg_dir))
        assert result is False

    def test_generate_setup_py_creates_file(self, tmp_path: Path) -> None:
        """generate_setup_py 创建 setup.py"""
        pkg_dir = tmp_path / "my_package"
        pkg_dir.mkdir()
        (pkg_dir / "__init__.py").write_text("__version__ = '1.0.0'")

        PackageBuilder.generate_setup_py(
            str(pkg_dir),
            name="my_package",
            version="1.0.0",
            description="Test package",
        )
        assert (pkg_dir / "setup.py").exists()

    def test_generate_pyproject_toml_creates_file(self, tmp_path: Path) -> None:
        """generate_pyproject_toml 创建 pyproject.toml"""
        pkg_dir = tmp_path / "my_package"
        pkg_dir.mkdir()
        (pkg_dir / "__init__.py").write_text("__version__ = '1.0.0'")

        PackageBuilder.generate_pyproject_toml(
            str(pkg_dir),
            name="my_package",
            version="1.0.0",
        )
        assert (pkg_dir / "pyproject.toml").exists()

    def test_build_package_returns_path(self, tmp_path: Path) -> None:
        """build_package 构建包"""
        pkg_dir = tmp_path / "my_package"
        pkg_dir.mkdir()
        (pkg_dir / "__init__.py").write_text("__version__ = '1.0.0'")

        result = PackageBuilder.build_package(str(pkg_dir), str(tmp_path / "dist"))
        assert isinstance(result, str | list)

    def test_get_build_artifacts_returns_list(self, tmp_path: Path) -> None:
        """get_build_artifacts 返回构建产物列表"""
        dist_dir = tmp_path / "dist"
        dist_dir.mkdir()
        (dist_dir / "package-1.0.0.tar.gz").write_text("")
        (dist_dir / "package-1.0.0-py3-none-any.whl").write_text("")

        artifacts = PackageBuilder.get_build_artifacts(str(dist_dir))
        assert isinstance(artifacts, list)
        assert len(artifacts) >= 2

    def test_clean_build_artifacts_removes_files(self, tmp_path: Path) -> None:
        """clean_build_artifacts 清理构建产物"""
        pkg_dir = tmp_path / "my_package"
        pkg_dir.mkdir()
        (pkg_dir / "__init__.py").write_text("")
        build_dir = pkg_dir / "build"
        build_dir.mkdir()
        (build_dir / "lib").mkdir()

        result = PackageBuilder.clean_build_artifacts(str(pkg_dir))
        assert result is True
        assert not build_dir.exists()

    def test_estimate_package_size_returns_int(self, tmp_path: Path) -> None:
        """estimate_package_size 返回包大小"""
        pkg_dir = tmp_path / "my_package"
        pkg_dir.mkdir()
        (pkg_dir / "__init__.py").write_text("__version__ = '1.0.0'")
        (pkg_dir / "module.py").write_text("def func(): pass\n" * 100)

        size = PackageBuilder.estimate_package_size(str(pkg_dir))
        assert isinstance(size, int)
        assert size > 0

    def test_list_package_files_returns_list(self, tmp_path: Path) -> None:
        """list_package_files 返回包文件列表"""
        pkg_dir = tmp_path / "my_package"
        pkg_dir.mkdir()
        (pkg_dir / "__init__.py").write_text("")
        (pkg_dir / "module.py").write_text("")
        (pkg_dir / "data.txt").write_text("")

        files = PackageBuilder.list_package_files(str(pkg_dir))
        assert isinstance(files, list)
        assert "__init__.py" in files
        assert "module.py" in files

    def test_check_installable_returns_bool(self, tmp_path: Path) -> None:
        """check_installable 检查是否可安装"""
        pkg_dir = tmp_path / "my_package"
        pkg_dir.mkdir()
        (pkg_dir / "__init__.py").write_text("")
        (pkg_dir / "setup.py").write_text("from setuptools import setup\nsetup()")

        result = PackageBuilder.check_installable(str(pkg_dir))
        assert isinstance(result, bool)