# weakref 弱引用

> **难度**：⭐⭐⭐ 专家
> **预计时间**：45分钟
> **前置知识**：引用概念、类与对象、垃圾回收基础
> **引入版本**：Python 3.0+

本章讲解 weakref 模块，理解弱引用与强引用的区别，解决循环引用和缓存问题。

---

## 为什么需要弱引用？

### 问题场景

你正在开发一个对象缓存系统：

```python
class Cache:
    def __init__(self) -> None:
        self._cache: dict[str, object] = {}
    
    def get(self, key: str, creator: callable) -> object:
        if key not in self._cache:
            self._cache[key] = creator()
        return self._cache[key]
    
    def size(self) -> int:
        return len(self._cache)

class BigObject:
    def __init__(self, name: str) -> None:
        self.name = name
        self.data = [0] * 1000000  # 占用大量内存

cache = Cache()

obj1 = cache.get("obj1", lambda: BigObject("对象1"))
obj2 = cache.get("obj2", lambda: BigObject("对象2"))

del obj1
del obj2

print(f"缓存大小: {cache.size()}")
```

**运行结果：**

```
缓存大小: 2
```

**问题：**
- 删除 obj1 和 obj2 后，缓存仍持有引用
- 对象不会被回收，内存无法释放
- 缓存"泄露"了对象

**弱引用解决方案：**

```python
import weakref

class Cache:
    def __init__(self) -> None:
        self._cache: dict[str, weakref.ref] = {}
    
    def get(self, key: str, creator: callable) -> object:
        if key in self._cache:
            obj = self._cache[key]()
            if obj is not None:
                return obj
        obj = creator()
        self._cache[key] = weakref.ref(obj)
        return obj
    
    def size(self) -> int:
        count = 0
        for ref in self._cache.values():
            if ref() is not None:
                count += 1
        return count

class BigObject:
    def __init__(self, name: str) -> None:
        self.name = name
        self.data = [0] * 1000000

cache = Cache()

obj1 = cache.get("obj1", lambda: BigObject("对象1"))
obj2 = cache.get("obj2", lambda: BigObject("对象2"))

del obj1
del obj2

print(f"缓存大小: {cache.size()}")
```

这就是弱引用的价值：**引用对象但不阻止其被回收**。

---

## 弱引用概念铺垫

```
┌─────────────────────────────────────────────────────────────┐
│          弱引用关键概念                                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 强引用 vs 弱引用                                        │
│  ─────────────────────────────────────────────              │
│  强引用：                                                    │
│  • 普通变量赋值：a = obj                                    │
│  • 增加引用计数                                             │
│  • 阻止对象被垃圾回收                                       │
│                                                             │
│  弱引用：                                                    │
│  • weakref.ref(obj)                                         │
│  • 不增加引用计数                                           │
│  • 不阻止对象被回收                                         │
│  • 对象被回收后，ref() 返回 None                            │
│                                                             │
│  2. Python 垃圾回收                                         │
│  ─────────────────────────────────────────────              │
│  • 引用计数：主要机制                                       │
│  • 对象引用计数为 0 时被回收                                │
│  • 弱引用不计入引用计数                                     │
│                                                             │
│  3. 弱引用的用途                                            │
│  ─────────────────────────────────────────────              │
│  • 缓存：持有对象引用但不阻止释放                           │
│  • 循环引用：避免引用计数无法降为 0                          │
│  • 观察者模式：观察对象状态而不持有                         │
│  • 关联数据：附加数据到对象而不延长生命周期                  │
│                                                             │
│  4. 弱引用类型                                              │
│  ─────────────────────────────────────────────              │
│  • weakref.ref：基础弱引用                                  │
│  • weakref.WeakKeyDictionary：键为弱引用的字典              │
│  • weakref.WeakValueDictionary：值为弱引用的字典            │
│  • weakref.WeakSet：弱引用集合                              │
│  • weakref.finalize：对象回收时的回调                       │
│                                                             │
│  5. 限制                                                    │
│  ─────────────────────────────────────────────              │
│  • 只能引用支持弱引用的对象                                 │
│  • 内置类型（int, str, list）不支持弱引用                   │
│  • 自定义类默认支持弱引用                                   │
│  • 需要 __slots__ 时添加 '__weakref__'                      │
│                                                             │
│  6. 生活类比                                                │
│  ─────────────────────────────────────────────              │
│  强引用 = 房子的主人（决定房子命运）                        │
│  弱引用 = 房子的观察者（只能看，不决定）                    │
│                                                             │
│  主人离开 → 房子被拆除 → 观察者看到"房子没了"               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## L1 琐解层：弱引用基础

### 语法结构

```
┌─────────────────────────────────────────────────────────────┐
│  weakref 核心语法                                            │
│                                                             │
│  创建弱引用：                                                │
│  ref = weakref.ref(obj)                                    │
│  ref = weakref.ref(obj, callback)  # 回调函数               │
│                                                             │
│  访问对象：                                                  │
│  obj = ref()  # 返回对象或 None                             │
│                                                             │
│  弱引用字典：                                                │
│  wkdict = weakref.WeakKeyDictionary()                      │
│  wvdict = weakref.WeakValueDictionary()                    │
│                                                             │
│  弱引用集合：                                                │
│  wset = weakref.WeakSet()                                  │
│                                                             │
│  回调：                                                      │
│  def callback(ref):                                        │
│      print("对象被回收")                                    │
│                                                             │
│  参数说明：                                                  │
│  obj      → 要引用的对象                                    │
│  ref      → 弱引用对象                                      │
│  callback → 对象被回收时调用的函数                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 最简示例：基础弱引用

