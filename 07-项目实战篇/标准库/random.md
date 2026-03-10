# random 模块 - 随机数

---

## 第一部分：什么是随机数与 random 模块概述

### 1.1 生活中的随机

#### 概念说明

在日常生活中，"随机"无处不在：

- 抽签决定顺序
- 掷骰子决定步数
- 彩票摇号
- 洗牌后发牌

计算机程序中同样需要"随机"：游戏里怪物的随机刷新位置、验证码的随机字符、密码的随机生成……

Python 标准库中的 `random` 模块就是专门用来处理这类需求的工具。

### 1.2 伪随机数：骰子背后的数学

#### 概念说明

有一个重要的概念需要先了解：计算机产生的随机数，**严格来说并不是真正的随机数**，而是"伪随机数"（Pseudo-random number）。

什么叫"伪"？意思是它是通过一套确定的数学公式计算出来的，只要起始条件（称为"种子"）相同，产生的随机数序列就完全一样。

可以这样理解：

```
真正的骰子：每次掷出的点数，连老天爷都不知道是多少。

伪随机数：有一台"假骰子机器"，每次开机时要输入一个起始数字（种子），
          之后每按一次按钮，它就按照内部公式算出下一个数字。
          只要起始数字相同，每次开机后按出来的序列完全一样。
```

这看起来是个缺点，但在编程中恰恰非常有用——当你需要**复现**某个随机实验时（比如调试游戏、复现科学实验），固定种子就能得到完全一样的结果。

```
┌─────────────────────────────────────────────────────┐
│                  伪随机数原理                        │
│                                                     │
│   种子 (seed)                                       │
│      │                                              │
│      ▼                                              │
│  ┌───────┐   公式f   ┌───────┐   公式f   ┌───────┐ │
│  │ 初始值 │ ───────► │  值1  │ ───────► │  值2  │  │
│  └───────┘           └───────┘           └───────┘ │
│                         │                   │      │
│                      随机数1             随机数2   │
│                                                     │
│  相同的种子 → 相同的序列，不同的种子 → 不同的序列   │
└─────────────────────────────────────────────────────┘
```

### 1.3 导入 random 模块

#### 概念说明

`random` 是 Python 内置标准库的一部分，无需安装，直接导入即可使用。

#### 示例代码

```python
# 最常见的导入方式：导入整个模块
import random

# 也可以只导入需要的函数（适合只用一两个函数时）
from random import randint, choice

# 查看 random 模块提供的所有函数
import random
print(dir(random))
```

推荐使用 `import random` 的方式，这样在代码中使用 `random.randint()` 时，一眼就能看出这个函数来自哪个模块，可读性更好。

---

## 第二部分：随机浮点数

### 2.1 random() — 生成 [0.0, 1.0) 之间的浮点数

#### 概念说明

`random.random()` 是最基础的函数，每次调用都返回一个大于等于 0.0、小于 1.0 的随机浮点数。

```
┌────────────────────────────────────────┐
│          random.random() 的范围        │
│                                        │
│   0.0                             1.0  │
│    [─────────────────────────────)     │
│    ▲                             ▲     │
│  包含 0.0                    不含 1.0  │
└────────────────────────────────────────┘
```

#### 示例代码

```python
import random

# 生成一个 [0.0, 1.0) 之间的随机浮点数
print(random.random())   # 例如: 0.37444887175646646
print(random.random())   # 例如: 0.9507143064099162
print(random.random())   # 例如: 0.7319939418114051

# 实际应用：用来模拟概率判断
# 例如，30% 的概率触发某事件
if random.random() < 0.3:
    print("触发了特殊事件！")
else:
    print("没有触发。")
```

### 2.2 uniform() — 生成指定范围内的浮点数

#### 概念说明

`random.uniform(a, b)` 返回一个介于 `a` 和 `b` 之间的随机浮点数。和 `random()` 不同，你可以自由指定范围。

注意：`a` 可以大于 `b`，结果仍然在两者之间。

#### 示例代码

