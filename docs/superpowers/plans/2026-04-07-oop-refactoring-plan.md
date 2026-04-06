# OOP Documentation Refactoring Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refactor 6 OOP documentation files with 6-step progressive teaching method, Python 3.11+ requirements, type annotations, and navigation links.

**Architecture:** Transform each document through structured additions: add version requirement header, problem-driven introduction, restructure content into 6-step format while preserving existing detailed content and ASCII diagrams, add type hints to all code examples, and add navigation links between chapters.

**Tech Stack:** Markdown documentation, Python 3.11+ type hints syntax

---

## File Structure

**Documents to modify:**
- `/Users/baxiang/Documents/hello-python/02-核心编程篇/面向对象编程/01-面向对象基础.md` - OOP basics
- `/Users/baxiang/Documents/hello-python/02-核心编程篇/面向对象编程/02-属性与方法.md` - Properties and methods
- `/Users/baxiang/Documents/hello-python/02-核心编程篇/面向对象编程/03-继承.md` - Inheritance
- `/Users/baxiang/Documents/hello-python/02-核心编程篇/面向对象编程/04-封装.md` - Encapsulation
- `/Users/baxiang/Documents/hello-python/02-核心编程篇/面向对象编程/05-多态.md` - Polymorphism
- `/Users/baxiang/Documents/hello-python/02-核心编程篇/面向对象编程/06-设计原则.md` - Design principles

---

## Task 1: Refactor 01-面向对象基础.md

**Files:**
- Modify: `/Users/baxiang/Documents/hello-python/02-核心编程篇/面向对象编程/01-面向对象基础.md`

- [ ] **Step 1: Add version requirement and problem scenario**

Add at the beginning of the file (after the title):

```markdown
# 面向对象基础

> **Python 版本要求：** 3.11+

本章讲解 Python 面向对象编程的基本概念，包括类与对象的关系、类的定义和对象的创建。

---

## 为什么需要面向对象？

### 问题场景

假设你要开发一个学生管理系统，需要管理大量学生的信息（姓名、年龄、成绩等）。

**使用面向过程的方式：**

```python
# 每个学生需要多个变量
student1_name = "张三"
student1_age = 18
student1_score = 85

student2_name = "李四"
student2_age = 17
student2_score = 92

# 每个学生都需要单独处理
def print_student(name, age, score):
    print(f"{name}, {age}岁, 成绩:{score}")

print_student(student1_name, student1_age, student1_score)
print_student(student2_name, student2_age, student2_score)
```

**问题：**
- 学生数量增加时，变量数量爆炸
- 相关数据没有组织在一起，容易出错
- 代码难以维护和扩展

**使用面向对象的方式：**

```python
class Student:
    def __init__(self, name: str, age: int, score: int) -> None:
        self.name = name
        self.age = age
        self.score = score
    
    def print_info(self) -> None:
        print(f"{self.name}, {self.age}岁, 成绩:{self.score}")

# 创建学生对象
students = [
    Student("张三", 18, 85),
    Student("李四", 17, 92),
]

# 统一处理
for student in students:
    student.print_info()
```

**优势：**
- 数据和行为封装在一起
- 代码更易维护和扩展
- 可以创建任意数量的学生对象

---

## 章节导航

- 上一篇：[函数进阶](../函数进阶/)
- 下一篇：[属性与方法](./02-属性与方法.md)
- 返回：[目录](../../README.md)

---

## 第一部分：面向过程 vs 面向对象

### 1.1 概念动机

面向对象是一种编程思想，它将数据和操作数据的方法封装在一起，形成"对象"。

```
┌─────────────────────────────────────────────────────────────┐
│              面向过程 vs 面向对象                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   面向过程：                                                 │
│   ✓ 关注"怎么做"（步骤）                                   │
│   ✓ 程序 = 函数 + 数据                                     │
│   ✓ 例如：洗菜() → 切菜() → 炒菜()                         │
│                                                             │
│   面向对象：                                                 │
│   ✓ 关注"谁来做"（对象）                                   │
│   ✓ 程序 = 对象 + 消息                                     │
│   ✓ 例如：厨师.洗菜()、厨师.切菜()、厨师.炒菜()            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 最简示例
```

- [ ] **Step 2: Refactor remaining sections with type annotations**

Continue from where Step 1 left off, replacing the existing "面向过程 vs 面向对象" section with the new structure. Update all code examples with type annotations:

```python
# ─────────────────────────────────────
# 面向过程：关注"怎么做"（步骤）
# ─────────────────────────────────────

