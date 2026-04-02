"""基础语法测试"""

from app.core.syntax import check_score, loop_examples, comprehension_examples


def test_check_score():
    assert check_score(95) == "优秀"
    assert check_score(85) == "良好"
    assert check_score(65) == "及格"
    assert check_score(45) == "不及格"


def test_loop_examples():
    result = loop_examples(5)
    assert result == [1, 2, 3, 4, 5]


def test_comprehension_examples():
    result = comprehension_examples()
    assert len(result["squares"]) == 10
    assert result["even_squares"] == [0, 4, 16, 36, 64]