```python
import random

# 生成 1.0 到 10.0 之间的随机浮点数
price = random.uniform(1.0, 10.0)
print(f"随机价格: {price:.2f} 元")   # 例如: 随机价格: 6.39 元

# 模拟一个传感器读数（温度在 36.0 到 37.5 之间）
temperature = random.uniform(36.0, 37.5)
print(f"体温: {temperature:.1f} °C")  # 例如: 体温: 36.8 °C

# a 可以大于 b
val = random.uniform(10, 1)
print(val)   # 仍然在 1 到 10 之间

# 生成多个随机浮点数
readings = [round(random.uniform(0, 100), 2) for _ in range(5)]
print("五次读数:", readings)
```

---

## 第三部分：随机整数

### 3.1 randint() — 生成指定范围内的整数

#### 概念说明

`random.randint(a, b)` 返回一个介于 `a` 和 `b` 之间的随机整数，**两端都包含**。

```
randint(1, 6)  →  相当于掷一颗六面骰子

可能的结果: 1, 2, 3, 4, 5, 6（每个等概率）
```

#### 示例代码

```python
import random

# 模拟掷一颗六面骰子
dice = random.randint(1, 6)
print(f"骰子点数: {dice}")

# 生成一个两位数的随机整数
num = random.randint(10, 99)
print(f"随机两位数: {num}")

# 注意：两端都包含
# randint(1, 1) 只可能返回 1
print(random.randint(1, 1))   # 一定是 1

# 模拟随机年龄（18 到 60 岁）
age = random.randint(18, 60)
print(f"随机年龄: {age} 岁")
```

### 3.2 randrange() — 更灵活的整数范围

#### 概念说明

`random.randrange(start, stop[, step])` 类似于内置的 `range()` 函数：

- 只有一个参数：`randrange(stop)` → 从 `[0, stop)` 中随机取一个整数
- 两个参数：`randrange(start, stop)` → 从 `[start, stop)` 中随机取一个整数（**不含 stop**）
- 三个参数：`randrange(start, stop, step)` → 从指定步长的序列中随机取一个

```
┌──────────────────────────────────────────────────────────┐
│           randint vs randrange 对比                      │
│                                                          │
│  randint(1, 6)       → 可能结果: 1 2 3 4 5 6            │
│                          (包含两端)                      │
│                                                          │
│  randrange(1, 7)     → 可能结果: 1 2 3 4 5 6            │
│                          (含左端，不含右端)              │
│                                                          │
│  randrange(0, 10, 2) → 可能结果: 0 2 4 6 8              │
│                          (步长为 2，只取偶数)            │
└──────────────────────────────────────────────────────────┘
```

#### 示例代码

```python
import random

# 从 0 到 9 中随机取一个整数（不含 10）
n = random.randrange(10)
print(f"0-9 中的随机数: {n}")

# 从 1 到 99 中随机取一个奇数（步长为 2，从 1 开始）
odd = random.randrange(1, 100, 2)
print(f"随机奇数: {odd}")   # 可能是: 1, 3, 5, ..., 99

# 从 0 到 100 中随机取一个 10 的倍数
multiple_of_10 = random.randrange(0, 101, 10)
print(f"10 的倍数: {multiple_of_10}")  # 可能是: 0, 10, 20, ..., 100

# randrange 不含右端，这是与 randint 最大的区别
# randrange(1, 6) 永远不会返回 6
result = random.randrange(1, 6)
print(f"randrange(1,6) 结果: {result}")  # 只可能是 1,2,3,4,5
```

---

## 第四部分：从序列中随机选择

### 4.1 choice() — 从序列中随机取一个元素

#### 概念说明

`random.choice(seq)` 从一个非空序列（列表、元组、字符串等）中随机返回一个元素。

就像从帽子里随机摸出一张纸条，每次只摸一张。

#### 示例代码

```python
import random

# 从列表中随机选一个
fruits = ["苹果", "香蕉", "橙子", "葡萄", "西瓜"]
picked = random.choice(fruits)
print(f"随机选中的水果: {picked}")

# 从元组中随机选一个
directions = ("上", "下", "左", "右")
move = random.choice(directions)
print(f"随机方向: {move}")

# 从字符串中随机选一个字符
alphabet = "abcdefghijklmnopqrstuvwxyz"
letter = random.choice(alphabet)
print(f"随机字母: {letter}")

# 注意：序列不能为空，否则会报错
try:
    random.choice([])
except IndexError as e:
    print(f"错误: {e}")   # 错误: Cannot choose from an empty sequence
```