def 洗菜() -> None:
    print("洗菜")

def 切菜() -> None:
    print("切菜")

def 炒菜() -> None:
    print("炒菜")

# 按步骤调用
洗菜()
切菜()
炒菜()


# ─────────────────────────────────────
# 面向对象：关注"谁来做"（对象）
# ─────────────────────────────────────

class 厨师:
    def 洗菜(self) -> None:
        print("洗菜")

    def 切菜(self) -> None:
        print("切菜")

    def 炒菜(self) -> None:
        print("炒菜")

# 创建对象并调用
chef = 厨师()
chef.洗菜()
chef.切菜()
chef.炒菜()
```

Keep the existing ASCII diagrams and detailed explanations, just add the new 6-step structure headers.

- [ ] **Step 3: Add type hints to all remaining code examples**

Update the Dog class example:

```python
class Dog:
    """表示狗的类"""

    # 类属性（所有实例共享）
    species: str = "Canis familiaris"

    def __init__(self, name: str, age: int, breed: str = "中华田园犬") -> None:
        """
        初始化方法
        参数:
            name: 名字
            age: 年龄
            breed: 品种（默认"中华田园犬"）
        """
        # 实例属性（每个实例独立）
        self.name: str = name
        self.age: int = age
        self.breed: str = breed

    def bark(self) -> None:
        """狗叫"""
        print(f"{self.name} 在叫：汪汪汪！")

    def run(self) -> None:
        """跑步"""
        print(f"{self.name} 正在奔跑！")

    def get_human_age(self) -> int:
        """计算人类年龄"""
        return self.age * 7


# ─────────────────────────────────────
# 创建和使用对象
# ─────────────────────────────────────

# 创建对象（实例化）
my_dog: Dog = Dog("Buddy", 3)
your_dog: Dog = Dog("Max", 5, "金毛")

# 访问属性
print(my_dog.name)      # Buddy
print(my_dog.species)   # Canis familiaris（类属性）

# 调用方法
my_dog.bark()             # Buddy 在叫：汪汪汪！
print(my_dog.get_human_age())  # 21
```

- [ ] **Step 4: Save and commit Task 1**

Commit message: `refactor(oop): add progressive teaching structure to 01-面向对象基础.md`

---

## Task 2: Refactor 02-属性与方法.md

**Files:**
- Modify: `/Users/baxiang/Documents/hello-python/02-核心编程篇/面向对象编程/02-属性与方法.md`

- [ ] **Step 1: Add version requirement, problem scenario, and navigation**

Add at the beginning:

```markdown
# 属性与方法

> **Python 版本要求：** 3.11+

本章讲解 Python 类的属性和方法，包括实例属性、类属性、实例方法、类方法和静态方法。

---

## 为什么需要不同的属性和方法？

### 问题场景

假设你要开发一个学生管理系统，需要：
1. 统计总学生数量（所有学生共享）
2. 每个学生有自己的姓名和年龄
3. 提供工具方法判断年龄是否成年

**问题：**
- 如何让所有学生共享同一个计数器？
- 如何区分每个学生独有的数据？
- 如何创建与实例无关的工具函数？

**解决方案：**
- **类属性**：所有实例共享的数据（如学生总数）
- **实例属性**：每个实例独有的数据（如姓名、年龄）
- **类方法**：操作类数据的方法
- **静态方法**：与类相关但不需要实例的工具函数

---

## 章节导航

- 上一篇：[面向对象基础](./01-面向对象基础.md)
- 下一篇：[继承](./03-继承.md)
- 返回：[目录](../../README.md)

---

## 第一部分：实例属性 vs 类属性

### 1.1 概念动机
```

- [ ] **Step 2: Update all code examples with type annotations**

```python
class Student:
    # 类属性（所有实例共享）
    school: str = "第一中学"
    count: int = 0

    def __init__(self, name: str, age: int) -> None:
        # 实例属性（每个实例独立）
        self.name: str = name
        self.age: int = age
        Student.count += 1  # 修改类属性