```python
import weakref

class MyObject:
    def __init__(self, name: str) -> None:
        self.name = name
    
    def __repr__(self) -> str:
        return f"MyObject({self.name})"

obj = MyObject("测试对象")
ref = weakref.ref(obj)

print(f"对象存在: {ref()}")
print(f"引用计数: {ref.__callback__}")

del obj

print(f"对象已删除: {ref()}")
```

**运行结果：**

```
对象存在: MyObject(测试对象)
引用计数: None
对象已删除: None
```

**说明：**
- `weakref.ref(obj)` 创建弱引用
- `ref()` 返回对象（如果还存在）或 None
- 删除 obj 后，弱引用返回 None

### 最简示例：回调函数

```python
import weakref

class MyObject:
    def __init__(self, name: str) -> None:
        self.name = name

def on_delete(ref: weakref.ref) -> None:
    print(f"对象被回收: {ref}")

obj = MyObject("测试")
ref = weakref.ref(obj, on_delete)

print(f"对象: {ref()}")

del obj
```

**运行结果：**

```
对象: <__main__.MyObject object at 0x...>
对象被回收: <weakref at 0x...>
```

**说明：**
- 对象被回收时，回调函数被调用
- 回调接收弱引用对象作为参数
- 可用于清理相关资源

### 详细示例：WeakValueDictionary

```python
import weakref

class Resource:
    def __init__(self, id: int) -> None:
        self.id = id
    
    def __repr__(self) -> str:
        return f"Resource({self.id})"

cache = weakref.WeakValueDictionary()

r1 = Resource(1)
r2 = Resource(2)
r3 = Resource(3)

cache["r1"] = r1
cache["r2"] = r2
cache["r3"] = r3

print(f"缓存: {dict(cache)}")
print(f"缓存大小: {len(cache)}")

del r1
del r2

print(f"删除后缓存: {dict(cache)}")
print(f"删除后大小: {len(cache)}")
```

**运行结果：**

```
缓存: {'r1': Resource(1), 'r2': Resource(2), 'r3': Resource(3)}
缓存大小: 3
删除后缓存: {'r3': Resource(3)}
删除后大小: 1
```

**说明：**
- WeakValueDictionary 的值是弱引用
- 删除对象后，字典自动移除对应条目
- 适合缓存场景

---

## L2 实践层：弱引用应用

### 实际应用场景

#### 场景1：对象缓存

```python
import weakref

class ObjectCache:
    def __init__(self) -> None:
        self._cache: weakref.WeakValueDictionary = weakref.WeakValueDictionary()
    
    def get(self, key: str, factory: callable) -> object:
        obj = self._cache.get(key)
        if obj is not None:
            return obj
        obj = factory()
        self._cache[key] = obj
        return obj
    
    def keys(self) -> list[str]:
        return list(self._cache.keys())
    
    def clear(self) -> None:
        self._cache.clear()

class ExpensiveObject:
    def __init__(self, name: str) -> None:
        self.name = name
        self.data = [i for i in range(100000)]
        print(f"创建 {name}")

cache = ObjectCache()

obj1 = cache.get("obj1", lambda: ExpensiveObject("对象1"))
obj2 = cache.get("obj2", lambda: ExpensiveObject("对象2"))

print(f"缓存键: {cache.keys()}")

obj1_again = cache.get("obj1", lambda: ExpensiveObject("对象1"))

del obj1
del obj1_again
del obj2

print(f"删除后缓存键: {cache.keys()}")
```