### 4.2 choices() — 有放回地随机抽取多个元素

#### 概念说明

`random.choices(population, weights=None, k=1)` 从序列中随机选取 `k` 个元素，**有放回**（即同一个元素可以被选中多次）。

还可以通过 `weights` 参数为每个元素设置权重，权重越大被选中的概率越高。

```
有放回抽样示意（从 [A, B, C] 中抽 3 次）：
第 1 次: 摸出 B → 放回 → [A, B, C]
第 2 次: 摸出 B → 放回 → [A, B, C]   （B 可以再次被选中）
第 3 次: 摸出 A → 放回 → [A, B, C]
结果: ['B', 'B', 'A']
```

#### 示例代码

```python
import random

# 有放回地随机抽取 3 个水果（可重复）
fruits = ["苹果", "香蕉", "橙子", "葡萄"]
result = random.choices(fruits, k=3)
print(f"抽取结果: {result}")  # 例如: ['香蕉', '苹果', '香蕉']

# 带权重：苹果的概率是其他水果的两倍
weighted_result = random.choices(
    fruits,
    weights=[2, 1, 1, 1],  # 苹果权重为 2，其他为 1
    k=10
)
print(f"带权重的 10 次抽取: {weighted_result}")

# 模拟有偏的硬币（正面概率 70%，反面概率 30%）
coin_flips = random.choices(["正面", "反面"], weights=[70, 30], k=20)
heads = coin_flips.count("正面")
print(f"20 次投掷，正面出现 {heads} 次")
```

### 4.3 sample() — 无放回地随机抽取多个元素

#### 概念说明

`random.sample(population, k)` 从序列中随机选取 `k` 个**不重复**的元素，**无放回**（每个元素最多被选中一次）。

```
无放回抽样示意（从 [A, B, C, D] 中抽 3 个）：
第 1 次: 摸出 C → 不放回 → [A, B, D]
第 2 次: 摸出 A → 不放回 → [B, D]
第 3 次: 摸出 D → 不放回 → [B]
结果: ['C', 'A', 'D']  （无重复）
```

#### 示例代码

```python
import random

# 从 1-49 中抽取 6 个不重复的数字（双色球选号）
lottery = random.sample(range(1, 50), k=6)
lottery.sort()
print(f"双色球号码: {lottery}")   # 例如: [3, 12, 23, 31, 38, 45]

# 从名单中随机抽取 3 名幸运观众
audience = ["张三", "李四", "王五", "赵六", "孙七", "周八"]
winners = random.sample(audience, k=3)
print(f"幸运观众: {winners}")

# 注意：k 不能超过序列长度
try:
    random.sample([1, 2, 3], k=5)  # 列表只有 3 个元素，却要抽 5 个
except ValueError as e:
    print(f"错误: {e}")
```

### 4.4 三个选择函数对比

```
┌──────────────┬─────────────┬──────────────┬────────────────────────┐
│   函数        │  抽取数量   │  是否可重复  │  适用场景              │
├──────────────┼─────────────┼──────────────┼────────────────────────┤
│ choice(seq)  │  1 个       │  N/A         │  随机选一个            │
├──────────────┼─────────────┼──────────────┼────────────────────────┤
│ choices(...) │  k 个       │  可以重复    │  模拟投票、权重抽样    │
│  k=1         │             │  (有放回)    │  验证码生成            │
├──────────────┼─────────────┼──────────────┼────────────────────────┤
│ sample(...,k)│  k 个       │  不可重复    │  抽奖、洗牌、选号      │
│              │             │  (无放回)    │  随机子集              │
└──────────────┴─────────────┴──────────────┴────────────────────────┘
```

---

## 第五部分：打乱顺序

### 5.1 shuffle() — 原地打乱列表

#### 概念说明

`random.shuffle(lst)` 将一个列表**原地**打乱顺序，即直接修改传入的列表，不返回新列表（返回值是 `None`）。

"原地"的意思是：不创建新列表，而是直接在原来的列表上操作。就像你拿着一叠牌，直接在手里洗牌，而不是重新发一副新牌。

