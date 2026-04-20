"""插件A - 示例插件"""

__all__ = ["PluginA", "run"]

PLUGIN_NAME = "plugin_a"
PLUGIN_VERSION = "1.0.0"


class PluginA:
    """示例插件A"""

    def __init__(self):
        self.name = PLUGIN_NAME
        self.version = PLUGIN_VERSION

    def run(self) -> str:
        return f"Plugin {self.name} v{self.version} is running"


def run() -> str:
    """插件入口函数"""
    plugin = PluginA()
    return plugin.run()
