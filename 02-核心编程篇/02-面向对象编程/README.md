# 面向对象编程

本章讲解 Python 面向对象编程的完整知识体系，包括类与对象、继承、封装、多态和设计原则。

---

## 章节导航

| 章节 | 文件 | 主题 |
|------|------|------|
| 01 | [01-面向对象基础.md](./01-面向对象基础.md) | 类与对象、定义和创建 |
| 02 | [02-属性与方法.md](./02-属性与方法.md) | 实例属性、类属性、三种方法 |
| 03 | [03-继承.md](./03-继承.md) | 继承基础、super()、多重继承 |
| 04 | [04-封装.md](./04-封装.md) | 私有属性、@property |
| 05 | [05-多态.md](./05-多态.md) | 多态、鸭子类型、抽象基类 |
| 06 | [06-设计原则.md](./06-设计原则.md) | 组合vs继承、SOLID |
| 07 | [07-数据类.md](./07-数据类.md) | @dataclass 数据容器类 |

---

## 面向对象四大特性

```
┌─────────────────────────────────────────┐
│       面向对象四大特性                  │
├─────────────────────────────────────────┤
│                                         │
│  1️⃣ 抽象（Abstraction）                 │
│     提取共同特征，忽略无关细节          │
│                                         │
│  2️⃣ 封装（Encapsulation）               │
│     隐藏内部实现，只暴露接口            │
│                                         │
│  3️⃣ 继承（Inheritance）                 │
│     子类继承父类的特征和行为            │
│                                         │
│  4️⃣ 多态（Polymorphism）                │
│     同一接口，不同实现                  │
│                                         │
└─────────────────────────────────────────┘
```

## 核心语法速查

```python
# 定义类
class ClassName:
    """文档字符串"""
    
    class_attr = "类属性"  # 所有实例共享
    
    def __init__(self, param):
        self.instance_attr = param  # 实例属性
    
    def instance_method(self):
        """实例方法"""
        pass
    
    @classmethod
    def class_method(cls):
        """类方法"""
        pass
    
    @staticmethod
    def static_method():
        """静态方法"""
        pass

# 继承
class Child(Parent):
    def __init__(self):
        super().__init__()

# 私有属性
self.__private = "私有"

# @property
@property
def name(self):
    return self.__name

@name.setter
def name(self, value):
    self.__name = value
```