"""异常示例"""


class ValidationError(Exception):
    """验证错误"""
    pass


class AgeError(ValidationError):
    """年龄错误"""
    pass


def divide(a: int, b: int) -> float | None:
    """除法（带异常处理）"""
    try:
        return a / b
    except ZeroDivisionError:
        print("错误: 除数不能为零")
        return None


def validate_age(age: int) -> bool:
    """验证年龄"""
    if not isinstance(age, int):
        raise ValidationError("年龄必须是整数")
    if age < 0:
        raise AgeError("年龄不能为负数")
    if age > 150:
        raise AgeError("年龄不合理")
    return True


def safe_convert(value: str) -> int | None:
    """安全转换"""
    try:
        return int(value)
    except (ValueError, TypeError):
        return None