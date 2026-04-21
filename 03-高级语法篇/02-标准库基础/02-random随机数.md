# random 随机数

> Python 3.11+

---

## 为什么需要 random 模块？

### 问题场景

你需要开发一个抽奖系统，从参与者列表中随机选出 3 名获奖者：

```python
# ❌ 自己实现随机逻辑：分布不均匀，无法复现
index = hash(str(time.time())) % len(participants)

# ✅ 用 random 模块：均匀分布，可用 seed 复现
import random
random.seed(42)                              # 固定种子，测试可复现
winners = random.sample(participants, k=3)  # 不重复随机抽取

# 安全令牌场景（用 secrets 而非 random）
import secrets
token = secrets.token_urlsafe(16)           # 密码学安全的随机字符串
```

`random` 模块适合模拟、测试、游戏等非安全场景；涉及密码和令牌时改用 `secrets`。

---

## 章节导航

| 部分 | 内容 |
|------|------|
| 第一部分 | 随机整数、随机浮点数 |
| 第二部分 | 随机选择、打乱顺序 |
| 第三部分 | 随机分布（均匀/正态/其他） |
| 第四部分 | 随机种子与可复现性 |
| 第五部分 | 实际应用（密码/抽奖/颜色/骰子） |
| 第六部分 | 安全随机数（secrets 模块） |
| L2 实践层 | 推荐做法、反模式、常见陷阱、适用场景 |

---

## 第一部分：基本随机数生成

### 1.1 随机整数

#### 实际场景

在游戏开发、模拟测试、数据采样等场景中，经常需要生成随机整数。比如掷骰子、生成测试数据、随机抽样等。

**问题：`randint()` 和 `randrange()` 有什么区别？如何生成指定范围内的随机整数？**

```python
import random

# 随机整数 [a, b]
rand_int: int = random.randint(1, 10)    # 1 到 10 之间的整数

# 随机整数 [a, b)，步长为 step
rand_range_step: int = random.randrange(1, 10, 2)  # 1, 3, 5, 7, 9 中的一个

# 随机整数 [a, b)
rand_range: int = random.randrange(10)     # 0 到 9 之间的整数
```

### 1.2 随机浮点数

#### 实际场景

在科学计算、概率模拟、蒙特卡洛方法中，需要生成随机浮点数。比如模拟物理过程、生成随机概率等。

**问题：`random()` 和 `uniform()` 有什么区别？如何生成指定范围的随机浮点数？**

```python
import random

# 随机浮点数 [0, 1)
rand_float: float = random.random()          # 0.0 到 1.0 之间

# 随机浮点数 [a, b]
rand_uniform: float = random.uniform(1.0, 10.0)  # 1.0 到 10.0 之间
```

## 第二部分：序列操作

### 2.1 随机选择

#### 实际场景

在抽奖系统、随机推荐、A/B 测试等场景中，需要从列表中随机选择元素。比如抽奖程序、随机展示广告、随机选择测试用例等。

**问题：`choice()`、`choices()` 和 `sample()` 有什么区别？**

```python
import random

items: list[str] = ['苹果', '香蕉', '橙子', '葡萄', '西瓜']

# 随机选择一个元素
one_item: str = random.choice(items)     # 随机一个水果

# 随机选择多个元素（可重复）
multi_items: list[str] = random.choices(items, k=3)  # 随机 3 个，可能重复

# 随机选择多个元素（不重复）
unique_items: list[str] = random.sample(items, k=3)   # 随机 3 个，不重复
```

### 2.2 打乱顺序

#### 实际场景

在洗牌游戏、随机排序、数据增强等场景中，需要随机打乱序列顺序。比如扑克牌游戏、随机展示列表项等。

**问题：如何原地打乱列表顺序？打乱后可以恢复吗？**

```python
import random

items: list[int] = [1, 2, 3, 4, 5]

# 原地打乱
random.shuffle(items)
print(items)  # [3, 1, 5, 2, 4]（随机顺序）
```

## 第三部分：随机分布

### 3.1 均匀分布

#### 实际场景

在蒙特卡洛模拟、随机采样中，经常需要均匀分布的随机数。

```python
import random

# 均匀分布 [a, b]
values: list[float] = [random.uniform(0, 1) for _ in range(5)]
print(values)  # [0.23, 0.87, 0.45, 0.12, 0.67]
```

