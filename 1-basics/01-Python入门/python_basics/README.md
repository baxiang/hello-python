# Python 基础入门

Python 基础语法示例项目，包含变量、数据类型、运算符等内容。

## 安装

```bash
uv sync
```

## 运行

```bash
uv run python -c "from app import __version__; print(f'版本: {__version__}')"
```

## 结构

- `app/core/basics.py` - 基础语法示例
- `app/utils/helpers.py` - 辅助函数
- `tests/` - 测试文件