```
shuffle() 原地修改示意：

原列表: [1, 2, 3, 4, 5]
         ↓  shuffle()  ↓
原列表: [3, 1, 5, 2, 4]   （同一个列表对象，顺序变了）
返回值: None
```

#### 示例代码

```python
import random

# 打乱一副扑克牌（简化版）
cards = list(range(1, 14))  # 1 到 13 代表 A 到 K
print(f"洗牌前: {cards}")

random.shuffle(cards)
print(f"洗牌后: {cards}")

# 注意：shuffle 返回 None，不能这样写
wrong = random.shuffle(cards)
print(f"返回值是: {wrong}")   # None  ← 常见错误！

# 正确方式：先 shuffle，再使用列表
names = ["Alice", "Bob", "Charlie", "Diana"]
random.shuffle(names)
print(f"随机排列: {names}")

# 如果需要保留原列表，先复制一份
original = [1, 2, 3, 4, 5]
shuffled = original.copy()
random.shuffle(shuffled)
print(f"原列表: {original}")    # 不变
print(f"打乱版: {shuffled}")    # 已打乱

# 字符串不能直接 shuffle（字符串是不可变的）
# random.shuffle("hello")   # 这会报错！
# 解决方案：先转成列表，shuffle 后再拼接
chars = list("hello")
random.shuffle(chars)
result = "".join(chars)
print(f"打乱后的字符串: {result}")
```

---

## 第六部分：随机种子

### 6.1 seed() — 控制随机序列的起点

#### 概念说明

`random.seed(a=None)` 设置随机数生成器的种子（起始值）。

回忆前面的比喻：伪随机数就像一台"假骰子机器"，种子就是开机时输入的起始数字。相同的种子，每次运行程序得到的随机序列**完全一样**。

```
┌─────────────────────────────────────────────────────────┐
│                   seed() 的作用                         │
│                                                         │
│  不设种子（默认）:                                       │
│    每次运行程序 → 系统自动选取种子 → 序列不同           │
│                                                         │
│  设置固定种子:                                           │
│    random.seed(42)                                      │
│    每次运行程序 → 种子固定为 42 → 序列完全相同          │
│                                                         │
│  应用场景:                                               │
│    - 调试：复现某个 bug                                  │
│    - 科学实验：确保结果可复现                            │
│    - 游戏存档：记录当前随机状态以便读档                  │
└─────────────────────────────────────────────────────────┘
```

#### 示例代码

```python
import random

# 不设种子：每次运行结果都不同
print("不设种子:")
print(random.randint(1, 100))
print(random.randint(1, 100))

# 设置固定种子：每次运行结果完全一样
print("\n设置种子 42 后:")
random.seed(42)
print(random.randint(1, 100))   # 总是输出相同的值
print(random.randint(1, 100))   # 总是输出相同的值

# 再次设置相同种子，序列重新从头开始
print("\n再次设置种子 42:")
random.seed(42)
print(random.randint(1, 100))   # 和上面第一个值相同
print(random.randint(1, 100))   # 和上面第二个值相同

# 实际应用：机器学习中确保实验可复现
random.seed(2024)
train_data = list(range(100))
random.shuffle(train_data)
print(f"\n前 10 个训练样本索引: {train_data[:10]}")
# 只要种子是 2024，每次运行这个顺序都一样
```

---

## 第七部分：综合实例

### 7.1 生成随机验证码

#### 概念说明

验证码通常由数字和字母组成，需要从字符集中随机选取若干个字符拼接而成。

#### 示例代码

```python
import random
import string

def generate_captcha(length=6):
    """生成指定长度的随机验证码（数字 + 大写字母）"""
    # string.digits = '0123456789'
    # string.ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    characters = string.digits + string.ascii_uppercase
    
    # 使用 choices 有放回抽取（验证码允许重复字符）
    captcha = random.choices(characters, k=length)
    return "".join(captcha)

# 生成 5 个验证码
for i in range(5):
    code = generate_captcha(6)
    print(f"验证码 {i+1}: {code}")

# 生成只含数字的 4 位验证码（适合短信验证码）
def generate_sms_code(length=4):
    return "".join(random.choices(string.digits, k=length))

print(f"\n短信验证码: {generate_sms_code()}")
```

