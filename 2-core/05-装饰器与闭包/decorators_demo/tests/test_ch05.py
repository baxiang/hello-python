"""第 5 章测试 — functools 标准装饰器"""

from app.decorators.ch05_functools import (
    DataReport,
    fibonacci,
    not_found,
    ok_response,
    parse_config,
    process_data,
)


class TestFunctoolsDecorators:
    """测试 functools 装饰器"""

    def setup_method(self):
        fibonacci.cache_clear()
        parse_config.cache_clear()

    def test_lru_cache_fibonacci(self):
        assert fibonacci(0) == 0
        assert fibonacci(1) == 1
        assert fibonacci(10) == 55
        assert fibonacci(30) == 832040

    def test_lru_cache_returns_cached(self):
        r1 = parse_config("db_host")
        r2 = parse_config("db_host")
        assert r1 == r2

    def test_lru_cache_info(self):
        parse_config("key1")
        parse_config("key1")
        parse_config("key2")
        info = parse_config.cache_info()
        assert info.hits >= 1
        assert info.misses >= 2

    def test_cached_property_computed_once(self):
        report = DataReport([1, 2, 3, 4, 5])
        _ = report.total
        _ = report.total
        _ = report.average
        assert report.calc_count == 2

    def test_cached_property_values(self):
        report = DataReport([10, 20, 30])
        assert report.total == 60
        assert report.average == 20.0

    def test_singledispatch_string(self):
        assert process_data("hello") == "String: HELLO"

    def test_singledispatch_int(self):
        assert process_data(21) == "Integer: 42"

    def test_singledispatch_list(self):
        assert process_data([1, 2, 3]) == "List: 3 items"

    def test_singledispatch_dict(self):
        assert process_data({"a": 1, "b": 2}) == "Dict: 2 keys"

    def test_singledispatch_default(self):
        assert process_data(set([1, 2])) == "Unknown type: set"

    def test_partial_ok_response(self):
        result = ok_response("success")
        assert result["status"] == 200
        assert result["message"] == "success"
        assert result["content_type"] == "application/json"

    def test_partial_not_found(self):
        result = not_found("Not found")
        assert result["status"] == 404
