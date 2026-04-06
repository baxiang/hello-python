"""高级特性测试"""

from app.core.advanced import (
    log_call,
    with_context,
    Config,
    BaseService,
    is_string_list,
    is_positive_dict,
    process_data,
    sum_values,
)


def test_log_call():
    @log_call
    def add(a: int, b: int) -> int:
        return a + b

    result = add(1, 2)
    assert result == 3


def test_with_context():
    @with_context
    def process(context: str, data: str) -> str:
        return f"[{context}] {data}"

    result = process("测试数据")
    assert "默认上下文" in result
    assert "测试数据" in result


def test_config():
    config = Config(9000)
    assert config.port == 9000
    assert Config.MAX_SIZE == 100
    assert Config.MIN_SIZE == 1
    assert Config.DEFAULT_PORT == 8080


def test_base_service():
    service = BaseService()
    assert service.get_version() == "1.0.0"


def test_is_string_list():
    assert is_string_list(["a", "b", "c"]) == True
    assert is_string_list([1, "b", 3]) == False
    assert is_string_list([]) == True


def test_is_positive_dict():
    assert is_positive_dict({"a": 1, "b": 2}) == True
    assert is_positive_dict({"a": 0, "b": 2}) == False
    assert is_positive_dict({"a": -1, "b": 2}) == False


def test_process_data():
    assert process_data(["a", "b", "c"]) == "a b c"
    assert process_data([1, 2, 3]) == "非字符串列表"


def test_sum_values():
    assert sum_values({"a": 1, "b": 2, "c": 3}) == 6
    assert sum_values({"a": 0, "b": 1}) == 0
    assert sum_values({"a": -1, "b": 2}) == 0
