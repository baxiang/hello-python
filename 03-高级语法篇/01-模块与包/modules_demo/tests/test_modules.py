"""模块测试"""

from app.core.module_example import get_module_info, get_path_info


def test_get_module_info():
    result = get_module_info()
    assert "name" in result
    assert "file" in result


def test_get_path_info():
    result = get_path_info()
    assert "python_path" in result
    assert "current_dir" in result