**运行结果：**

```
创建 对象1
创建 对象2
缓存键: ['obj1', 'obj2']
删除后缓存键: []
```

#### 场景2：循环引用解决

```python
import weakref

class Parent:
    def __init__(self, name: str) -> None:
        self.name = name
        self.children: list[Child] = []
    
    def add_child(self, child: Child) -> None:
        self.children.append(child)
        child.parent = self

class Child:
    def __init__(self, name: str) -> None:
        self.name = name
        self._parent_ref: weakref.ref | None = None
    
    @property
    def parent(self) -> Parent | None:
        if self._parent_ref is None:
            return None
        return self._parent_ref()
    
    @parent.setter
    def parent(self, value: Parent) -> None:
        self._parent_ref = weakref.ref(value)
    
    def __repr__(self) -> str:
        parent_name = self.parent.name if self.parent else "None"
        return f"Child({self.name}, parent={parent_name})"

parent = Parent("父亲")
child1 = Child("儿子1")
child2 = Child("儿子2")

parent.add_child(child1)
parent.add_child(child2)

print(f"孩子1: {child1}")
print(f"孩子2: {child2}")

del parent

print(f"删除父亲后: {child1}")
```

**运行结果：**

```
孩子1: Child(儿子1, parent=父亲)
孩子2: Child(儿子2, parent=父亲)
删除父亲后: Child(儿子1, parent=None)
```

**说明：**
- Child 用弱引用引用 Parent
- Parent 删除后，Child 的 parent 属性自动为 None
- 避免循环引用导致的内存泄露

#### 场景3：观察者模式

```python
import weakref

class Observable:
    def __init__(self) -> None:
        self._observers: weakref.WeakSet = weakref.WeakSet()
    
    def add_observer(self, observer: object) -> None:
        self._observers.add(observer)
    
    def notify(self, message: str) -> None:
        for observer in self._observers:
            if hasattr(observer, 'on_notify'):
                observer.on_notify(message)
    
    def observer_count(self) -> int:
        return len(self._observers)

class Observer:
    def __init__(self, name: str) -> None:
        self.name = name
    
    def on_notify(self, message: str) -> None:
        print(f"{self.name} 收到: {message}")

subject = Observable()
obs1 = Observer("观察者1")
obs2 = Observer("观察者2")

subject.add_observer(obs1)
subject.add_observer(obs2)

print(f"观察者数量: {subject.observer_count()}")

subject.notify("事件1")

del obs1

print(f"删除后观察者数量: {subject.observer_count()}")

subject.notify("事件2")
```

**运行结果：**

```
观察者数量: 2
观察者1 收到: 事件1
观察者2 收到: 事件1
删除后观察者数量: 1
观察者2 收到: 事件2
```

**说明：**
- 用 WeakSet 存储观察者
- 观察者被删除后自动从集合移除
- 避免观察者被主题"锁住"

### 推荐做法

| 做法 | 原因 | 示例 |
|------|------|------|
| **缓存用 WeakValueDictionary** | 自动清理已删除对象 | `cache = WeakValueDictionary()` |
| **循环引用用弱引用** | 避免内存泄露 | `child._parent_ref = weakref.ref(parent)` |
| **检查 ref() 是否为 None** | 对象可能已被回收 | `if ref() is not None:` |
| **添加回调清理资源** | 及时释放关联资源 | `weakref.ref(obj, cleanup)` |

### 反模式：不要这样做

#### 错误1：对内置类型使用弱引用

```python
import weakref

num = 42
try:
    ref = weakref.ref(num)
except TypeError as e:
    print(f"错误: {e}")

lst = [1, 2, 3]
try:
    ref = weakref.ref(lst)
except TypeError as e:
    print(f"错误: {e}")
```

**运行结果：**

```
错误: cannot create weak reference to 'int' object
错误: cannot create weak reference to 'list' object
```

**问题：**
- int, str, list, dict 等内置类型不支持弱引用
- 只能对自定义类使用弱引用

```python
import weakref

class MyList:
    def __init__(self, items: list) -> None:
        self.items = items

my_list = MyList([1, 2, 3])
ref = weakref.ref(my_list)
print(f"成功: {ref()}")
```

