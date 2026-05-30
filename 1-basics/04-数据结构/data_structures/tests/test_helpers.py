"""辅助函数测试"""

from app.utils.helpers import flatten_list, unique_items


def test_flatten_list():
    result = flatten_list([[1, 2], [3, 4], [5, 6]])
    assert result == [1, 2, 3, 4, 5, 6]


def test_flatten_list_single_inner():
    result = flatten_list([[1, 2, 3]])
    assert result == [1, 2, 3]


def test_flatten_list_empty():
    result = flatten_list([])
    assert result == []


def test_unique_items():
    result = unique_items([1, 2, 2, 3, 3, 3])
    assert sorted(result) == [1, 2, 3]


def test_unique_items_all_same():
    result = unique_items(["a", "a", "a"])
    assert result == ["a"]


def test_unique_items_empty():
    result = unique_items([])
    assert result == []
