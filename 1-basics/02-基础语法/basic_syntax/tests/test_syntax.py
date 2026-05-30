"""基础语法测试"""

from app.core.syntax import (
    check_score,
    comprehension_examples,
    loop_examples,
    match_example,
)


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


def test_match_example_known():
    assert match_example(200) == "OK"
    assert match_example(404) == "Not Found"
    assert match_example(500) == "Server Error"


def test_match_example_unknown():
    assert match_example(302) == "Unknown"
    assert match_example(999) == "Unknown"
