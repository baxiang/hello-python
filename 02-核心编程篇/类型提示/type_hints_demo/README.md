# 类型提示示例项目

本项目包含 Python 类型提示的实用示例，覆盖基础到高级特性。

## 项目结构

```
app/
├── core/
│   ├── basics.py      # 容器类型、Optional/Union、Callable 示例
│   ├── generics.py    # 泛型函数、Stack、Repository 示例
│   ├── protocols.py   # Protocol、TypedDict 示例
│   └── advanced.py    # ParamSpec、Final、TypeGuard 示例
│   └── utils/
│       └── helpers.py # 辅助函数
tests/
├── test_basics.py     # basics 模块测试
├── test_generics.py   # generics 模块测试
├── test_protocols.py  # protocols 模块测试
├── test_advanced.py   # advanced 模块测试
```

## 运行测试

```bash
# 运行所有测试
uv run pytest -v

# 运行特定模块测试
uv run pytest tests/test_basics.py -v
uv run pytest tests/test_generics.py -v
```

## 类型检查（可选）

```bash
uv run mypy app/
```

## 学习建议

1. 先阅读对应章节文档（01-基础、02-进阶、03-高级）
2. 查看示例代码理解语法
3. 运行测试验证行为
4. 修改代码尝试变体

## 示例对照

| 文档章节 | 示例模块 | 测试文件 |
|---------|---------|---------|
| 容器类型、Optional、Callable | basics.py | test_basics.py |
| 泛型深入 | generics.py | test_generics.py |
| 协议、TypedDict | protocols.py | test_protocols.py |
| ParamSpec、Final、TypeGuard | advanced.py | test_advanced.py |