### 3.2 正态分布

#### 实际场景

在统计模拟、自然现象模拟、金融建模中，正态分布（高斯分布）是最常见的分布。比如模拟身高分布、股票价格波动等。

**问题：如何生成符合正态分布的随机数？`gauss()` 和 `normalvariate()` 有什么区别？**

```python
import random

# 正态分布（高斯分布）
# mu: 均值, sigma: 标准差
values: list[float] = [random.gauss(0, 1) for _ in range(5)]
print(values)  # 接近标准正态分布

# 另一种写法
values_alt: list[float] = [random.normalvariate(0, 1) for _ in range(5)]
```

### 3.3 其他分布

#### 实际场景

在特定领域的模拟中，需要其他类型的概率分布。比如指数分布用于模拟等待时间，Beta 分布用于贝叶斯统计等。

```python
import random

# 指数分布
exp_value: float = random.expovariate(1.0)

# 三角分布
tri_value: float = random.triangular(0, 1, 0.5)  # low, high, mode

# Beta 分布
beta_value: float = random.betavariate(2, 5)

# Gamma 分布
gamma_value: float = random.gammavariate(1, 1)
```

## 第四部分：随机种子与可复现性

### 4.1 设置随机种子

#### 实际场景

在测试、调试、科学实验中，需要保证随机数的可复现性。设置相同的种子可以保证每次运行生成相同的随机序列。

**问题：为什么要设置随机种子？什么时候需要设置？**

```python
import random

# 设置随机种子，确保可复现
random.seed(42)
val1: float = random.random()  # 0.6394267984578837

random.seed(42)
val2: float = random.random()  # 0.6394267984578837（相同结果）
```

## 第五部分：实际应用示例

### 5.1 生成随机密码

#### 实际场景

在用户注册、密码重置、系统初始化等场景中，需要生成随机密码或密钥。

```python
import random
import string

def generate_password(length: int = 12) -> str:
    """生成随机密码"""
    chars: str = string.ascii_letters + string.digits + '!@#$%^&*'
    return ''.join(random.choices(chars, k=length))

password: str = generate_password(16)
print(password)  # xK9#mP2@nL5$qR8!
```

### 5.2 抽奖程序

#### 实际场景

在活动抽奖、随机选人等场景中，需要从参与者中随机选择获奖者。

```python
import random

def lottery(participants: list[str], winners_count: int) -> list[str]:
    """抽奖程序"""
    winners: list[str] = random.sample(participants, winners_count)
    return winners

participants: list[str] = ['张三', '李四', '王五', '赵六', '钱七', '孙八']
winners: list[str] = lottery(participants, 2)
print(f"中奖者: {winners}")
```

### 5.3 随机颜色生成

#### 实际场景

在数据可视化、图形设计、游戏开发中，需要生成随机颜色。

```python
import random

def random_color() -> str:
    """生成随机十六进制颜色"""
    return f'#{random.randint(0, 0xFFFFFF):06x}'

colors: list[str] = [random_color() for _ in range(5)]
for color in colors:
    print(color)  # #a3f2c1, #8b4d2e, ...
```

### 5.4 模拟掷骰子

#### 实际场景

在游戏开发、概率教学、统计模拟中，需要模拟骰子投掷。

```python
import random

def roll_dice(count: int = 1) -> list[int]:
    """掷骰子"""
    return [random.randint(1, 6) for _ in range(count)]

result1: list[int] = roll_dice(2)  # [3, 5]
result2: list[int] = roll_dice(3)  # [1, 6, 2]
```

### 5.5 模拟抛硬币

#### 实际场景

在概率教学、统计模拟中，需要模拟抛硬币实验。

```python
import random

def flip_coin() -> str:
    """抛硬币"""
    return random.choice(['正面', '反面'])

results: list[str] = [flip_coin() for _ in range(10)]
print(results)  # ['正面', '反面', '正面', ...]
```

## 第六部分：安全随机数

### 6.1 使用 secrets 模块

#### 实际场景

在生成安全令牌、API 密钥、会话 ID 等安全敏感场景中，不应使用 `random` 模块，而应使用 `secrets` 模块，因为它生成的是加密安全的随机数。

**问题：为什么安全敏感场景要使用 `secrets` 而不是 `random`？**

