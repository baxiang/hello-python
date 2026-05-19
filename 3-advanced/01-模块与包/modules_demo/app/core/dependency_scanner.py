"""依赖分析工具"""

import ast
from pathlib import Path
from types import ModuleType


class DependencyScanner:
    """依赖分析工具类"""

    _STDLIB_MODULES: set[str] | None = None

    @staticmethod
    def scan_file_imports(file_path: str) -> list[str]:
        """扫描文件的导入语句

        Args:
            file_path: 文件路径

        Returns:
            导入的模块名列表
        """
        path = Path(file_path)
        if not path.exists():
            return []

        try:
            content = path.read_text()
            tree = ast.parse(content)
        except (OSError, SyntaxError):
            return []

        imports: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.append(node.module.split(".")[0])

        return list(set(imports))

    @staticmethod
    def scan_module_imports(module: ModuleType) -> list[str]:
        """扫描模块的导入依赖

        Args:
            module: 模块对象

        Returns:
            依赖模块名列表
        """
        imports: set[str] = set()
        for name in dir(module):
            obj = getattr(module, name)
            if isinstance(obj, ModuleType):
                imports.add(obj.__name__.split(".")[0])

        return sorted(imports)

    @staticmethod
    def scan_package_dependencies(package_path: str) -> list[str]:
        """扫描包的所有依赖

        Args:
            package_path: 包目录路径

        Returns:
            所有依赖模块名列表
        """
        p = Path(package_path)
        if not p.is_dir():
            return []

        all_deps: set[str] = set()

        for py_file in p.rglob("*.py"):
            deps = DependencyScanner.scan_file_imports(str(py_file))
            all_deps.update(deps)

        all_deps.discard(p.name)
        return sorted(all_deps)

    @staticmethod
    def get_import_graph(package_path: str) -> dict[str, list[str]]:
        """获取包内模块的导入关系图

        Args:
            package_path: 包目录路径

        Returns:
            字典，键为模块名，值为该模块导入的其他模块列表
        """
        p = Path(package_path)
        if not p.is_dir():
            return {}

        graph: dict[str, list[str]] = {}
        package_name = p.name

        for py_file in p.rglob("*.py"):
            if py_file.name == "__init__.py":
                module_name = py_file.parent.name
            else:
                module_name = py_file.stem

            relative_path = py_file.relative_to(p)
            if relative_path.parent != Path("."):
                parts = list(relative_path.parts[:-1])
                is_init = py_file.name == "__init__.py"
                mod_part = module_name if is_init else py_file.stem
                parts.append(mod_part)
                module_name = ".".join(parts)

            deps = DependencyScanner.scan_file_imports(str(py_file))
            internal_deps = [
                d
                for d in deps
                if d == package_name
                or d.startswith(f"{package_name}.")
                or d in [f.stem for f in p.rglob("*.py") if f != py_file]
            ]
            graph[module_name] = internal_deps

        return graph

    @staticmethod
    def detect_circular_imports(package_path: str) -> list[tuple[str, str]]:
        """检测循环导入

        Args:
            package_path: 包目录路径

        Returns:
            循环导入对列表
        """
        graph = DependencyScanner.get_import_graph(package_path)
        circular: list[tuple[str, str]] = []

        for module_a, deps_a in graph.items():
            for dep in deps_a:
                if dep in graph and module_a in graph.get(dep, []):
                    pair = tuple(sorted([module_a, dep]))
                    if pair not in circular:
                        circular.append(pair)

        return circular

    @staticmethod
    def get_stdlib_modules() -> list[str]:
        """获取 Python 标准库模块列表

        Returns:
            标准库模块名列表
        """
        if DependencyScanner._STDLIB_MODULES is None:
            from sys import stdlib_module_names

            DependencyScanner._STDLIB_MODULES = set(stdlib_module_names)

        return sorted(DependencyScanner._STDLIB_MODULES)

    @staticmethod
    def is_stdlib(module_name: str) -> bool:
        """检查模块是否为标准库

        Args:
            module_name: 模块名

        Returns:
            True 如果是标准库模块
        """
        stdlib = DependencyScanner.get_stdlib_modules()
        base_name = module_name.split(".")[0]
        return base_name in stdlib

    @staticmethod
    def get_third_party_deps(file_path: str) -> list[str]:
        """获取文件的第三方依赖

        Args:
            file_path: 文件路径

        Returns:
            第三方模块名列表
        """
        all_imports = DependencyScanner.scan_file_imports(file_path)
        stdlib = set(DependencyScanner.get_stdlib_modules())
        return [imp for imp in all_imports if imp not in stdlib]