```

And similarly for all other code examples.

- [ ] **Step 3: Add type hints to method signatures**

```python
class Student:
    count: int = 0

    def __init__(self, name: str) -> None:
        self.name: str = name
        Student.count += 1

    def introduce(self) -> None:
        """实例方法"""
        print(f"我是{self.name}")

    @classmethod
    def get_count(cls) -> int:
        """类方法"""
        return cls.count

    @classmethod
    def from_string(cls, data_str: str) -> "Student":
        """类方法：工厂方法"""
        name = data_str.split(",")[0]
        return cls(name)

    @staticmethod
    def is_adult(age: int) -> bool:
        """静态方法"""
        return age >= 18
```

- [ ] **Step 4: Save and commit Task 2**

Commit message: `refactor(oop): add progressive teaching structure to 02-属性与方法.md`

---

## Task 3: Refactor 03-继承.md

**Files:**
- Modify: `/Users/baxiang/Documents/hello-python/02-核心编程篇/面向对象编程/03-继承.md`

- [ ] **Step 1: Add version requirement, problem scenario, and navigation**

```markdown
# 继承

> **Python 版本要求：** 3.11+

本章讲解 Python 面向对象编程中的继承机制，包括继承基础、super() 的使用和多重继承。

---

## 为什么需要继承？

### 问题场景

假设你要开发一个动物管理系统，有多种动物：
- 狗：有名字、会叫、会跑、会捡球
- 猫：有名字、会叫、会跑、会抓老鼠
- 鸟：有名字、会叫、会飞

**不使用继承：**

```python
class Dog:
    def __init__(self, name: str) -> None:
        self.name = name
    
    def speak(self) -> None:
        print(f"{self.name}：汪汪汪")
    
    def move(self) -> None:
        print(f"{self.name}在跑")
    
    def fetch(self) -> None:
        print(f"{self.name}在捡球")

class Cat:
    def __init__(self, name: str) -> None:
        self.name = name
    
    def speak(self) -> None:
        print(f"{self.name}：喵喵喵")
    
    def move(self) -> None:
        print(f"{self.name}在跑")
    
    def catch_mouse(self) -> None:
        print(f"{self.name}在抓老鼠")

# 问题：重复代码太多！
# 每个动物都有 name、speak()、move()
```

**问题：**
- 大量重复代码
- 修改共性需要在多个地方修改
- 难以统一管理

**使用继承：**

```python
class Animal:
    """动物基类"""
    def __init__(self, name: str) -> None:
        self.name = name
    
    def speak(self) -> None:
        print(f"{self.name}发出声音")
    
    def move(self) -> None:
        print(f"{self.name}在移动")

class Dog(Animal):
    """狗：继承自动物"""
    def speak(self) -> None:
        print(f"{self.name}：汪汪汪")
    
    def fetch(self) -> None:
        print(f"{self.name}在捡球")

class Cat(Animal):
    """猫：继承自动物"""
    def speak(self) -> None:
        print(f"{self.name}：喵喵喵")
    
    def catch_mouse(self) -> None:
        print(f"{self.name}在抓老鼠")

# 共性代码只在 Animal 中写一次
# 子类只关注自己的特性
```

---

## 章节导航

- 上一篇：[属性与方法](./02-属性与方法.md)
- 下一篇：[封装](./04-封装.md)
- 返回：[目录](../../README.md)

---

## 第一部分：继承基础

### 1.1 概念动机
```

- [ ] **Step 2: Add type annotations to all code examples**

```python
class Animal:
    def __init__(self, name: str) -> None:
        self.name: str = name

    def speak(self) -> None:
        print("动物在说话")

    def move(self) -> None:
        print("动物在移动")


class Dog(Animal):
    def __init__(self, name: str, breed: str) -> None:
        super().__init__(name)
        self.breed: str = breed

    def speak(self) -> None:
        print(f"{self.name} 在叫：汪汪汪！")

    def fetch(self) -> None:
        print(f"{self.name} 正在捡球")
```

- [ ] **Step 3: Update MRO example with type hints**

```python
class A:
    def method(self) -> None:
        print("A")

class B(A):
    def method(self) -> None:
        print("B")

class C(A):
    def method(self) -> None:
        print("C")