```python
import secrets

# 安全随机整数
secure_int: int = secrets.randbelow(1000000)

# 安全随机字节
key: bytes = secrets.token_bytes(16)

# 安全随机 URL 安全字符串
token_url: str = secrets.token_urlsafe(16)

# 安全随机十六进制字符串
token_hex: str = secrets.token_hex(16)
```

---

## L2 实践层：最佳实践

### 推荐做法

| 做法 | 原因 | 示例 |
|------|------|------|
| 安全场景用 `secrets` 而非 `random` | `random` 基于伪随机算法，可被预测 | `secrets.token_urlsafe(16)` |
| 测试时固定 `random.seed()` | 保证测试可复现，排查问题方便 | `random.seed(42)` |
| 不重复抽样用 `sample()`，可重复用 `choices()` | 二者语义不同，混用导致逻辑错误 | `random.sample(lst, k=3)` |
| 带权重抽样用 `choices(weights=...)` | 模拟概率不等的抽奖、A/B 测试 | `random.choices(lst, weights=[60,30,10])` |
| 生产代码避免在模块顶层调用 `random.seed()` | 会影响整个程序的随机状态 | 测试中局部设置 |

### 实际应用示例

```python
import random
import string
import secrets

# 带权重的抽奖（一等奖 10%，二等奖 30%，三等奖 60%）
prizes = ["一等奖", "二等奖", "三等奖"]
result = random.choices(prizes, weights=[10, 30, 60], k=1)[0]

# 生成安全 API token
api_token: str = secrets.token_urlsafe(32)

# 可复现的随机测试数据
rng = random.Random(42)        # 使用独立的 Random 实例，不影响全局状态
test_data = [rng.randint(1, 100) for _ in range(10)]
```

### 反模式：不要这样做

```python
# ❌ 密码/令牌用 random
import random
password = ''.join(random.choices('abcdef0123456789', k=32))  # 不安全！

# ✅ 用 secrets
import secrets
token = secrets.token_hex(16)

# ❌ 混淆 sample 和 choices
import random
items = [1, 2, 3]
# sample 要求 k <= len(items)
random.sample(items, k=5)   # ValueError，元素不够

# ✅ 可重复时用 choices
random.choices(items, k=5)  # 允许重复，[2, 1, 3, 2, 1]

# ❌ 在模块顶层设置 seed（影响全局随机状态）
import random
random.seed(42)              # 会让所有依赖 random 的代码都变成伪随机
```

### 常见陷阱

| 陷阱 | 现象 | 解决方案 |
|------|------|---------|
| `random.sample(lst, k>len(lst))` | `ValueError` | 确认 `k <= len(lst)`，或改用 `choices` |
| 未设种子的测试 | 每次运行结果不同，难以复现 bug | 测试前 `random.seed(固定值)` |
| 用 `random` 生成密码 | 伪随机，可被预测 | 改用 `secrets` 模块 |
| `shuffle` 修改原列表 | 原始数据丢失 | 先 `copy = lst[:]`，再 `shuffle(copy)` |
| 全局 seed 污染 | 一处设了 seed，影响其他模块随机行为 | 用 `random.Random(seed)` 创建独立实例 |

### 适用场景

| 场景 | 推荐模块 | 说明 |
|------|---------|------|
| 游戏、模拟、测试数据 | `random` | 性能好，可复现 |
| 统计分布模拟 | `random` | 内置正态、指数等分布 |
| 密码、令牌、会话 ID | `secrets` | 密码学安全 |
| 大规模数值模拟 | `numpy.random` | 批量生成，速度快 100 倍 |

---

## 本章小结

```
┌──────────────────────────────────────────────────────────────┐
│                  random 模块 知识要点                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   随机整数：randint(a,b)  randrange(a,b,step)                │
│   随机浮点：random()  uniform(a,b)                           │
│                                                              │
│   序列操作：                                                 │
│   choice(seq)         随机选 1 个                            │
│   choices(seq,k=N)    可重复选 N 个（支持 weights）          │
│   sample(seq,k=N)     不重复选 N 个                          │
│   shuffle(seq)        原地打乱                               │
│                                                              │
│   分布：gauss(mu,sigma)  normalvariate  uniform  expovariate │
│   种子：seed(n) 固定状态，测试可复现                         │
│                                                              │
│   安全场景必须用 secrets：                                   │
│   token_urlsafe()  token_hex()  token_bytes()  randbelow()   │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```