"""模块示例"""

import os
import sys
from pathlib import Path
from typing import Any


def get_module_info() -> dict[str, Any]:
    """获取模块信息"""
    return {
        "name": __name__,
        "file": __file__,
        "package": __package__,
        "doc": __doc__
    }


def list_imported_modules() -> list[str]:
    """列出已导入的模块"""
    return sorted(sys.modules.keys())


def get_path_info() -> dict[str, Any]:
    """获取路径信息"""
    return {
        "python_path": sys.path[:5],
        "current_dir": os.getcwd(),
        "executable": sys.executable
    }


def create_package_structure(name: str) -> dict[str, str]:
    """创建包结构"""
    return {
        "package": name,
        "init_file": f"{name}/__init__.py",
        "module": f"{name}/module.py",
        "subpackage": f"{name}/subpackage/__init__.py"
    }