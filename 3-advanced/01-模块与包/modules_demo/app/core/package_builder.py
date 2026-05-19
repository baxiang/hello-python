"""打包发布工具"""

import shutil
import subprocess
from pathlib import Path


class PackageBuilder:
    """打包发布工具类"""

    @staticmethod
    def create_sdist(package_path: str, output_dir: str | None = None) -> str:
        """创建源码分发包

        Args:
            package_path: 包目录路径
            output_dir: 输出目录，默认为 package_path/dist

        Returns:
            创建的 sdist 文件路径，失败返回空字符串
        """
        p = Path(package_path)
        if not p.is_dir():
            return ""

        try:
            result = subprocess.run(
                ["python", "-m", "build", "--sdist", str(p)],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                for artifact in (p / "dist").iterdir():
                    if artifact.name.endswith(".tar.gz"):
                        return str(artifact)
            return ""
        except Exception:
            return ""

    @staticmethod
    def create_wheel(package_path: str, output_dir: str | None = None) -> str:
        """创建 wheel 分发包

        Args:
            package_path: 包目录路径
            output_dir: 输出目录

        Returns:
            创建的 wheel 文件路径
        """
        p = Path(package_path)
        if not p.is_dir():
            return ""

        try:
            result = subprocess.run(
                ["python", "-m", "build", "--wheel", str(p)],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                for artifact in (p / "dist").iterdir():
                    if artifact.name.endswith(".whl"):
                        return str(artifact)
            return ""
        except Exception:
            return ""

    @staticmethod
    def get_package_metadata(package_path: str) -> dict[str, str | None]:
        """获取包的元数据

        Args:
            package_path: 包目录路径

        Returns:
            元数据字典
        """
        p = Path(package_path)
        metadata: dict[str, str | None] = {
            "name": p.name,
            "version": None,
            "description": None,
            "author": None,
        }

        init_file = p / "__init__.py"
        if init_file.exists():
            content = init_file.read_text()
            for line in content.splitlines():
                if line.strip().startswith("__version__"):
                    parts = line.split("=")
                    if len(parts) >= 2:
                        metadata["version"] = parts[1].strip().strip("'\"")

        setup_py = p / "setup.py"
        if setup_py.exists():
            content = setup_py.read_text()
            if "name=" in content:
                start = content.find("name=")
                end = content.find(",", start)
                if end == -1:
                    end = content.find(")", start)
                name_val = content[start:end].split("=")[1].strip().strip("'\"")
                metadata["name"] = name_val

        pyproject = p / "pyproject.toml"
        if pyproject.exists():
            content = pyproject.read_text()
            for line in content.splitlines():
                if line.startswith("version"):
                    metadata["version"] = line.split("=")[1].strip().strip("'\"")
                if line.startswith("name"):
                    metadata["name"] = line.split("=")[1].strip().strip("'\"")

        return metadata

    @staticmethod
    def validate_package(package_path: str) -> bool:
        """验证包结构是否正确

        Args:
            package_path: 包目录路径

        Returns:
            True 如果包结构有效
        """
        p = Path(package_path)
        return p.is_dir() and (p / "__init__.py").exists()

    @staticmethod
    def generate_setup_py(
        package_path: str,
        name: str,
        version: str,
        description: str = "",
        author: str = "",
    ) -> bool:
        """生成 setup.py 文件

        Args:
            package_path: 包目录路径
            name: 包名
            version: 版本号
            description: 描述
            author: 作者

        Returns:
            True 如果成功创建
        """
        p = Path(package_path)
        setup_content = f'''from setuptools import setup, find_packages

setup(
    name="{name}",
    version="{version}",
    description="{description}",
    author="{author}",
    packages=find_packages(),
)
'''
        try:
            (p / "setup.py").write_text(setup_content)
            return True
        except Exception:
            return False

    @staticmethod
    def generate_pyproject_toml(
        package_path: str,
        name: str,
        version: str,
        description: str = "",
    ) -> bool:
        """生成 pyproject.toml 文件

        Args:
            package_path: 包目录路径
            name: 包名
            version: 版本号
            description: 描述

        Returns:
            True 如果成功创建
        """
        p = Path(package_path)
        content = f'''[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "{name}"
version = "{version}"
description = "{description}"
'''
        try:
            (p / "pyproject.toml").write_text(content)
            return True
        except Exception:
            return False

    @staticmethod
    def build_package(package_path: str, output_dir: str) -> str | list[str]:
        """构建包（sdist + wheel）

        Args:
            package_path: 包目录路径
            output_dir: 输出目录

        Returns:
            构建产物路径列表
        """
        sdist = PackageBuilder.create_sdist(package_path, output_dir)
        wheel = PackageBuilder.create_wheel(package_path, output_dir)

        artifacts = []
        if sdist:
            artifacts.append(sdist)
        if wheel:
            artifacts.append(wheel)

        return artifacts

    @staticmethod
    def get_build_artifacts(dist_dir: str) -> list[str]:
        """获取构建产物列表

        Args:
            dist_dir: dist 目录路径

        Returns:
            构建产物路径列表
        """
        p = Path(dist_dir)
        if not p.is_dir():
            return []

        artifacts = []
        for item in p.iterdir():
            if item.name.endswith(".tar.gz") or item.name.endswith(".whl"):
                artifacts.append(str(item))

        return artifacts

    @staticmethod
    def clean_build_artifacts(package_path: str) -> bool:
        """清理构建产物

        Args:
            package_path: 包目录路径

        Returns:
            True 如果成功清理
        """
        p = Path(package_path)
        dirs_to_remove = ["build", "dist", "*.egg-info"]

        try:
            for pattern in dirs_to_remove:
                if pattern.endswith("-info"):
                    for item in p.glob(pattern):
                        shutil.rmtree(item)
                else:
                    target = p / pattern
                    if target.exists():
                        shutil.rmtree(target)
            return True
        except Exception:
            return False

    @staticmethod
    def estimate_package_size(package_path: str) -> int:
        """估算包的大小

        Args:
            package_path: 包目录路径

        Returns:
            总大小（字节）
        """
        p = Path(package_path)
        total_size = 0

        for file in p.rglob("*"):
            if file.is_file():
                total_size += file.stat().st_size

        return total_size

    @staticmethod
    def list_package_files(
        package_path: str, include_hidden: bool = False
    ) -> list[str]:
        """列出包中的文件

        Args:
            package_path: 包目录路径
            include_hidden: 是否包含隐藏文件

        Returns:
            文件名列表
        """
        p = Path(package_path)
        files: list[str] = []

        for item in p.iterdir():
            if item.is_file() and (include_hidden or not item.name.startswith(".")):
                files.append(item.name)

        return sorted(files)

    @staticmethod
    def check_installable(package_path: str) -> bool:
        """检查包是否可安装

        Args:
            package_path: 包目录路径

        Returns:
            True 如果包有安装配置
        """
        p = Path(package_path)
        return (p / "setup.py").exists() or (p / "pyproject.toml").exists()