### 7.2 抽奖程序

#### 概念说明

抽奖程序的核心是"无放回抽样"——每个人只能中奖一次，使用 `sample()` 最合适。

#### 示例代码

```python
import random

def lottery(participants, prizes):
    """
    抽奖程序
    participants: 参与者名单（列表）
    prizes: 奖项字典，格式为 {奖项名称: 名额数量}
    """
    # 复制一份名单，避免修改原数据
    remaining = participants.copy()
    results = {}
    
    for prize_name, count in prizes.items():
        if len(remaining) < count:
            print(f"警告: 剩余人数不足，{prize_name} 只能抽取 {len(remaining)} 人")
            count = len(remaining)
        
        # 从剩余参与者中无放回抽取
        winners = random.sample(remaining, k=count)
        results[prize_name] = winners
        
        # 将中奖者从名单中移除（已中奖的不能再中奖）
        for winner in winners:
            remaining.remove(winner)
    
    return results

# 模拟年会抽奖
participants = [f"员工{i:03d}" for i in range(1, 51)]  # 50 名员工

prizes = {
    "一等奖（iPhone）":   1,
    "二等奖（iPad）":     3,
    "三等奖（耳机）":     10,
}

print("=== 年会抽奖开始 ===\n")
results = lottery(participants, prizes)

for prize, winners in results.items():
    print(f"{prize}:")
    for w in winners:
        print(f"    {w}")
    print()

print("=== 抽奖结束 ===")
```

### 7.3 猜数字游戏

#### 概念说明

经典的猜数字游戏：程序随机生成一个数字，玩家猜，程序提示"大了"或"小了"，直到猜中为止。

#### 示例代码

```python
import random

def guess_number_game():
    """猜数字游戏：程序随机生成 1-100 之间的整数，玩家猜测"""
    secret = random.randint(1, 100)
    attempts = 0
    max_attempts = 7  # 最多猜 7 次（理论上二分法 7 次足够）
    
    print("=== 猜数字游戏 ===")
    print(f"我想了一个 1 到 100 之间的整数，你有 {max_attempts} 次机会猜中它！")
    
    while attempts < max_attempts:
        attempts += 1
        remaining = max_attempts - attempts
        
        try:
            guess = int(input(f"\n第 {attempts} 次猜测（剩余 {remaining} 次）: "))
        except ValueError:
            print("请输入一个整数！")
            attempts -= 1  # 不计入无效输入
            continue
        
        if guess == secret:
            print(f"恭喜你！猜对了！答案就是 {secret}，你用了 {attempts} 次。")
            return True
        elif guess < secret:
            print("太小了，再大一点！")
        else:
            print("太大了，再小一点！")
    
    print(f"\n很遗憾，{max_attempts} 次机会用完了。答案是 {secret}。")
    return False

# 取消注释以运行游戏：
# guess_number_game()

# 演示模式（无需用户输入，自动模拟二分法）
def demo_binary_search():
    """演示用二分法猜数字的过程"""
    secret = random.randint(1, 100)
    low, high = 1, 100
    attempts = 0
    
    print(f"答案是: {secret}（演示二分法猜测过程）")
    
    while low <= high:
        attempts += 1
        mid = (low + high) // 2
        print(f"第 {attempts} 次猜: {mid}", end=" → ")
        
        if mid == secret:
            print(f"猜中了！共 {attempts} 次")
            break
        elif mid < secret:
            print("太小")
            low = mid + 1
        else:
            print("太大")
            high = mid - 1

demo_binary_search()
```

### 7.4 模拟掷骰子统计

#### 概念说明

通过大量模拟来验证概率理论——掷一颗公平骰子，每个点数出现的概率应该接近 1/6（约 16.67%）。

#### 示例代码

