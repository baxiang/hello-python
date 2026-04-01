# 函数

本章讲解 Python 函数的完整知识体系，包括函数基础、参数详解、变量作用域和 Lambda 匿名函数。

---

## 章节导航

| 章节 | 文件 | 主题 |
|------|------|------|
| 01 | [01-函数基础.md](./01-函数基础.md) | 函数定义、调用、返回值 |
| 02 | [02-函数参数详解.md](./02-函数参数详解.md) | 位置参数、默认参数、*args、**kwargs |
| 03 | [03-变量作用域.md](./03-变量作用域.md) | LEGB 规则、global、nonlocal |
| 04 | [04-Lambda匿名函数.md](./04-Lambda匿名函数.md) | lambda 语法、使用场景 |

---

## 核心知识点

### 函数定义

```python
def 函数名(参数):
    """文档字符串"""
    函数体
    return 返回值
```

### 参数类型

| 参数类型 | 说明 | 示例 |
|----------|------|------|
| 位置参数 | 按顺序传递 | `func(1, 2)` |
| 默认参数 | 有预设值 | `def func(a=1)` |
| 关键字参数 | 按名称传递 | `func(a=1, b=2)` |
| *args | 可变位置参数 | `def func(*args)` |
| **kwargs | 可变关键字参数 | `def func(**kwargs)` |

### 作用域规则

```
LEGB 查找顺序：
Local → Enclosing → Global → Built-in
```

### Lambda 语法

```python
lambda 参数: 表达式

# 最佳使用场景：sorted、filter、map 的参数
sorted(data, key=lambda x: x[1])
```