"""包结构处理工具"""

import os
from pathlib import Path
from types import ModuleType


class PluginPackage:
    """包结构处理工具类"""

    def __init__(self, package_path: str) -> None:
        """初始化包对象

        Args:
            package_path: 包目录路径
        """
        self._path = package_path
        self._name = Path(package_path).name

    @property
    def name(self) -> str:
        """包名"""
        return self._name

    @property
    def path(self) -> str:
        """包路径"""
        return self._path

    @property
    def modules(self) -> list[str]:
        """包中的模块列表"""
        return self.list_modules(self._path)

    @staticmethod
    def is_package(path: str) -> bool:
        """判断路径是否为 Python 包

        Args:
            path: 路径字符串

        Returns:
            True 如果是包（包含 __init__.py 的目录）
        """
        p = Path(path)
        return p.is_dir() and (p / "__init__.py").exists()

    @staticmethod
    def get_package_info(package_path: str) -> dict[str, str | None]:
        """获取包的基本信息

        Args:
            package_path: 包目录路径

        Returns:
            包含 name, path, docstring 的字典
        """
        p = Path(package_path)
        init_file = p / "__init__.py"

        docstring = None
        if init_file.exists():
            content = init_file.read_text()
            if content.startswith('"""'):
                end = content.find('"""', 3)
                if end > 0:
                    docstring = content[3:end].strip()

        return {
            "name": p.name,
            "path": str(p),
            "docstring": docstring,
        }

    @staticmethod
    def list_modules(package_path: str, include_private: bool = False) -> list[str]:
        """列出包中的所有模块和子包

        Args:
            package_path: 包目录路径
            include_private: 是否包含以下划线开头的模块

        Returns:
            模块名列表
        """
        modules: list[str] = []
        p = Path(package_path)

        if not p.is_dir():
            return modules

        for item in p.iterdir():
            if item.name.startswith("_") and not include_private:
                continue

            if item.is_file() and item.suffix == ".py":
                modules.append(item.stem)
            elif item.is_dir() and (item / "__init__.py").exists():
                modules.append(item.name)

        return sorted(modules)

    @staticmethod
    def create_package(package_path: str, docstring: str | None = None) -> bool:
        """创建新的包结构

        Args:
            package_path: 包目录路径
            docstring: 包的文档字符串

        Returns:
            True 如果创建成功
        """
        p = Path(package_path)
        try:
            p.mkdir(parents=True, exist_ok=True)
            init_file = p / "__init__.py"

            if docstring:
                init_file.write_text(f'"""{docstring}"""\n')
            else:
                init_file.write_text("")

            return True
        except Exception:
            return False

    @staticmethod
    def is_namespace_package(package_path: str) -> bool:
        """判断是否为命名空间包

        命名空间包是没有 __init__.py 的目录

        Args:
            package_path: 包目录路径

        Returns:
            True 如果是命名空间包
        """
        p = Path(package_path)
        return p.is_dir() and not (p / "__init__.py").exists()

    @staticmethod
    def get_package_version(package_path: str) -> str | None:
        """获取包的版本号

        从 __init__.py 中读取 __version__

        Args:
            package_path: 包目录路径

        Returns:
            版本字符串，未找到返回 None
        """
        init_file = Path(package_path) / "__init__.py"
        if not init_file.exists():
            return None

        content = init_file.read_text()
        for line in content.splitlines():
            if line.strip().startswith("__version__"):
                parts = line.split("=")
                if len(parts) >= 2:
                    version = parts[1].strip().strip("'\"")
                    return version

        return None

    @staticmethod
    def from_module(module: ModuleType) -> "PluginPackage":
        """从模块对象创建 PluginPackage 实例

        Args:
            module: Python 模块对象

        Returns:
            PluginPackage 实例
        """
        path = getattr(module, "__path__", [None])[0]
        if path is None:
            file_path = getattr(module, "__file__", None)
            if file_path:
                path = str(Path(file_path).parent)

        if path is None:
            path = "."

        return PluginPackage(str(path))