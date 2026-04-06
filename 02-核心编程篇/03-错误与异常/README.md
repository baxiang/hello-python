# 错误与异常

本章讲解 Python 错误与异常处理的完整知识体系，包括异常类型、异常处理、抛出异常和上下文管理器。

---

## 章节导航

| 章节 | 文件 | 主题 |
|------|------|------|
| 01 | [01-错误与异常基础.md](./01-错误与异常基础.md) | 语法错误、常见异常类型 |
| 02 | [02-异常处理.md](./02-异常处理.md) | try-except、else、finally |
| 03 | [03-抛出异常.md](./03-抛出异常.md) | raise、自定义异常、断言 |
| 04 | [04-上下文管理器.md](./04-上下文管理器.md) | with 语句、自定义上下文管理器 |

---

## 核心知识点

### 异常处理结构

```python
try:
    # 可能出错的代码
except ValueError:
    # 处理特定异常
except Exception as e:
    # 处理其他异常
else:
    # 没有异常时执行
finally:
    # 总是执行
```

### 常见异常类型

| 异常 | 说明 |
|------|------|
| ValueError | 值错误 |
| TypeError | 类型错误 |
| IndexError | 索引越界 |
| KeyError | 键不存在 |
| FileNotFoundError | 文件不存在 |
| ZeroDivisionError | 除零错误 |

### 抛出异常

```python
raise ValueError("错误信息")
assert condition, "断言失败"
```

### 上下文管理器

```python
with open("file.txt") as f:
    content = f.read()
```