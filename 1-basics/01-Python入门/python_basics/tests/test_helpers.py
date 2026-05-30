"""辅助函数测试"""

from app.utils.helpers import print_result


def test_print_result(capsys):
    print_result("测试", {"a": 1, "b": 2})
    captured = capsys.readouterr()
    assert "测试" in captured.out
    assert "a: 1" in captured.out
    assert "b: 2" in captured.out
