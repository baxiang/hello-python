"""导入机制解析工具"""

import importlib
import importlib.util
import sys
from types import ModuleType
from typing import Any


class ImportResolver:
    """导入机制解析工具类"""

    @staticmethod
    def import_module(module_name: str) -> ModuleType:
        """导入模块

        Args:
            module_name: 模块名称

        Returns:
            模块对象

        Raises:
            ImportError: 模块不存在
        """
        return importlib.import_module(module_name)

    @staticmethod
    def safe_import(module_name: str) -> ModuleType | None:
        """安全导入模块，失败返回 None

        Args:
            module_name: 模块名称

        Returns:
            模块对象，失败返回 None
        """
        try:
            return importlib.import_module(module_name)
        except ImportError:
            return None

    @staticmethod
    def reload_module(module: ModuleType) -> ModuleType:
        """重新加载模块

        Args:
            module: 要重新加载的模块对象

        Returns:
            重新加载后的模块对象
        """
        return importlib.reload(module)

    @staticmethod
    def get_module_spec(module_name: str) -> importlib.machinery.ModuleSpec | None:
        """获取模块规格说明

        Args:
            module_name: 模块名称

        Returns:
            ModuleSpec 对象，找不到返回 None
        """
        return importlib.util.find_spec(module_name)

    @staticmethod
    def is_importable(module_name: str) -> bool:
        """检查模块是否可导入

        Args:
            module_name: 模块名称

        Returns:
            True 如果模块可以被导入
        """
        spec = importlib.util.find_spec(module_name)
        return spec is not None

    @staticmethod
    def get_importer(module: ModuleType) -> Any:
        """获取模块的导入器

        Args:
            module: 模块对象

        Returns:
            导入器对象，无则返回 None
        """
        return getattr(module, "__loader__", None)

    @staticmethod
    def resolve_dotted_name(name: str) -> Any:
        """解析点分名称获取属性

        Args:
            name: 点分名称，如 "os.path.join"

        Returns:
            属性对象，找不到返回 None
        """
        parts = name.split(".")
        if not parts:
            return None

        try:
            obj = importlib.import_module(parts[0])
            for part in parts[1:]:
                obj = getattr(obj, part)
            return obj
        except (ImportError, AttributeError):
            return None

    @staticmethod
    def get_module_dependencies(module: ModuleType) -> list[str]:
        """获取模块的依赖列表

        Args:
            module: 模块对象

        Returns:
            依赖模块名列表
        """
        deps: set[str] = set()

        for name, value in vars(module).items():
            if isinstance(value, ModuleType):
                deps.add(value.__name__)

        return sorted(deps)

    @staticmethod
    def import_from_module(module_name: str, attr_name: str) -> Any:
        """从模块导入指定属性

        Args:
            module_name: 模块名称
            attr_name: 属性名称

        Returns:
            属性对象

        Raises:
            ImportError: 模块不存在
            AttributeError: 属性不存在
        """
        module = importlib.import_module(module_name)
        return getattr(module, attr_name)

    @staticmethod
    def clear_from_cache(module_name: str) -> bool:
        """从模块缓存中清除

        Args:
            module_name: 模块名称

        Returns:
            True 如果成功清除
        """
        if module_name in sys.modules:
            del sys.modules[module_name]
            return True
        return False

    @staticmethod
    def get_cached_module(module_name: str) -> ModuleType | None:
        """获取缓存的模块

        Args:
            module_name: 模块名称

        Returns:
            缓存的模块对象，不存在返回 None
        """
        return sys.modules.get(module_name)