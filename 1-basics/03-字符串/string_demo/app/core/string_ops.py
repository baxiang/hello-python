"""字符串操作示例"""

from typing import Any


def string_operations(s: str) -> dict[str, Any]:
    """字符串基本操作"""
    return {
        "original": s,
        "length": len(s),
        "upper": s.upper(),
        "lower": s.lower(),
        "capitalize": s.capitalize(),
        "reverse": s[::-1]
    }


def string_formatting(name: str, value: float) -> dict[str, str]:
    """字符串格式化"""
    return {
        "f_string": f"{name} {value:.2f}",
        "format": "{} {:.2f}".format(name, value),
        "percent": "%s %.2f" % (name, value)
    }


def string_methods(s: str) -> dict[str, Any]:
    """字符串方法"""
    return {
        "strip": s.strip(),
        "split": s.split(","),
        "join": "-".join(s.split(",")),
        "find": s.find("python"),
        "replace": s.replace("python", "Python")
    }


def string_validation(s: str) -> dict[str, bool]:
    """字符串验证"""
    return {
        "isdigit": s.isdigit(),
        "isalpha": s.isalpha(),
        "isalnum": s.isalnum(),
        "isspace": s.isspace()
    }