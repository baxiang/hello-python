"""文件操作功能测试"""

from pathlib import Path

import pytest

from processor.operations import FileOperations


def test_add_prefix(tmp_path: Path) -> None:
    """添加前缀：验证所有文件名以指定前缀开头"""
    for name in ["a.txt", "b.txt", "c.txt"]:
        (tmp_path / name).write_text("content")

    results = FileOperations.add_prefix(str(tmp_path), "new_")

    assert len(results) == 3
    for file in tmp_path.iterdir():
        assert file.name.startswith("new_")


def test_add_suffix(tmp_path: Path) -> None:
    """添加后缀：验证文件名在扩展名前插入了指定后缀"""
    (tmp_path / "a.txt").write_text("content")
    (tmp_path / "b.txt").write_text("content")

    FileOperations.add_suffix(str(tmp_path), "_done")

    names = {f.name for f in tmp_path.iterdir()}
    assert "a_done.txt" in names
    assert "b_done.txt" in names


def test_add_timestamp(tmp_path: Path) -> None:
    """添加时间戳：验证操作有返回结果（文件名含时间戳）"""
    (tmp_path / "report.txt").write_text("content")

    results = FileOperations.add_timestamp(str(tmp_path))

    assert len(results) == 1
    # 重命名后的文件名包含 _ 分隔的时间戳部分
    renamed = list(tmp_path.iterdir())[0]
    assert renamed.stem.startswith("report_")


def test_organize_by_extension(tmp_path: Path) -> None:
    """按扩展名整理：验证文件被移动到对应扩展名子目录"""
    (tmp_path / "a.txt").write_text("content")
    (tmp_path / "b.txt").write_text("content")
    (tmp_path / "c.py").write_text("pass")

    result = FileOperations.organize_by_extension(str(tmp_path))

    assert result[".txt"] == 2
    assert result[".py"] == 1
    assert (tmp_path / ".txt").is_dir()
    assert (tmp_path / ".py").is_dir()


def test_find_duplicates(tmp_path: Path) -> None:
    """查找重复文件：大小相同的文件应被检测为重复"""
    data = b"hello world"
    (tmp_path / "file1.txt").write_bytes(data)
    (tmp_path / "file2.txt").write_bytes(data)
    (tmp_path / "unique.txt").write_bytes(b"different content here")

    result = FileOperations.find_duplicates(str(tmp_path))

    # 只有大小相同的两个文件应出现在结果中
    assert len(result) == 1
    duplicate_group = list(result.values())[0]
    assert len(duplicate_group) == 2
