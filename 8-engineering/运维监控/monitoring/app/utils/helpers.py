"""辅助函数"""

import platform
import os
from typing import Dict, Any


def get_system_info() -> Dict[str, Any]:
    """获取系统信息"""
    return {
        "platform": platform.platform(),
        "python_version": platform.python_version(),
        "cpu_count": os.cpu_count(),
        "hostname": platform.node()
    }