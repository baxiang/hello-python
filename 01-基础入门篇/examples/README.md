# Python 基础入门篇示例代码

本目录包含《Python基础入门篇》所有章节的可运行示例代码和测试。

## 项目结构

```
examples/
├── pyproject.toml     # 项目配置
├── README.md          # 本文件
├── src/               # 示例代码
└── tests/             # 测试代码
```

## 快速开始

### 安装依赖

```bash
cd examples
uv sync
```

### 运行示例

```bash
# 运行单个章节示例
uv run python src/03_variables.py

# 运行流程控制章节（包含 match 语句）
uv run python src/05_flow_control.py
```

### 运行测试

```bash
# 运行所有测试
uv run pytest

# 运行单个章节测试
uv run pytest tests/test_03_variables.py -v

# 查看测试覆盖率
uv run pytest --cov=src --cov-report=html
```

## 章节列表

| 编号 | 章节名称 | 示例文件 | 测试文件 |
|-----|---------|---------|---------|
| 01 | Python简介 | src/01_python_intro.py | - |
| 02 | 环境搭建 | src/02_environment.py | - |
| 03 | 变量与数据类型 | src/03_variables.py | tests/test_03_variables.py |
| 04 | 运算符 | src/04_operators.py | tests/test_04_operators.py |
| 05 | 流程控制 | src/05_flow_control.py | tests/test_05_flow_control.py |
| 06 | 字符串 | src/06_strings.py | tests/test_06_strings.py |
| 07 | 列表 | src/07_lists.py | tests/test_07_lists.py |
| 08 | 元组 | src/08_tuples.py | tests/test_08_tuples.py |
| 09 | 字典 | src/09_dicts.py | tests/test_09_dicts.py |
| 10 | 集合 | src/10_sets.py | tests/test_10_sets.py |
| 11 | 推导式 | src/11_comprehensions.py | tests/test_11_comprehensions.py |

## 技术要求

- Python 3.11+
- 使用现代类型提示语法

## License

MIT