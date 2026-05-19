# 模块与包

Python 模块与包示例项目，演示模块导入、包结构、命名空间包等核心概念。

## 项目结构

```
modules_demo/
├── app/                      # 主应用包
│   ├── __init__.py          # 包初始化，演示 __all__ 和公共API
│   ├── core/                # 核心模块
│   ├── utils/               # 工具模块
│   ├── models/              # 数据模型
│   ├── services/            # 服务层
│   └── constants.py         # 常量定义
├── sample_plugins/          # 示例插件目录
│   ├── plugin_a/           # 插件A
│   └── plugin_b/           # 插件B
└── tests/                   # 测试套件
```

## 知识点覆盖

| 章节 | 知识点 | 示例文件 |
|------|--------|----------|
| 3.1 模块导入方式 | import/from/import as | `app/__init__.py` |
| 3.2 包的结构与__init__.py | 包初始化、__all__ | `app/__init__.py` |
| 3.3 相对导入与绝对导入 | .module vs app.module | `app/core/`, `app/utils/` |
| 3.4 __name__ == "__main__" | 模块入口检测 | `app/core/runner.py` |
| 3.5 命名空间包 | PEP 420, 无__init__.py | `app/models/`, `app/services/` |
| 3.6 模块搜索路径 | sys.path 操作 | `app/utils/path_utils.py` |
| 3.7 动态导入 | importlib | `app/utils/import_utils.py` |
| 3.8 循环导入问题及解决 | 延迟导入、重构 | `app/core/circular_a.py` |

## 安装

```bash
cd "03-高级语法篇/01-模块与包/modules_demo"
uv sync
```

## 运行测试

```bash
# 运行所有测试
uv run pytest tests/ -v

# 运行特定测试文件
uv run pytest tests/test_imports.py -v
uv run pytest tests/test_packages.py -v
uv run pytest tests/test_namespace_packages.py -v
uv run pytest tests/test_dynamic_import.py -v
uv run pytest tests/test_circular_import.py -v
```

## 代码质量

```bash
uv run ruff check .
uv run ruff check --fix .
uv run ruff format .
```

## 快速使用示例

### 基本导入

```python
# 绝对导入
from app import greet, __version__
from app.core import calculate, DataProcessor
from app.utils import format_output, PathManager

# 使用导入的功能
print(greet("World"))  # Hello, World!
print(calculate(10, 5))  # 15
```

### 相对导入 (在包内)

```python
# 在 app/core/module.py 中
from ..utils.formatting import format_output  # 上级目录导入
from . import runner  # 当前目录导入
```

### 命名空间包

```python
# app/models 和 app/services 是命名空间包
from app.models import User, Product
from app.services import UserService, ProductService

user = User(id=1, name="Alice")
service = UserService()
service.save(user)
```

### 动态导入

```python
from app.utils.import_utils import dynamic_import

# 动态导入模块
module = dynamic_import("app.core.runner")
# 动态导入并调用函数
result = dynamic_import("app.core.runner", "run_main")
```

### 模块搜索路径

```python
from app.utils.path_utils import add_to_path, remove_from_path

# 添加自定义路径
add_to_path("/custom/modules")
# 移除路径
remove_from_path("/custom/modules")
```

### 循环导入解决

```python
# app/core/circular_a.py 和 circular_b.py 演示了循环导入问题
# 通过延迟导入解决
from app.core.circular_a import process_a

result = process_a("test")  # 正确处理循环依赖
```

## 示例插件使用

项目包含两个示例插件，演示包结构设计：

### Plugin A

```python
from sample_plugins.plugin_a import PluginA, run

# 方式1: 使用入口函数
result = run()  # "Plugin plugin_a v1.0.0 is running"

# 方式2: 实例化类
plugin = PluginA()
print(plugin.name)     # "plugin_a"
print(plugin.version)  # "1.0.0"
print(plugin.run())    # "Plugin plugin_a v1.0.0 is running"
```

### Plugin B

```python
from sample_plugins.plugin_b import PluginB, execute

# 方式1: 使用入口函数
result = execute("hello")
# {"plugin": "plugin_b", "version": "0.5.0", "input": "hello", "status": "processed"}

# 方式2: 实例化类
plugin = PluginB()
result = plugin.execute("data")
```

## 版本

当前版本: 0.1.0