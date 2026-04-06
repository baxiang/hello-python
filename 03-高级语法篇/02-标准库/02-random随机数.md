# random 模块参考（详细版）

> Python 3.11+

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