"""插件B - 示例插件"""

__all__ = ["PluginB", "execute"]

PLUGIN_NAME = "plugin_b"
PLUGIN_VERSION = "0.5.0"


class PluginB:
    """示例插件B"""

    def __init__(self):
        self.name = PLUGIN_NAME
        self.version = PLUGIN_VERSION

    def execute(self, data: str) -> dict:
        return {
            "plugin": self.name,
            "version": self.version,
            "input": data,
            "status": "processed",
        }


def execute(data: str) -> dict:
    """插件入口函数"""
    plugin = PluginB()
    return plugin.execute(data)
