"""日志扫描模块 - pathlib模块示例

演示pathlib模块的核心功能:
- 目录遍历 (iterdir)
- glob模式匹配 (glob/rglob)
- 文件信息获取 (Path属性)
- 路径拼接 (/运算符)
"""

from collections.abc import Iterator
from datetime import datetime
from pathlib import Path


class LogScanner:
    """日志文件扫描器"""

    def __init__(self, root_dir: Path | str):
        self.root_dir = Path(root_dir)

    def scan(self, pattern: str = "*") -> list[Path]:
        """扫描目录中的文件"""
        return [f for f in self.root_dir.glob(pattern) if f.is_file()]

    def scan_recursive(self, pattern: str = "*") -> list[Path]:
        """递归扫描目录"""
        return [f for f in self.root_dir.rglob(pattern) if f.is_file()]

    def iter_files(self) -> Iterator[Path]:
        """迭代目录中的文件"""
        for entry in self.root_dir.iterdir():
            if entry.is_file():
                yield entry

    def join_path(self, *parts: str) -> Path:
        """拼接路径"""
        return self.root_dir / Path(*parts)

    def relative_path(self, path: Path | str) -> Path:
        """获取相对路径"""
        return Path(path).relative_to(self.root_dir)

    def is_subdirectory(self, path: Path | str) -> bool:
        """判断是否为子目录"""
        try:
            Path(path).relative_to(self.root_dir)
            return True
        except ValueError:
            return False


def scan_directory(directory: Path | str, pattern: str = "*") -> list[Path]:
    """扫描目录中的文件

    Args:
        directory: 目录路径
        pattern: glob模式

    Returns:
        文件路径列表
    """
    path = Path(directory)
    return [f for f in path.glob(pattern) if f.is_file()]


def find_log_files(directory: Path | str, recursive: bool = False) -> list[Path]:
    """查找日志文件

    Args:
        directory: 目录路径
        recursive: 是否递归查找

    Returns:
        日志文件路径列表
    """
    path = Path(directory)

    files = []
    if recursive:
        files.extend(path.rglob("*.log"))
    else:
        files.extend(path.glob("*.log"))

    return [f for f in files if f.is_file()]


def get_file_info(filepath: Path | str) -> dict:
    """获取文件信息

    Args:
        filepath: 文件路径

    Returns:
        文件信息字典
    """
    path = Path(filepath)

    if not path.exists():
        return {
            "name": path.name,
            "path": str(path),
            "exists": False,
        }

    stat = path.stat()
    return {
        "name": path.name,
        "path": str(path),
        "exists": True,
        "size": stat.st_size,
        "modified": datetime.fromtimestamp(stat.st_mtime),
        "is_dir": path.is_dir(),
        "is_file": path.is_file(),
        "extension": path.suffix,
    }