```python
import random

def simulate_dice(rolls=10000):
    """模拟掷骰子 N 次，统计每个点数出现的频率"""
    counts = {i: 0 for i in range(1, 7)}  # 初始化计数器
    
    for _ in range(rolls):
        result = random.randint(1, 6)
        counts[result] += 1
    
    print(f"模拟掷骰子 {rolls} 次的结果：\n")
    print(f"{'点数':<6} {'次数':<8} {'频率':<10} {'可视化'}")
    print("-" * 50)
    
    for face, count in sorted(counts.items()):
        frequency = count / rolls * 100
        bar = "#" * int(frequency / 2)  # 用 # 号画简单柱状图
        print(f"{face:<6} {count:<8} {frequency:<9.2f}% {bar}")
    
    print("-" * 50)
    print(f"理论期望频率: 16.67%（每个点数）")

simulate_dice(10000)

# 进阶：模拟两颗骰子的点数之和
def simulate_two_dice(rolls=50000):
    """模拟两颗骰子之和的分布"""
    counts = {i: 0 for i in range(2, 13)}
    
    for _ in range(rolls):
        total = random.randint(1, 6) + random.randint(1, 6)
        counts[total] += 1
    
    print(f"\n模拟两颗骰子之和（共 {rolls} 次）：\n")
    for total, count in sorted(counts.items()):
        freq = count / rolls * 100
        bar = "#" * int(freq / 0.5)
        print(f"点数和 {total:2d}: {freq:5.2f}% {bar}")

simulate_two_dice()
```

### 7.5 随机密码生成器

#### 概念说明

安全的密码应该包含大写字母、小写字母、数字和特殊字符，且字符顺序随机。

#### 示例代码

```python
import random
import string

def generate_password(length=12, use_upper=True, use_lower=True,
                       use_digits=True, use_symbols=True):
    """
    生成随机强密码
    
    参数:
        length:      密码长度（默认 12）
        use_upper:   是否包含大写字母
        use_lower:   是否包含小写字母
        use_digits:  是否包含数字
        use_symbols: 是否包含特殊字符
    """
    charset = ""
    required_chars = []  # 确保每种字符至少出现一次
    
    if use_upper:
        charset += string.ascii_uppercase
        required_chars.append(random.choice(string.ascii_uppercase))
    
    if use_lower:
        charset += string.ascii_lowercase
        required_chars.append(random.choice(string.ascii_lowercase))
    
    if use_digits:
        charset += string.digits
        required_chars.append(random.choice(string.digits))
    
    if use_symbols:
        symbols = "!@#$%^&*()-_=+"
        charset += symbols
        required_chars.append(random.choice(symbols))
    
    if not charset:
        raise ValueError("至少需要选择一种字符类型")
    
    # 随机填充剩余位数
    remaining_length = length - len(required_chars)
    if remaining_length < 0:
        remaining_length = 0
    
    random_chars = random.choices(charset, k=remaining_length)
    
    # 合并并打乱顺序（避免必选字符总是在开头）
    all_chars = required_chars + random_chars
    random.shuffle(all_chars)
    
    return "".join(all_chars[:length])

# 生成不同类型的密码
print("=== 随机密码生成器 ===\n")

for i in range(5):
    pwd = generate_password(length=16)
    print(f"强密码 {i+1}: {pwd}")

print()
# 只含字母和数字（适合某些不支持特殊字符的网站）
for i in range(3):
    pwd = generate_password(length=10, use_symbols=False)
    print(f"无符号密码 {i+1}: {pwd}")
```

---

## 第八部分：函数速查表

```
┌────────────────────────┬──────────────────────────┬──────────────────────────────┐
│  函数                  │  返回值                  │  说明                        │
├────────────────────────┼──────────────────────────┼──────────────────────────────┤
│ random()               │  float [0.0, 1.0)        │  最基础的随机浮点数          │
├────────────────────────┼──────────────────────────┼──────────────────────────────┤
│ uniform(a, b)          │  float [a, b]            │  指定范围的随机浮点数        │
├────────────────────────┼──────────────────────────┼──────────────────────────────┤
│ randint(a, b)          │  int [a, b]              │  含两端的随机整数            │
├────────────────────────┼──────────────────────────┼──────────────────────────────┤
│ randrange(start,       │  int                     │  类似 range()，不含右端      │
│   stop[, step])        │                          │                              │
├────────────────────────┼──────────────────────────┼──────────────────────────────┤
│ choice(seq)            │  seq 中的一个元素        │  随机选一个，不可用于空序列  │
├────────────────────────┼──────────────────────────┼──────────────────────────────┤
│ choices(pop, k=n)      │  含 n 个元素的列表       │  有放回，可设权重            │
├────────────────────────┼──────────────────────────┼──────────────────────────────┤
│ sample(pop, k)         │  含 k 个元素的列表       │  无放回，不可重复            │
├────────────────────────┼──────────────────────────┼──────────────────────────────┤
│ shuffle(lst)           │  None（原地修改）        │  打乱列表顺序                │
├────────────────────────┼──────────────────────────┼──────────────────────────────┤
│ seed(a)                │  None                    │  设置随机种子，固定序列      │
└────────────────────────┴──────────────────────────┴──────────────────────────────┘
```