class D(B, C):
    pass
```

- [ ] **Step 4: Save and commit Task 3**

Commit message: `refactor(oop): add progressive teaching structure to 03-继承.md`

---

## Task 4: Refactor 04-封装.md

**Files:**
- Modify: `/Users/baxiang/Documents/hello-python/02-核心编程篇/面向对象编程/04-封装.md`

- [ ] **Step 1: Add version requirement, problem scenario, and navigation**

```markdown
# 封装

> **Python 版本要求：** 3.11+

本章讲解 Python 面向对象编程中的封装机制，包括私有属性、私有方法和 @property 装饰器。

---

## 为什么需要封装？

### 问题场景

假设你要开发一个银行账户系统：

**问题代码：**

```python
class BankAccount:
    def __init__(self, owner: str, balance: int) -> None:
        self.owner = owner
        self.balance = balance

account = BankAccount("张三", 1000)
# 问题：余额可以被随意修改！
account.balance = -100  # 余额变成负数！
account.balance = "abc"  # 类型错误！
```

**问题：**
- 数据可以被随意访问和修改
- 无法添加验证逻辑
- 无法保护数据完整性

**使用封装后：**

```python
class BankAccount:
    def __init__(self, owner: str, balance: int) -> None:
        self.owner = owner
        self.__balance = balance  # 私有属性
    
    def deposit(self, amount: int) -> bool:
        """存款"""
        if amount > 0:
            self.__balance += amount
            return True
        return False
    
    def withdraw(self, amount: int) -> bool:
        """取款"""
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            return True
        return False
    
    def get_balance(self) -> int:
        """查询余额"""
        return self.__balance

account = BankAccount("张三", 1000)
account.deposit(500)
# account.__balance = -100  # 错误！无法直接访问
```

---

## 章节导航

- 上一篇：[继承](./03-继承.md)
- 下一篇：[多态](./05-多态.md)
- 返回：[目录](../../README.md)

---

## 第一部分：什么是封装

### 1.1 概念动机
```

- [ ] **Step 2: Add type annotations to BankAccount example**

```python
class BankAccount:
    def __init__(self, owner: str, balance: int = 0) -> None:
        self.owner: str = owner
        self.__balance: int = balance
        self.__transaction_count: int = 0

    def deposit(self, amount: int) -> bool:
        """存款 - 公共接口"""
        if amount > 0:
            self.__balance += amount
            self.__transaction_count += 1
            print(f"存入{amount}，余额：{self.__balance}")
            return True
        print("存款金额必须大于 0")
        return False

    def withdraw(self, amount: int) -> bool:
        """取款 - 公共接口"""
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            self.__transaction_count += 1
            print(f"取出{amount}，余额：{self.__balance}")
            return True
        print("余额不足")
        return False

    def get_balance(self) -> int:
        """查询余额 - 公共接口"""
        return self.__balance

    def __validate_amount(self, amount: int) -> bool:
        """私有方法：验证金额"""
        return amount > 0
```

- [ ] **Step 3: Add type annotations to @property example**

```python
class Person:
    def __init__(self, age: int) -> None:
        self.__age: int = age

    @property
    def age(self) -> int:
        """getter 方法：获取 age"""
        return self.__age

    @age.setter
    def age(self, value: int) -> None:
        """setter 方法：设置 age"""
        if 0 < value < 150:
            self.__age = value
        else:
            raise ValueError("年龄必须在 0-150 之间")

    @property
    def age_group(self) -> str:
        """只读属性：年龄段"""
        if self.__age < 18:
            return "未成年"
        elif self.__age < 60:
            return "成年人"
        else:
            return "老年人"
```

- [ ] **Step 4: Save and commit Task 4**

Commit message: `refactor(oop): add progressive teaching structure to 04-封装.md`

---

## Task 5: Refactor 05-多态.md

**Files:**
- Modify: `/Users/baxiang/Documents/hello-python/02-核心编程篇/面向对象编程/05-多态.md`

- [ ] **Step 1: Add version requirement, problem scenario, and navigation**

```markdown
# 多态

> **Python 版本要求：** 3.11+

本章讲解 Python 面向对象编程中的多态机制，包括多态基础、鸭子类型和抽象基类。

---

## 为什么需要多态？

