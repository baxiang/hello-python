"""辅助函数"""

import json
from typing import Any


def pretty_print(data: Any) -> str:
    """美化打印"""
    return json.dumps(data, ensure_ascii=False, indent=2, default=str)
