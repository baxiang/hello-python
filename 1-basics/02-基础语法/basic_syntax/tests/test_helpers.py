"""辅助函数测试"""

from app.utils.helpers import format_output


def test_format_output():
    result = format_output("分数", 95)
    assert result == "分数: 95"


def test_format_output_with_string():
    result = format_output("状态", "完成")
    assert result == "状态: 完成"