### 问题场景

假设你要开发一个游戏，有不同类型的角色，每个角色都能攻击：

**不使用多态：**

```python
class Warrior:
    def attack(self) -> str:
        return "战士挥剑"

class Mage:
    def attack(self) -> str:
        return "法师施法"

class Archer:
    def attack(self) -> str:
        return "弓箭手射箭"

def perform_attack(character: str, character_type: str) -> None:
    """需要判断类型，很繁琐"""
    if character_type == "warrior":
        print("战士挥剑")
    elif character_type == "mage":
        print("法师施法")
    elif character_type == "archer":
        print("弓箭手射箭")

# 问题：
# 1. 每次添加新角色都要修改 perform_attack
# 2. 代码重复，难以维护
```

**使用多态：**

```python
class Character:
    def attack(self) -> str:
        raise NotImplementedError

class Warrior(Character):
    def attack(self) -> str:
        return "战士挥剑"

class Mage(Character):
    def attack(self) -> str:
        return "法师施法"

class Archer(Character):
    def attack(self) -> str:
        return "弓箭手射箭"

def perform_attack(character: Character) -> None:
    """统一接口，自动调用正确的方法"""
    print(character.attack())

# 添加新角色无需修改 perform_attack
characters = [Warrior(), Mage(), Archer()]
for c in characters:
    perform_attack(c)
```

**优势：**
- 统一接口，简化代码
- 易于扩展新类型
- 降低耦合度

---

## 章节导航

- 上一篇：[封装](./04-封装.md)
- 下一篇：[设计原则](./06-设计原则.md)
- 返回：[目录](../../README.md)

---

## 第一部分：什么是多态

### 1.1 概念动机
```

- [ ] **Step 2: Add type annotations to Animal example**

```python
from typing import List

class Animal:
    """动物基类"""
    def speak(self) -> str:
        raise NotImplementedError("子类必须实现此方法")

class Dog(Animal):
    def speak(self) -> str:
        return "汪汪汪"

class Cat(Animal):
    def speak(self) -> str:
        return "喵喵喵"

class Duck(Animal):
    def speak(self) -> str:
        return "嘎嘎嘎"


def make_animal_speak(animal: Animal) -> None:
    """让动物叫（不关心具体类型）"""
    print(f"{type(animal).__name__}: {animal.speak()}")

# 创建不同的动物
animals: List[Animal] = [Dog(), Cat(), Duck()]

# 统一处理
for animal in animals:
    make_animal_speak(animal)
```

- [ ] **Step 3: Add type annotations to duck typing and ABC examples**

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    """抽象基类：定义所有形状必须实现的方法"""

    @abstractmethod
    def get_area(self) -> float:
        """计算面积 - 子类必须实现"""
        pass

    @abstractmethod
    def get_perimeter(self) -> float:
        """计算周长 - 子类必须实现"""
        pass


class Rectangle(Shape):
    def __init__(self, width: float, height: float) -> None:
        self.width: float = width
        self.height: float = height

    def get_area(self) -> float:
        return self.width * self.height

    def get_perimeter(self) -> float:
        return 2 * (self.width + self.height)


class Circle(Shape):
    def __init__(self, radius: float) -> None:
        self.radius: float = radius

    def get_area(self) -> float:
        return 3.14 * self.radius ** 2

    def get_perimeter(self) -> float:
        return 2 * 3.14 * self.radius
```

- [ ] **Step 4: Save and commit Task 5**

Commit message: `refactor(oop): add progressive teaching structure to 05-多态.md`

---

## Task 6: Refactor 06-设计原则.md

**Files:**
- Modify: `/Users/baxiang/Documents/hello-python/02-核心编程篇/面向对象编程/06-设计原则.md`

- [ ] **Step 1: Add version requirement, problem scenario, and navigation**

```markdown
# 设计原则

> **Python 版本要求：** 3.11+

本章讲解面向对象设计的基本原则，包括组合与继承的选择和最佳实践。

---

## 为什么需要设计原则？

### 问题场景

假设你要开发一个游戏角色系统：

**糟糕的设计（过度继承）：**

```python
class Character:
    def move(self) -> None: pass
    def attack(self) -> None: pass

class FlyingCharacter(Character):
    def fly(self) -> None: pass

