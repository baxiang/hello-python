"""模块属性工具 - PluginInfo 类"""

import sys
from dataclasses import dataclass
from types import ModuleType
from typing import Any


@dataclass
class ModuleInfo:
    """模块信息数据类"""

    name: str
    file: str | None
    doc: str | None
    package: str | None


class PluginInfo:
    """插件信息工具类 - 展示模块属性的使用"""

    @staticmethod
    def get_module_info(module: ModuleType) -> ModuleInfo:
        """获取模块基本信息

        Args:
            module: 模块对象

        Returns:
            ModuleInfo 实例，包含模块名称、文件路径、文档和包名
        """
        return ModuleInfo(
            name=module.__name__,
            file=getattr(module, "__file__", None),
            doc=getattr(module, "__doc__", None),
            package=getattr(module, "__package__", None),
        )

    @staticmethod
    def get_exports(module: ModuleType) -> list[str]:
        """获取模块的公开导出列表

        如果模块定义了 __all__，返回 __all__ 中的内容；
        否则返回不以单下划线开头的属性名。

        Args:
            module: 模块对象

        Returns:
            公开属性名列表
        """
        if hasattr(module, "__all__"):
            return list(module.__all__)
        return [name for name in dir(module) if not name.startswith("_")]

    @staticmethod
    def get_doc(module: ModuleType) -> str | None:
        """获取模块的文档字符串

        Args:
            module: 模块对象

        Returns:
            文档字符串，无则返回 None
        """
        return getattr(module, "__doc__", None)

    @staticmethod
    def get_path(module: ModuleType) -> str | None:
        """获取模块文件路径

        Args:
            module: 模块对象

        Returns:
            文件路径字符串，内置模块返回 None
        """
        return getattr(module, "__file__", None)

    @staticmethod
    def get_package(module: ModuleType) -> str | None:
        """获取模块所属包名

        Args:
            module: 模块对象

        Returns:
            包名字符串，顶层模块返回 None
        """
        return getattr(module, "__package__", None)

    @staticmethod
    def get_namespace(module: ModuleType) -> dict[str, Any]:
        """获取模块的命名空间字典

        Args:
            module: 模块对象

        Returns:
            模块的 __dict__ 命名空间
        """
        return dict(getattr(module, "__dict__", {}))

    @staticmethod
    def is_loaded(module_name: str) -> bool:
        """检查模块是否已加载

        Args:
            module_name: 模块名称

        Returns:
            True 如果模块已加载到 sys.modules
        """
        return module_name in sys.modules

    @staticmethod
    def list_loaded_modules() -> list[str]:
        """列出所有已加载的模块

        Returns:
            已加载模块名列表
        """
        return sorted(sys.modules.keys())

    @staticmethod
    def get_mode(module: ModuleType) -> str:
        """获取模块运行模式

        Args:
            module: 模块对象

        Returns:
            'main' 如果是主模块，'imported' 如果是被导入模块
        """
        name = getattr(module, "__name__", "")
        return "main" if name == "__main__" else "imported"
