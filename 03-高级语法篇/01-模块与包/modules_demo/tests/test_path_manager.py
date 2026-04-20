"""PathManager 测试 - 模块搜索路径管理"""

import sys
from pathlib import Path

from app.core.path_manager import PathManager


class TestPathManager:
    """测试 PathManager 类"""

    def test_get_search_paths_returns_list(self) -> None:
        """get_search_paths 返回搜索路径列表"""
        paths = PathManager.get_search_paths()
        assert isinstance(paths, list)
        assert len(paths) > 0

    def test_get_search_paths_contains_stdlib(self) -> None:
        """搜索路径包含标准库路径"""
        paths = PathManager.get_search_paths()
        assert any("lib" in p.lower() or "python" in p.lower() for p in paths)

    def test_add_path_to_front(self, tmp_path: Path) -> None:
        """add_path 将路径添加到搜索路径前端"""
        test_path = str(tmp_path)
        original_len = len(sys.path)

        PathManager.add_path(test_path)
        assert sys.path[0] == test_path
        assert len(sys.path) == original_len + 1

        sys.path.remove(test_path)

    def test_remove_path_from_search(self, tmp_path: Path) -> None:
        """remove_path 从搜索路径移除指定路径"""
        test_path = str(tmp_path)
        sys.path.insert(0, test_path)

        PathManager.remove_path(test_path)
        assert test_path not in sys.path

    def test_path_exists_returns_bool(self, tmp_path: Path) -> None:
        """path_exists 返回布尔值"""
        assert PathManager.path_exists(str(tmp_path)) is True
        assert PathManager.path_exists("/nonexistent/path/xyz") is False

    def test_get_site_packages_returns_list(self) -> None:
        """get_site_packages 返回 site-packages 路径列表"""
        paths = PathManager.get_site_packages()
        assert isinstance(paths, list)
        if len(paths) > 0:
            assert all("site-packages" in p for p in paths)

    def test_resolve_module_path_returns_path_or_none(self) -> None:
        """resolve_module_path 返回路径或 None"""

        path = PathManager.resolve_module_path("os")
        assert path is None or isinstance(path, str)

        path = PathManager.resolve_module_path("nonexistent_module_xyz")
        assert path is None

    def test_get_current_dir_returns_string(self) -> None:
        """get_current_dir 返回当前目录字符串"""
        cwd = PathManager.get_current_dir()
        assert isinstance(cwd, str)
        assert len(cwd) > 0

    def test_find_module_in_paths_returns_path_or_none(self, tmp_path: Path) -> None:
        """find_module_in_paths 在指定路径中查找模块"""
        test_file = tmp_path / "test_module.py"
        test_file.write_text("# test")

        path = PathManager.find_module_in_paths("test_module", [str(tmp_path)])
        assert path == str(test_file)

        path = PathManager.find_module_in_paths("nonexistent", [str(tmp_path)])
        assert path is None