class SwimmingCharacter(Character):
    def swim(self) -> None: pass

# 问题：如何创建既会飞又会游泳的角色？
# 需要创建 FlyingSwimmingCharacter
# 继承层次越来越复杂，呈指数增长
```

**问题：**
- 继承层次过深，难以维护
- 组合爆炸（FlyingSwimmingCharacter, FlyingRunningCharacter...）
- 修改父类影响所有子类
- 代码复用困难

**更好的设计（使用组合）：**

```python
class FlyBehavior:
    def fly(self) -> str:
        return "在空中飞翔"

class SwimBehavior:
    def swim(self) -> str:
        return "在水中游泳"

class Character:
    def __init__(self, name: str) -> None:
        self.name = name
        self.fly_behavior: FlyBehavior | None = None
        self.swim_behavior: SwimBehavior | None = None
    
    def set_fly(self, fly: FlyBehavior) -> None:
        self.fly_behavior = fly
    
    def set_swim(self, swim: SwimBehavior) -> None:
        self.swim_behavior = swim

# 灵活组合，无需创建大量子类
duck = Character("鸭子")
duck.set_fly(FlyBehavior())
duck.set_swim(SwimBehavior())
```

**优势：**
- 灵活组合行为
- 易于扩展新行为
- 降低耦合度

---

## 章节导航

- 上一篇：[多态](./05-多态.md)
- 返回：[目录](../../README.md)

---

## 第一部分：组合 vs 继承

### 1.1 概念动机
```

- [ ] **Step 2: Add type annotations to all examples**

```python
class Engine:
    """发动机类"""
    def start(self) -> str:
        return "发动机启动"

class Wheel:
    """轮子类"""
    def rotate(self) -> str:
        return "轮子转动"

class Car:
    """汽车类 - 使用组合"""
    def __init__(self, brand: str) -> None:
        self.brand: str = brand
        # 组合：汽车"有"发动机和轮子
        self.engine: Engine = Engine()
        self.wheels: list[Wheel] = [Wheel() for _ in range(4)]

    def drive(self) -> str:
        result = [f"{self.brand} 汽车："]
        result.append(self.engine.start())
        for wheel in self.wheels:
            result.append(wheel.rotate())
        return "\n".join(result)
```

- [ ] **Step 3: Add type annotations to SOLID example**

```python
# ✅ 遵循单一职责：每个类只做一件事
class User:
    def __init__(self, name: str, email: str) -> None:
        self.name: str = name
        self.email: str = email

class UserRepository:
    def save(self, user: User) -> None:
        # 保存到数据库
        pass

class EmailService:
    def send(self, user: User, message: str) -> None:
        # 发送邮件
        pass

class ReportGenerator:
    def generate(self, user: User) -> str:
        # 生成报告
        return ""
```

- [ ] **Step 4: Save and commit Task 6**

Commit message: `refactor(oop): add progressive teaching structure to 06-设计原则.md`

---

## Task 7: Final Commit

- [ ] **Step 1: Create final commit**

After all 6 files are updated, create a summary commit:

```bash
git add .
git commit -m "Refactor OOP directory with progressive teaching method

- Add Python 3.11+ version requirement to all documents
- Add problem-driven introduction ('为什么需要...？')
- Apply 6-step progressive teaching structure
- Add type annotations to all code examples
- Add chapter navigation links
- Preserve existing detailed content and ASCII diagrams"
```

---

## Self-Review Checklist

After completing all tasks:

1. **Spec coverage:**
   - [ ] Python 3.11+ version requirement added to all 6 files
   - [ ] Problem scenario introduction added to all 6 files
   - [ ] 6-step teaching structure applied to all 6 files
   - [ ] Type annotations added to all code examples
   - [ ] Chapter navigation links added to all 6 files
   - [ ] Existing content and ASCII diagrams preserved

2. **Placeholder scan:**
   - [ ] No "TODO", "TBD", or placeholder text in code blocks
   - [ ] All code examples are complete and runnable

3. **Type consistency:**
   - [ ] Type hints use Python 3.11+ syntax (e.g., `list[str]` not `List[str]`)
   - [ ] Return types specified for all functions
   - [ ] Class attribute types specified

---

**Plan complete.** Two execution options:

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?**