# 装饰器与闭包

本章讲解 Python 装饰器与闭包的完整知识体系，包括函数进阶、闭包原理和装饰器用法。

---

## 章节导航

| 章节 | 文件 | 主题 |
|------|------|------|
| 01 | [01-函数进阶.md](./01-函数进阶.md) | 函数是一等公民、嵌套函数、LEGB |
| 02 | [02-闭包详解.md](./02-闭包详解.md) | 闭包概念、nonlocal、应用场景 |
| 03 | [03-装饰器基础.md](./03-装饰器基础.md) | 装饰器语法、常用装饰器 |
| 04 | [04-装饰器进阶.md](./04-装饰器进阶.md) | 带参数装饰器、类装饰器 |

---

## 核心概念

### 闭包

```python
def outer(x):
    def inner(y):
        return x + y  # 引用外层变量 x
    return inner

add5 = outer(5)
print(add5(3))  # 8
```

### 装饰器

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print("前处理")
        result = func(*args, **kwargs)
        print("后处理")
        return result
    return wrapper

@my_decorator
def my_func():
    print("执行函数")
```

### 常用装饰器

```python
# 计时
@timer
def slow_function(): ...

# 日志
@logger
def important_function(): ...

# 缓存
@lru_cache(maxsize=128)
def expensive_function(): ...

# 重试
@retry(times=3)
def unstable_function(): ...
```