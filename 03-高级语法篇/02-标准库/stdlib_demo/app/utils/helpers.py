"""辅助函数"""

import json
from typing import Any


def to_json(data: Any) -> str:
    """转换为 JSON"""
    return json.dumps(data, ensure_ascii=False, indent=2)


def from_json(json_str: str) -> Any:
    """从 JSON 解析"""
    return json.loads(json_str)