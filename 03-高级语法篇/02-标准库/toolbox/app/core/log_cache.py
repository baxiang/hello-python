"""日志缓存模块 - pickle模块示例

演示pickle模块的核心功能:
- pickle序列化
- pickle反序列化
- 安全警告
- 缓存管理
"""

import pickle
from collections.abc import Sequence
from datetime import datetime
from pathlib import Path
from typing import Any

from app.core.log_entry import LogEntry


class LogCache:
    """日志缓存管理器"""

    def __init__(self, cache_file: Path | str):
        self.cache_file = Path(cache_file)

    def save(self, data: Sequence[LogEntry] | Any) -> None:
        """保存数据到缓存

        Args:
            data: 要缓存的数据

        Warning:
            pickle可能存在安全风险，只缓存可信数据
        """
        save_cache(data, self.cache_file)

    def load(self) -> list[LogEntry] | Any:
        """从缓存加载数据

        Returns:
            缓存的数据或空列表

        Warning:
            不要加载不可信来源的pickle文件
        """
        return load_cache(self.cache_file)

    def clear(self) -> None:
        """清除缓存"""
        clear_cache(self.cache_file)

    def exists(self) -> bool:
        """检查缓存是否存在"""
        return self.cache_file.exists()

    def size(self) -> int:
        """获取缓存文件大小"""
        if not self.exists():
            return 0
        return self.cache_file.stat().st_size

    def modified_time(self) -> datetime | None:
        """获取缓存修改时间"""
        if not self.exists():
            return None
        return datetime.fromtimestamp(self.cache_file.stat().st_mtime)


def save_cache(data: Any, filepath: Path | str) -> None:
    """保存数据到pickle文件

    Args:
        data: 要缓存的数据
        filepath: 文件路径

    Warning:
        pickle可能存在安全风险，只缓存可信数据
    """
    path = Path(filepath)
    with path.open("wb") as f:
        pickle.dump(data, f)


def load_cache(filepath: Path | str) -> list[LogEntry] | Any:
    """从pickle文件加载数据

    Args:
        filepath: 文件路径

    Returns:
        缓存的数据或空列表

    Warning:
        不要加载不可信来源的pickle文件
    """
    path = Path(filepath)
    if not path.exists():
        return []
    with path.open("rb") as f:
        return pickle.load(f)


def clear_cache(filepath: Path | str) -> None:
    """清除缓存文件

    Args:
        filepath: 文件路径
    """
    path = Path(filepath)
    if path.exists():
        path.unlink()
