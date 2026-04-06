"""pytest 配置文件"""

import importlib.util
import sys
from pathlib import Path


def load_module(name: str, path: Path):
    """动态加载模块（支持数字开头的文件名）"""
    spec = importlib.util.spec_from_file_location(name, path)
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        return module
    raise ImportError(f"Cannot load module {name} from {path}")


# 添加 src 目录到 Python 路径
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# 加载所有模块
modules = {
    "variables": src_path / "03_variables.py",
    "operators": src_path / "04_operators.py",
    "flow_control": src_path / "05_flow_control.py",
    "strings": src_path / "06_strings.py",
    "lists": src_path / "07_lists.py",
    "tuples": src_path / "08_tuples.py",
    "dicts": src_path / "09_dicts.py",
    "sets": src_path / "10_sets.py",
    "comprehensions": src_path / "11_comprehensions.py",
}

for name, path in modules.items():
    load_module(name, path)