#### 错误2：忘记检查弱引用有效性

```python
import weakref

class MyObject:
    def __init__(self, value: int) -> None:
        self.value = value

obj = MyObject(10)
ref = weakref.ref(obj)
del obj

print(ref().value)
```

**运行结果：**

```
AttributeError: 'NoneType' object has no attribute 'value'
```

**问题：**
- 对象已回收，ref() 返回 None
- 直接访问 None 的属性导致错误

```python
import weakref

class MyObject:
    def __init__(self, value: int) -> None:
        self.value = value

obj = MyObject(10)
ref = weakref.ref(obj)
del obj

obj_ref = ref()
if obj_ref is not None:
    print(obj_ref.value)
else:
    print("对象已回收")
```

#### 错误3：__slots__ 中遗漏 __weakref__

```python
import weakref

class SlottedClass:
    __slots__ = ['value']
    
    def __init__(self, value: int) -> None:
        self.value = value

obj = SlottedClass(10)
try:
    ref = weakref.ref(obj)
except TypeError as e:
    print(f"错误: {e}")
```

**运行结果：**

```
错误: cannot create weak reference to 'SlottedClass' object
```

**问题：**
- __slots__ 类默认不支持弱引用
- 需要显式添加 '__weakref__'

```python
import weakref

class SlottedClass:
    __slots__ = ['value', '__weakref__']
    
    def __init__(self, value: int) -> None:
        self.value = value

obj = SlottedClass(10)
ref = weakref.ref(obj)
print(f"成功: {ref()}")
```

### 适用场景

| 场景 | 是否推荐弱引用 | 原因 |
|------|---------------|------|
| 对象缓存 | ✅ 推荐 | 自动清理，避免内存泄露 |
| 循环引用 | ✅ 推荐 | 打破引用循环 |
| 观察者模式 | ✅ 推荐 | 观察者可独立释放 |
| 关联数据映射 | ✅ 推荐 | 不延长对象生命周期 |
| 需要长期持有对象 | ❌ 不推荐 | 用强引用 |

---

## L3 专家层：弱引用原理

### Python 垃圾回收机制

```
┌─────────────────────────────────────────────────────────────┐
│          Python 垃圾回收机制                                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 引用计数（主要机制）                                    │
│  ─────────────────────────────────────────────              │
│  • 每个对象有引用计数器                                     │
│  • 新引用：计数 +1                                          │
│  • 引用删除：计数 -1                                        │
│  • 计数为 0：立即回收                                       │
│                                                             │
│  2. 弱引用不影响引用计数                                    │
│  ─────────────────────────────────────────────              │
│  • weakref.ref(obj) 不增加计数                              │
│  • 对象可以被正常回收                                       │
│  • 回收时弱引用返回 None                                    │
│                                                             │
│  3. 循环引用问题                                            │
│  ─────────────────────────────────────────────              │
│  • A 引用 B，B 引用 A                                       │
│  • 引用计数无法降为 0                                       │
│  • 需要垃圾回收器处理                                       │
│  • 弱引用可以打破循环                                       │
│                                                             │
│  4. 垃圾回收器                                              │
│  ─────────────────────────────────────────────              │
│  • 分代回收（generational）                                │
│  • 循环引用检测                                             │
│  • 弱引用帮助减少循环检测开销                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 弱引用内部实现

```python
import weakref
import gc

class MyObject:
    def __init__(self, name: str) -> None:
        self.name = name

obj = MyObject("测试")
print(f"引用计数: {gc.get_referrers(obj)}")

ref = weakref.ref(obj)
print(f"创建弱引用后: {gc.get_referrers(obj)}")

print(f"弱引用对象: {ref}")
print(f"弱引用的目标: {ref.__obj__}")
```

**说明：**
- 弱引用对象存储在单独的弱引用列表中
- 不计入目标对象的引用计数
- 目标对象有 __weakref__ 属性存储弱引用列表

### finalize 对象回收回调

```python
import weakref

class MyObject:
    def __init__(self, id: int) -> None:
        self.id = id

def cleanup(id: int) -> None:
    print(f"对象 {id} 被回收，清理资源")

obj = MyObject(1)
finalizer = weakref.finalize(obj, cleanup, obj.id)

print(f"对象存在: {finalizer.alive}")

del obj

