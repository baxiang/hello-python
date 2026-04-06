"""标准库测试"""

from app.core.stdlib_usage import collections_examples, itertools_examples, functools_examples


def test_collections_examples():
    result = collections_examples()
    assert "counter" in result
    assert "defaultdict" in result


def test_itertools_examples():
    result = itertools_examples()
    assert result["chain"] == [1, 2, 3, 4]
    assert len(result["combinations"]) == 3


def test_functools_examples():
    result = functools_examples()
    assert result["reduce"] == 15
    assert result["partial"] == 25