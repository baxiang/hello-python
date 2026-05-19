"""基础类型提示示例"""

from collections.abc import Callable

UserId = int
UserName = str
UserDict = dict[UserName, int]


def count_words(text: str) -> dict[str, int]:
    """统计单词频率"""
    result: dict[str, int] = {}
    for word in text.split():
        result[word] = result.get(word, 0) + 1
    return result


def get_point() -> tuple[float, float]:
    """获取坐标点"""
    return (10.5, 20.3)


def unique_items(items: list[str]) -> set[str]:
    """获取唯一元素"""
    return set(items)


def find_user(user_id: int) -> dict[str, str] | None:
    """查找用户"""
    users: dict[int, dict[str, str]] = {
        1: {"name": "张三", "email": "zhangsan@example.com"},
        2: {"name": "李四", "email": "lisi@example.com"},
    }
    return users.get(user_id)


def parse_value(value: str) -> int | float | bool | str:
    """解析字符串值为最合适的类型（ch01：Union 类型返回）

    >>> parse_value("42")       → 42 (int)
    >>> parse_value("3.14")     → 3.14 (float)
    >>> parse_value("true")     → True (bool)
    >>> parse_value("hello")    → "hello" (str, 原样返回)
    """
    if value.isdigit():
        return int(value)
    try:
        return float(value)
    except ValueError:
        if value.lower() == "true":
            return True
        if value.lower() == "false":
            return False
        return value  # 无法解析时原样返回


def apply_operation(
    func: Callable[[int, int], int],
    a: int,
    b: int
) -> int:
    """应用运算函数"""
    return func(a, b)


def callback_pattern(callback: Callable[[str], None]) -> None:
    """回调模式示例"""
    message = "处理完成"
    callback(message)


def get_user_score(user_id: UserId) -> UserDict | None:
    """获取用户分数"""
    scores: UserDict = {"张三": 85, "李四": 92}
    if user_id in [1, 2]:
        return scores
    return None
