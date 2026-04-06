"""辅助函数"""

from typing import Any
import json


def pretty_print(data: Any) -> str:
    """美化打印"""
    return json.dumps(data, ensure_ascii=False, indent=2, default=str)