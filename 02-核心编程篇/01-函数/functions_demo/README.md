# 函数

Python 函数示例项目，覆盖第 01-05 章（函数基础 → 参数详解 → 作用域 → Lambda → 内置函数）。

## 场景

学生成绩统计系统：通过分数计算、等级评定、排序、统计等操作，演示 Python 函数的各种用法。

## 项目结构

```
functions_demo/
├── pyproject.toml
├── app/
│   ├── __init__.py
│   ├── core/
│   │   ├── functions.py    # ch01-02: 基础函数、高阶函数、参数类型
│   │   ├── builtins.py     # ch04-05: Lambda、内置函数（map/filter/sorted/zip 等）
│   │   └── scope.py        # ch03: 作用域（global/nonlocal/LEGB/闭包陷阱）
│   └── utils/
│       └── helpers.py      # 格式化工具
└── tests/
    └── test_functions.py   # 32 个测试，全覆盖
```

## 安装

```bash
uv sync
```

## 使用示例

```python
from app.core.functions import create_student, letter_grade, merge_sort
from app.core.builtins import sort_students, score_stats
from app.core.scope import make_score_accumulator

# ch01: 基础函数
letter_grade(95)          # → "A"
merge_sort([3, 1, 4, 1])  # → [1, 1, 3, 4]

# ch02: 全部参数类型
create_student("张三", 85, "数学", "努力", comment="表现优秀")

# ch03: 闭包状态机
add, avg, reset = make_score_accumulator()
add(80); add(90); avg()   # → 85.0

# ch04-05: Lambda + 内置函数
students = [{"name": "张三", "score": 85}, {"name": "李四", "score": 92}]
sort_students(students, reverse=True)
score_stats([80, 90, 70])  # → {"min": 70, "max": 90, ...}
```

## 运行测试

```bash
uv run pytest               # 全部测试
uv run pytest -v            # 详细输出
uv run pytest -k "ch01"     # 只运行 ch01 相关测试
```

## 章节映射

| 代码文件 | 对应章节 | 核心内容 |
|---------|---------|---------|
| `functions.py` | ch01-02 | 函数定义、高阶函数、递归、位置/默认/*args/**kwargs/keyword-only |
| `scope.py` | ch03 | global、nonlocal、LEGB、闭包陷阱修复 |
| `builtins.py` | ch04-05 | Lambda、map/filter/sorted/reduce、enumerate/zip/any/all/isinstance |
