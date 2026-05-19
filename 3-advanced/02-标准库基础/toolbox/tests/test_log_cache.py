"""LogCache测试 - pickle模块"""

from datetime import datetime
from pathlib import Path

from app.core.log_cache import (
    LogCache,
    clear_cache,
    load_cache,
    save_cache,
)
from app.core.log_entry import LogEntry


class TestLogCache:
    def test_create_cache(self, tmp_path: Path):
        cache = LogCache(tmp_path / "cache.pkl")
        assert cache.cache_file == tmp_path / "cache.pkl"

    def test_save_entries(self, tmp_path: Path):
        entries = [
            LogEntry(datetime(2024, 4, 20, 10, 0), "INFO", "msg1"),
            LogEntry(datetime(2024, 4, 20, 11, 0), "ERROR", "msg2"),
        ]
        cache = LogCache(tmp_path / "cache.pkl")
        cache.save(entries)
        assert (tmp_path / "cache.pkl").exists()

    def test_load_entries(self, tmp_path: Path):
        entries = [
            LogEntry(datetime(2024, 4, 20, 10, 0), "INFO", "msg1"),
            LogEntry(datetime(2024, 4, 20, 11, 0), "ERROR", "msg2"),
        ]
        cache = LogCache(tmp_path / "cache.pkl")
        cache.save(entries)
        loaded = cache.load()
        assert len(loaded) == 2
        assert loaded[0].level == "INFO"

    def test_clear_cache(self, tmp_path: Path):
        entries = [
            LogEntry(datetime(2024, 4, 20, 10, 0), "INFO", "msg1"),
        ]
        cache = LogCache(tmp_path / "cache.pkl")
        cache.save(entries)
        cache.clear()
        assert not (tmp_path / "cache.pkl").exists()

    def test_load_empty(self, tmp_path: Path):
        cache = LogCache(tmp_path / "cache.pkl")
        loaded = cache.load()
        assert loaded == []

    def test_cache_exists(self, tmp_path: Path):
        cache = LogCache(tmp_path / "cache.pkl")
        assert cache.exists() is False
        cache.save([])
        assert cache.exists() is True


class TestSaveCache:
    def test_save_cache_func(self, tmp_path: Path):
        entries = [
            LogEntry(datetime(2024, 4, 20, 10, 0), "INFO", "msg1"),
        ]
        cache_file = tmp_path / "cache.pkl"
        save_cache(entries, cache_file)
        assert cache_file.exists()

    def test_save_cache_dict(self, tmp_path: Path):
        data = {"total_count": 5, "errors": 2}
        cache_file = tmp_path / "cache.pkl"
        save_cache(data, cache_file)
        assert cache_file.exists()


class TestLoadCache:
    def test_load_cache_func(self, tmp_path: Path):
        entries = [
            LogEntry(datetime(2024, 4, 20, 10, 0), "INFO", "msg1"),
            LogEntry(datetime(2024, 4, 20, 11, 0), "ERROR", "msg2"),
        ]
        cache_file = tmp_path / "cache.pkl"
        save_cache(entries, cache_file)
        loaded = load_cache(cache_file)
        assert len(loaded) == 2

    def test_load_cache_nonexistent(self, tmp_path: Path):
        nonexistent = tmp_path / "nonexistent.pkl"
        loaded = load_cache(nonexistent)
        assert loaded == []

    def test_load_cache_dict(self, tmp_path: Path):
        data = {"total_count": 5, "errors": 2}
        cache_file = tmp_path / "cache.pkl"
        save_cache(data, cache_file)
        loaded = load_cache(cache_file)
        assert loaded["total_count"] == 5


class TestClearCache:
    def test_clear_cache_func(self, tmp_path: Path):
        cache_file = tmp_path / "cache.pkl"
        save_cache([], cache_file)
        clear_cache(cache_file)
        assert not cache_file.exists()

    def test_clear_cache_nonexistent(self, tmp_path: Path):
        nonexistent = tmp_path / "nonexistent.pkl"
        clear_cache(nonexistent)


class TestCacheInfo:
    def test_cache_size(self, tmp_path: Path):
        entries = [
            LogEntry(datetime(2024, 4, 20, 10, 0), "INFO", "msg1"),
        ]
        cache = LogCache(tmp_path / "cache.pkl")
        cache.save(entries)
        size = cache.size()
        assert size > 0

    def test_cache_modified_time(self, tmp_path: Path):
        entries = [
            LogEntry(datetime(2024, 4, 20, 10, 0), "INFO", "msg1"),
        ]
        cache = LogCache(tmp_path / "cache.pkl")
        cache.save(entries)
        modified = cache.modified_time()
        assert modified is not None
