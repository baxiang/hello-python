"""核心插件加载器"""

import importlib
import importlib.util
import sys
from pathlib import Path
from types import ModuleType
from typing import Any, Callable


class PluginLoader:
    """插件加载器类"""

    def __init__(self, base_path: str) -> None:
        """初始化插件加载器

        Args:
            base_path: 插件搜索的基础路径
        """
        self._base_path = base_path
        self._loaded_plugins: dict[str, ModuleType] = {}

    @property
    def base_path(self) -> str:
        """基础路径"""
        return self._base_path

    def load_plugin_from_path(self, plugin_path: str) -> ModuleType | None:
        """从指定路径加载插件

        Args:
            plugin_path: 插件目录路径

        Returns:
            加载的模块对象，失败返回 None
        """
        p = Path(plugin_path)
        if not p.is_dir() or not (p / "__init__.py").exists():
            return None

        plugin_name = p.name
        init_file = p / "__init__.py"

        try:
            spec = importlib.util.spec_from_file_location(
                plugin_name,
                str(init_file),
                submodule_search_locations=[str(p)],
            )
            if spec is None or spec.loader is None:
                return None

            module = importlib.util.module_from_spec(spec)
            sys.modules[plugin_name] = module
            spec.loader.exec_module(module)

            self._loaded_plugins[plugin_name] = module
            return module
        except Exception:
            return None

    def load_all_plugins(self) -> dict[str, ModuleType]:
        """加载所有发现的插件

        Returns:
            插件名到模块对象的字典
        """
        discovered = self.discover_plugins()
        for plugin_path in discovered:
            self.load_plugin_from_path(plugin_path)

        return self._loaded_plugins

    def discover_plugins(self) -> list[str]:
        """发现所有可用的插件

        Returns:
            发现的插件路径列表
        """
        plugins: list[str] = []
        base = Path(self._base_path)

        if not base.is_dir():
            return plugins

        for item in base.iterdir():
            if item.is_dir() and (item / "__init__.py").exists():
                plugins.append(str(item))

        return plugins

    def is_valid_plugin(self, plugin_path: str) -> bool:
        """验证是否为有效插件

        Args:
            plugin_path: 插件路径

        Returns:
            True 如果是有效的插件目录
        """
        p = Path(plugin_path)
        return p.is_dir() and (p / "__init__.py").exists()

    def get_plugin_metadata(self, plugin_path: str) -> dict[str, Any]:
        """获取插件的元数据

        Args:
            plugin_path: 插件路径

        Returns:
            元数据字典
        """
        metadata: dict[str, Any] = {}
        init_file = Path(plugin_path) / "__init__.py"

        if not init_file.exists():
            return metadata

        content = init_file.read_text()
        for line in content.splitlines():
            if line.strip().startswith("PLUGIN_"):
                parts = line.split("=")
                if len(parts) >= 2:
                    key = parts[0].strip()
                    value = parts[1].strip().strip("'\"")
                    metadata[key] = value

        return metadata

    def reload_plugin(self, plugin_path: str) -> ModuleType | None:
        """重新加载插件

        Args:
            plugin_path: 插件路径

        Returns:
            重新加载后的模块对象
        """
        plugin_name = Path(plugin_path).name

        if plugin_name in sys.modules:
            del sys.modules[plugin_name]

        return self.load_plugin_from_path(plugin_path)

    def unregister_plugin(self, plugin_name: str) -> bool:
        """注销插件

        Args:
            plugin_name: 插件名

        Returns:
            True 如果成功注销
        """
        if plugin_name in self._loaded_plugins:
            del self._loaded_plugins[plugin_name]

        if plugin_name in sys.modules:
            del sys.modules[plugin_name]
            return True

        return False

    def get_loaded_plugins(self) -> list[str]:
        """获取已加载插件列表

        Returns:
            已加载插件名列表
        """
        return list(self._loaded_plugins.keys())

    def load_plugin_by_name(self, plugin_name: str) -> ModuleType | None:
        """通过名称加载插件

        Args:
            plugin_name: 插件名

        Returns:
            模块对象，找不到返回 None
        """
        base = Path(self._base_path)
        plugin_path = base / plugin_name

        if plugin_path.exists():
            return self.load_plugin_from_path(str(plugin_path))

        return None

    def filter_plugins_by_criteria(
        self, criteria: Callable[[ModuleType], bool]
    ) -> list[str]:
        """根据条件过滤插件

        Args:
            criteria: 过滤条件函数

        Returns:
            符合条件的插件名列表
        """
        filtered: list[str] = []
        for name, module in self._loaded_plugins.items():
            if criteria(module):
                filtered.append(name)

        return filtered

    def get_plugin_dependencies(self, plugin_path: str) -> list[str]:
        """获取插件的依赖列表

        Args:
            plugin_path: 插件路径

        Returns:
            依赖模块名列表
        """
        init_file = Path(plugin_path) / "__init__.py"
        if not init_file.exists():
            return []

        content = init_file.read_text()
        deps: set[str] = set()

        for line in content.splitlines():
            if line.startswith("import "):
                module = line.split()[1].split(".")[0]
                deps.add(module)
            elif line.startswith("from "):
                module = line.split()[1].split(".")[0]
                deps.add(module)

        return list(deps)

    def has_plugin(self, plugin_name: str) -> bool:
        """检查是否已加载指定插件

        Args:
            plugin_name: 插件名

        Returns:
            True 如果插件已加载
        """
        return plugin_name in self._loaded_plugins