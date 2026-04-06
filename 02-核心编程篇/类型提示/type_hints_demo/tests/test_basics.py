"""基础类型提示测试"""

from app.core.basics import (
    count_words,
    get_point,
    unique_items,
    find_user,
    parse_value,
    apply_operation,
    get_user_score,
)


def test_count_words():
    result = count_words("hello world hello")
    assert result["hello"] == 2
    assert result["world"] == 1


def test_get_point():
    x, y = get_point()
    assert x == 10.5
    assert y == 20.3


def test_unique_items():
    result = unique_items(["a", "b", "a", "c"])
    assert result == {"a", "b", "c"}


def test_find_user():
    user = find_user(1)
    assert user is not None
    assert user["name"] == "张三"

    user = find_user(999)
    assert user is None


def test_parse_value():
    assert parse_value("123") == 123
    assert parse_value("3.14") == 3.14
    assert parse_value("true") == True
    assert parse_value("false") == False


def test_apply_operation():
    assert apply_operation(lambda x, y: x + y, 5, 3) == 8
    assert apply_operation(lambda x, y: x * y, 5, 3) == 15


def test_get_user_score():
    scores = get_user_score(1)
    assert scores is not None
    assert "张三" in scores
