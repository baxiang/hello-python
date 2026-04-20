"""模块搜索路径管理器"""

import sys
from pathlib import Path


class PathManager:
    """模块搜索路径管理工具类"""

    @staticmethod
    def get_search_paths() -> list[str]:
        """获取当前模块搜索路径列表

        Returns:
            sys.path 的副本
        """
        return list(sys.path)

    @staticmethod
    def add_path(path: str, position: int = 0) -> None:
        """添加路径到模块搜索路径

        Args:
            path: 要添加的路径
            position: 插入位置，默认为 0（最前面）
        """
        if path not in sys.path:
            sys.path.insert(position, path)

    @staticmethod
    def remove_path(path: str) -> bool:
        """从搜索路径中移除指定路径

        Args:
            path: 要移除的路径

        Returns:
            True 如果成功移除，False 如果路径不存在
        """
        if path in sys.path:
            sys.path.remove(path)
            return True
        return False

    @staticmethod
    def path_exists(path: str) -> bool:
        """检查路径是否存在

        Args:
            path: 路径字符串

        Returns:
            True 如果路径存在
        """
        return Path(path).exists()

    @staticmethod
    def get_site_packages() -> list[str]:
        """获取所有 site-packages 路径

        Returns:
            site-packages 路径列表
        """
        return [p for p in sys.path if "site-packages" in p]

    @staticmethod
    def resolve_module_path(module_name: str) -> str | None:
        """解析模块的文件路径

        Args:
            module_name: 模块名称

        Returns:
            模块文件路径，找不到返回 None
        """
        if module_name in sys.modules:
            mod = sys.modules[module_name]
            return getattr(mod, "__file__", None)

        import importlib.util

        spec = importlib.util.find_spec(module_name)
        if spec is not None:
            return spec.origin
        return None

    @staticmethod
    def get_current_dir() -> str:
        """获取当前工作目录

        Returns:
            当前工作目录路径
        """
        return str(Path.cwd())

    @staticmethod
    def find_module_in_paths(module_name: str, paths: list[str]) -> str | None:
        """在指定路径列表中查找模块文件

        Args:
            module_name: 模块名称
            paths: 搜索路径列表

        Returns:
            找到的模块文件路径，未找到返回 None
        """
        for search_path in paths:
            module_file = Path(search_path) / f"{module_name}.py"
            if module_file.exists():
                return str(module_file)

            package_init = Path(search_path) / module_name / "__init__.py"
            if package_init.exists():
                return str(package_init)

        return None