---

## 第九部分：常见错误和注意事项

### 9.1 shuffle() 的返回值是 None

#### 概念说明

初学者最常犯的错误是把 `shuffle()` 的返回值赋给一个变量，导致变量变成 `None`。

#### 示例代码

```python
import random

nums = [1, 2, 3, 4, 5]

# 错误写法：result 将会是 None
result = random.shuffle(nums)
print(result)   # None  ← 出错了！

# 正确写法：先 shuffle，再使用原来的列表
random.shuffle(nums)
print(nums)     # 已打乱的列表
```

### 9.2 randint 含两端，randrange 不含右端

#### 概念说明

这两个函数的边界处理不同，混淆后容易产生难以察觉的 bug。

#### 示例代码

```python
import random

# randint(1, 6) 可以返回 6
# 相当于掷骰子，1 到 6 都能出现
dice = random.randint(1, 6)

# randrange(1, 6) 不能返回 6
# 相当于从 [1, 2, 3, 4, 5] 中随机选一个
wrong_dice = random.randrange(1, 6)   # 永远不会是 6！

# 要用 randrange 模拟骰子，应该写：
correct_dice = random.randrange(1, 7)  # 1 到 6

print(f"randint(1,6)  范围: 1-6  含 6")
print(f"randrange(1,6) 范围: 1-5  不含 6  ← 当心！")
print(f"randrange(1,7) 范围: 1-6  含 6（等效 randint）")
```

### 9.3 不要把 random 用于安全场景

#### 概念说明

`random` 模块生成的是伪随机数，**不适合用于密码学或安全场景**（如生成 token、加密密钥、安全的会话 ID 等）。

对于安全场景，应使用 Python 标准库中的 `secrets` 模块。

#### 示例代码

```python
import secrets  # 安全随机数模块

# 安全的随机 token（适合用于重置密码链接等）
token = secrets.token_hex(16)   # 16 字节 = 32 位十六进制
print(f"安全 token: {token}")

# 安全的随机整数
secure_num = secrets.randbelow(100)
print(f"安全随机整数: {secure_num}")

# 安全的随机选择
secure_choice = secrets.choice(["A", "B", "C"])
print(f"安全随机选择: {secure_choice}")

# 对比：
# random 模块  → 速度快，适合模拟、游戏、数据处理
# secrets 模块 → 安全性高，适合密码学、身份验证
```

### 9.4 choice() 不能用于空序列

#### 示例代码

```python
import random

# 使用前要确认序列非空
items = []

# 直接使用会报错
try:
    random.choice(items)
except IndexError:
    print("错误：不能从空序列中选择")

# 正确做法：先检查
if items:
    result = random.choice(items)
else:
    print("序列为空，无法选择")
```

### 9.5 seed() 只影响当前程序中的随机状态

#### 概念说明

`random.seed()` 设置的种子会在程序运行期间持续影响后续所有的随机调用，直到再次调用 `seed()` 为止。

#### 示例代码

```python
import random

random.seed(100)
print(random.randint(1, 100))   # 固定值，例如 15
print(random.randint(1, 100))   # 固定值，例如 43
print(random.randint(1, 100))   # 固定值，例如 71

# 中途调用其他随机函数，会消耗随机序列中的"名额"
random.seed(100)
print(random.randint(1, 100))   # 和上面第一个相同：15
random.random()                 # 消耗了一个随机数
print(random.randint(1, 100))   # 和上面第三个相同：71（因为中间插了一个）
```

---

[返回索引](../README.md) | [返回 11-模块与包](../11-模块与包.md)
