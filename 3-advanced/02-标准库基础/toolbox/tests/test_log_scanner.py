"""LogScanner测试 - pathlib模块"""

from pathlib import Path

from app.core.log_scanner import (
    LogScanner,
    find_log_files,
    get_file_info,
    scan_directory,
)


class TestLogScanner:
    def test_create_scanner(self, tmp_path: Path):
        scanner = LogScanner(tmp_path)
        assert scanner.root_dir == tmp_path

    def test_scan_all_files(self, tmp_path: Path):
        (tmp_path / "app.log").touch()
        (tmp_path / "error.log").touch()
        scanner = LogScanner(tmp_path)
        files = scanner.scan()
        assert len(files) == 2

    def test_scan_with_pattern(self, tmp_path: Path):
        (tmp_path / "app.log").touch()
        (tmp_path / "error.log").touch()
        (tmp_path / "config.yaml").touch()
        scanner = LogScanner(tmp_path)
        log_files = scanner.scan(pattern="*.log")
        assert len(log_files) == 2

    def test_scan_recursive(self, tmp_path: Path):
        subdir = tmp_path / "logs"
        subdir.mkdir()
        (tmp_path / "app.log").touch()
        (subdir / "error.log").touch()
        scanner = LogScanner(tmp_path)
        files = scanner.scan_recursive()
        assert len(files) == 2

    def test_scan_recursive_pattern(self, tmp_path: Path):
        subdir = tmp_path / "logs"
        subdir.mkdir()
        (tmp_path / "app.log").touch()
        (tmp_path / "config.yaml").touch()
        (subdir / "error.log").touch()
        (subdir / "data.json").touch()
        scanner = LogScanner(tmp_path)
        log_files = scanner.scan_recursive(pattern="*.log")
        assert len(log_files) == 2


class TestScanDirectory:
    def test_scan_directory(self, tmp_path: Path):
        (tmp_path / "file1.txt").touch()
        (tmp_path / "file2.txt").touch()
        files = scan_directory(tmp_path)
        assert len(files) == 2

    def test_scan_directory_with_pattern(self, tmp_path: Path):
        (tmp_path / "file1.log").touch()
        (tmp_path / "file2.txt").touch()
        files = scan_directory(tmp_path, pattern="*.log")
        assert len(files) == 1


class TestFindLogFiles:
    def test_find_log_files(self, tmp_path: Path):
        (tmp_path / "app.log").touch()
        (tmp_path / "error.log").touch()
        (tmp_path / "data.txt").touch()
        log_files = find_log_files(tmp_path)
        assert len(log_files) == 2

    def test_find_log_files_recursive(self, tmp_path: Path):
        subdir = tmp_path / "nested"
        subdir.mkdir()
        (tmp_path / "root.log").touch()
        (subdir / "nested.log").touch()
        log_files = find_log_files(tmp_path, recursive=True)
        assert len(log_files) == 2


class TestGetFileInfo:
    def test_get_file_info(self, tmp_path: Path):
        test_file = tmp_path / "test.log"
        test_file.write_text("hello world")
        info = get_file_info(test_file)
        assert info["name"] == "test.log"
        assert info["size"] == 11
        assert info["exists"] is True
        assert "modified" in info

    def test_get_file_info_nonexistent(self, tmp_path: Path):
        nonexistent = tmp_path / "nonexistent.log"
        info = get_file_info(nonexistent)
        assert info["exists"] is False


class TestPathOperations:
    def test_join_path(self, tmp_path: Path):
        scanner = LogScanner(tmp_path)
        full_path = scanner.join_path("logs", "app.log")
        assert str(full_path).endswith("logs/app.log")

    def test_relative_path(self, tmp_path: Path):
        scanner = LogScanner(tmp_path)
        subdir = tmp_path / "logs"
        subdir.mkdir()
        rel = scanner.relative_path(subdir)
        assert rel == Path("logs")

    def test_is_subdirectory(self, tmp_path: Path):
        scanner = LogScanner(tmp_path)
        subdir = tmp_path / "logs"
        subdir.mkdir()
        assert scanner.is_subdirectory(subdir) is True
