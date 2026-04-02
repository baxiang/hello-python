"""数据结构示例"""

from typing import Any
from collections import namedtuple


def list_operations(items: list) -> dict[str, Any]:
    """列表操作"""
    result = items.copy()
    return {
        "original": items,
        "append": result + ["new"],
        "slice": items[:3],
        "reverse": items[::-1],
        "length": len(items)
    }


def dict_operations(data: dict) -> dict[str, Any]:
    """字典操作"""
    return {
        "keys": list(data.keys()),
        "values": list(data.values()),
        "items": list(data.items()),
        "get": data.get("name", "N/A"),
        "length": len(data)
    }


def set_operations(a: set, b: set) -> dict[str, set]:
    """集合操作"""
    return {
        "union": a | b,
        "intersection": a & b,
        "difference": a - b,
        "symmetric_difference": a ^ b
    }


def tuple_operations(data: tuple) -> dict[str, Any]:
    """元组操作"""
    Point = namedtuple("Point", ["x", "y"])
    p = Point(data[0], data[1])
    return {
        "original": data,
        "slice": data[:2],
        "namedtuple": p,
        "x": p.x,
        "y": p.y
    }