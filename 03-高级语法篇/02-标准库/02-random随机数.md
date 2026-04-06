# random 模块参考

Python random 模块提供随机数生成功能。

---

## 基本随机数

### 随机整数

```python
import random

# 随机整数 [a, b]
print(random.randint(1, 10))    # 1 到 10 之间的整数

# 随机整数 [a, b)，步长为 step
print(random.randrange(1, 10, 2))  # 1, 3, 5, 7, 9 中的一个

# 随机整数 [a, b)
print(random.randrange(10))     # 0 到 9 之间的整数
```

### 随机浮点数

```python
import random

# 随机浮点数 [0, 1)
print(random.random())          # 0.0 到 1.0 之间

# 随机浮点数 [a, b]
print(random.uniform(1.0, 10.0))  # 1.0 到 10.0 之间
```

---

## 序列操作

### 随机选择

```python
import random

items = ['苹果', '香蕉', '橙子', '葡萄', '西瓜']

# 随机选择一个元素
print(random.choice(items))     # 随机一个水果

# 随机选择多个元素（可重复）
print(random.choices(items, k=3))  # 随机 3 个，可能重复

# 随机选择多个元素（不重复）
print(random.sample(items, k=3))   # 随机 3 个，不重复
```

### 打乱顺序

```python
import random

items = [1, 2, 3, 4, 5]

# 原地打乱
random.shuffle(items)
print(items)  # [3, 1, 5, 2, 4]（随机顺序）
```

---

## 随机分布

### 均匀分布

```python
import random

# 均匀分布 [a, b]
values = [random.uniform(0, 1) for _ in range(5)]
print(values)  # [0.23, 0.87, 0.45, 0.12, 0.67]
```

### 正态分布

```python
import random

# 正态分布（高斯分布）
# mu: 均值, sigma: 标准差
values = [random.gauss(0, 1) for _ in range(5)]
print(values)  # 接近标准正态分布

# 另一种写法
values = [random.normalvariate(0, 1) for _ in range(5)]
```

### 其他分布

```python
import random

# 指数分布
value = random.expovariate(1.0)

# 三角分布
value = random.triangular(0, 1, 0.5)  # low, high, mode

# Beta 分布
value = random.betavariate(2, 5)

# Gamma 分布
value = random.gammavariate(1, 1)
```

---

## 随机种子

### 设置种子

```python
import random

# 设置随机种子，确保可复现
random.seed(42)
print(random.random())  # 0.6394267984578837

random.seed(42)
print(random.random())  # 0.6394267984578837（相同结果）
```

---

## 常用示例

### 生成随机密码

```python
import random
import string

def generate_password(length=12):
    """生成随机密码"""
    chars = string.ascii_letters + string.digits + '!@#$%^&*'
    return ''.join(random.choices(chars, k=length))

password = generate_password(16)
print(password)  # xK9#mP2@nL5$qR8!
```

### 抽奖程序

```python
import random

def lottery(participants, winners_count):
    """抽奖程序"""
    winners = random.sample(participants, winners_count)
    return winners

participants = ['张三', '李四', '王五', '赵六', '钱七', '孙八']
winners = lottery(participants, 2)
print(f"中奖者: {winners}")
```

### 随机颜色

```python
import random

def random_color():
    """生成随机十六进制颜色"""
    return f'#{random.randint(0, 0xFFFFFF):06x}'

for _ in range(5):
    print(random_color())  # #a3f2c1, #8b4d2e, ...
```

### 模拟掷骰子

```python
import random

def roll_dice(count=1):
    """掷骰子"""
    return [random.randint(1, 6) for _ in range(count)]

print(roll_dice(2))  # [3, 5]
print(roll_dice(3))  # [1, 6, 2]
```

### 模拟抛硬币

```python
import random

def flip_coin():
    """抛硬币"""
    return random.choice(['正面', '反面'])

results = [flip_coin() for _ in range(10)]
print(results)  # ['正面', '反面', '正面', ...]
```

---

## 安全随机数

对于安全敏感场景，使用 `secrets` 模块：

```python
import secrets

# 安全随机整数
token = secrets.randbelow(1000000)

# 安全随机字节
key = secrets.token_bytes(16)

# 安全随机 URL 安全字符串
token = secrets.token_urlsafe(16)

# 安全随机十六进制字符串
token = secrets.token_hex(16)
```