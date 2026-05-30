"""数据结构测试"""

from app.core.structures import (
    dict_operations,
    list_operations,
    set_operations,
    tuple_operations,
)


def test_list_operations():
    result = list_operations([1, 2, 3, 4, 5])
    assert result["length"] == 5
    assert result["slice"] == [1, 2, 3]
    assert result["reverse"] == [5, 4, 3, 2, 1]


def test_dict_operations():
    result = dict_operations({"name": "Python", "version": 3.11})
    assert result["keys"] == ["name", "version"]
    assert result["get"] == "Python"


def test_set_operations():
    result = set_operations({1, 2, 3}, {3, 4, 5})
    assert result["union"] == {1, 2, 3, 4, 5}
    assert result["intersection"] == {3}


def test_tuple_operations():
    result = tuple_operations((10, 20))
    assert result["original"] == (10, 20)
    assert result["slice"] == (10, 20)
    assert result["x"] == 10
    assert result["y"] == 20