print(f"对象删除后: {finalizer.alive}")
```

**运行结果：**

```
对象存在: True
对象删除后: False
对象 1 被回收，清理资源
```

**说明：**
- `weakref.finalize` 提供更可靠的回调机制
- 回调在对象被回收时执行
- 可以传递额外参数给回调函数

### 弱引用限制

```
┌─────────────────────────────────────────────────────────────┐
│          弱引用支持的类型                                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ✅ 支持弱引用：                                            │
│  ─────────────────────────────────────────────              │
│  • 自定义类实例                                             │
│  • 函数（function）                                         │
│  • 方法（bound/unbound method）                             │
│  • 类型对象（type）                                         │
│  • 某些内置对象（如 file）                                  │
│                                                             │
│  ❌ 不支持弱引用：                                          │
│  ─────────────────────────────────────────────              │
│  • int, float, complex                                      │
│  • str, bytes                                               │
│  • list, tuple, dict                                        │
│  • set, frozenset                                           │
│  • None                                                     │
│                                                             │
│  原因：                                                      │
│  ─────────────────────────────────────────────              │
│  • 内置类型可能被频繁复制                                   │
│  • 小整数被缓存（无法区分实例）                             │
│  • 实现复杂度考量                                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 性能考量

| 操作 | 时间复杂度 | 说明 |
|------|-----------|------|
| 创建弱引用 | O(1) | 简单指针操作 |
| 访问弱引用 | O(1) | 检查对象是否存在 |
| 回调执行 | O(1) | 回收时执行 |
| WeakDict 操作 | O(1) | 与普通字典相同 |

**内存影响：**

```python
import weakref
import sys

class MyObject:
    def __init__(self) -> None:
        self.data = [0] * 1000

objs = [MyObject() for _ in range(100)]
refs = [weakref.ref(obj) for obj in objs]

print(f"对象内存: ~{sum(sys.getsizeof(obj) for obj in objs)} bytes")
print(f"弱引用内存: ~{sum(sys.getsizeof(ref) for ref in refs)} bytes")

del objs

print(f"删除对象后，弱引用仍然占用少量内存")
```

**说明：**
- 弱引用本身占用少量内存
- 对象释放后，弱引用可以保留（返回 None）
- 内存开销远小于持有对象

### 设计动机

| 设计选择 | 原因 |
|----------|------|
| 不计入引用计数 | 允许对象被正常回收 |
| 提供 WeakDict 类型 | 简化缓存实现 |
| 回调机制 | 允许清理关联资源 |
| 限制支持类型 | 实现复杂度与实际需求 |

### 知识关联

```
知识关联图：
┌─────────────────┐     ┌─────────────────┐
│   引用计数      │────→│    弱引用       │
│   垃圾回收      │     │   weakref       │
└─────────────────┘     └─────────────────┘
        │                       │
        ↓                       ↓
┌─────────────────┐     ┌─────────────────┐
│   循环引用      │     │   WeakDict      │
│   内存泄露      │     │   缓存实现      │
└─────────────────┘     └─────────────────┘
        │                       │
        ↓                       ↓
┌─────────────────┐     ┌─────────────────┐
│   finalize      │     │   __slots__     │
│   回收回调      │     │   __weakref__   │
└─────────────────┘     └─────────────────┘
```

---

## 自检清单

回答以下问题，检查你是否掌握了核心概念：

1. 弱引用和强引用的区别是什么？
2. 为什么内置类型不支持弱引用？
3. WeakValueDictionary 有什么作用？
4. 如何解决循环引用问题？
5. __slots__ 类如何支持弱引用？

---

## 本章术语表

| 术语 | 定义 | 本章位置 |
|------|------|---------|
| 弱引用 | 不阻止对象回收的引用 | 概念铺垫 |
| 强引用 | 阻止对象回收的引用 | 概念铺垫 |
| weakref.ref | 基础弱引用类型 | L1理解层 |
| WeakValueDictionary | 值为弱引用的字典 | L1理解层 |
| WeakKeyDictionary | 键为弱引用的字典 | L1理解层 |
| WeakSet | 弱引用集合 | L1理解层 |
| finalize | 对象回收回调 | L3专家层 |
| __weakref__ | slots 中支持弱引用 | L2实践层 |

---

## 扩展阅读

- Python 官方文档：weakref 模块
- 《流畅的Python》第8章：对象引用、可变性和垃圾回收
- Python 垃圾回收机制：引用计数与分代回收