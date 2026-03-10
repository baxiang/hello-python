# math 模块 - 数学运算

Python 内置的 `math` 模块提供了丰富的数学函数和常量，是进行科学计算、几何运算、工程计算的基础工具。本章将从零开始，带你掌握 `math` 模块的核心用法。

---

## 第一部分：什么是 math 模块

### 1.1 概念说明

#### 概念说明

想象你是一名工程师，需要计算圆形水池的面积、斜坡的角度、信号的衰减曲线……这些计算都离不开数学公式。Python 的 `math` 模块就像一本随身携带的"数学工具书"，里面预先写好了几十种常用的数学函数和常量，你只需要调用即可，不必自己从头实现。

`math` 模块属于 Python **标准库**的一部分，安装 Python 时就已自动附带，无需额外安装。它的底层由 C 语言实现，运行速度快，精度高，是数值计算的首选工具。

```
┌──────────────────────────────────────────────────────────┐
│                   Python 程序                             │
│                                                          │
│   import math          ← 引入工具箱                       │
│                                                          │
│   math.sqrt(16)        ← 使用工具：开平方                  │
│   math.pi              ← 使用常量：圆周率                  │
│   math.sin(math.pi/6)  ← 使用工具：正弦函数               │
└──────────────────────────────────────────────────────────┘
```

#### 示例代码

```python
# 不使用 math 模块：手动计算平方根（繁琐且易出错）
x = 2.0
result = x ** 0.5
print(result)  # 1.4142135623730951

# 使用 math 模块：直接调用，语义清晰
import math
result = math.sqrt(2)
print(result)  # 1.4142135623730951
```

### 1.2 为什么需要 math 模块

#### 概念说明

Python 本身支持基本的算术运算（`+`、`-`、`*`、`/`、`**`），但对于以下场景，基础运算符力不从心：

- 三角函数（正弦、余弦、正切）
- 对数函数（自然对数、以 2 为底、以 10 为底）
- 取整（向上取整、向下取整）
- 数学常量（圆周率 π、自然常数 e）
- 特殊值（无穷大、非数字 NaN）

`math` 模块将这些功能统一封装，使代码更具可读性，也更不容易出错。

```
┌─────────────────────────────────────────────────────────────┐
│  math 模块功能全景                                           │
├──────────────┬──────────────────────────────────────────────┤
│ 基础运算      │ sqrt、pow、fabs、factorial、gcd、lcm         │
├──────────────┼──────────────────────────────────────────────┤
│ 取整函数      │ ceil、floor、trunc、round（内置）             │
├──────────────┼──────────────────────────────────────────────┤
│ 三角函数      │ sin、cos、tan、asin、acos、atan、atan2        │
├──────────────┼──────────────────────────────────────────────┤
│ 双曲函数      │ sinh、cosh、tanh                             │
├──────────────┼──────────────────────────────────────────────┤
│ 对数函数      │ log、log2、log10、exp                        │
├──────────────┼──────────────────────────────────────────────┤
│ 数学常量      │ pi、e、tau、inf、nan                         │
└──────────────┴──────────────────────────────────────────────┘
```

---

## 第二部分：导入方式

### 2.1 三种导入方式对比

#### 概念说明

在 Python 中，使用模块前必须先导入。`math` 模块有三种常见的导入方式，各有适用场景。

```
┌─────────────────────────────────────────────────────────────┐
│  导入方式对比                                                │
├──────────────────────┬──────────────────────────────────────┤
│ 方式                  │ 示例                                │
├──────────────────────┼──────────────────────────────────────┤
│ import math          │ math.sqrt(4)     ← 推荐，最清晰      │
├──────────────────────┼──────────────────────────────────────┤
│ from math import ... │ sqrt(4)          ← 适合常用函数      │
├──────────────────────┼──────────────────────────────────────┤
│ from math import *   │ sqrt(4)          ← 不推荐，污染命名空间│
└──────────────────────┴──────────────────────────────────────┘
```

**推荐使用第一种**：`import math`，每次调用时写 `math.函数名`，代码阅读者一眼就知道这个函数来自 `math` 模块。

#### 示例代码

```python
# 方式一：整体导入（推荐）
import math

print(math.sqrt(9))   # 3.0
print(math.pi)        # 3.141592653589793

# 方式二：按需导入（适合只用少数函数时）
from math import sqrt, pi

print(sqrt(9))        # 3.0
print(pi)             # 3.141592653589793

# 方式三：导入全部（不推荐，容易与自定义函数名冲突）
from math import *

print(sqrt(9))        # 3.0
print(pi)             # 3.141592653589793

# 风险示例：名称冲突
# 如果你自己写了一个 sqrt 函数，from math import * 会覆盖它
def sqrt(x):
    return "我的自定义函数"

from math import *    # 这行之后，sqrt 又变回了 math.sqrt
```

---

## 第三部分：基础数学运算

### 3.1 sqrt — 平方根

#### 概念说明

`math.sqrt(x)` 计算 `x` 的平方根（square root）。输入必须是非负数，结果始终是浮点数（float）。

与 `x ** 0.5` 的区别：`math.sqrt` 对负数会直接抛出 `ValueError`，而 `x ** 0.5` 对负数会返回 `nan`（在某些情况下）。使用 `math.sqrt` 能让错误更早暴露，更容易调试。

#### 示例代码

```python
import math

# 基本用法
print(math.sqrt(4))     # 2.0
print(math.sqrt(2))     # 1.4142135623730951
print(math.sqrt(0))     # 0.0
print(math.sqrt(100))   # 10.0

# 注意：结果始终是 float
result = math.sqrt(9)
print(type(result))     # <class 'float'>
print(result)           # 3.0，不是整数 3

# 负数会抛出异常
try:
    math.sqrt(-1)
except ValueError as e:
    print(f"错误：{e}")  # 错误：math domain error

# 实际应用：计算直角三角形斜边
a = 3
b = 4
hypotenuse = math.sqrt(a**2 + b**2)
print(f"斜边长度：{hypotenuse}")  # 斜边长度：5.0
```

### 3.2 pow — 幂运算

#### 概念说明

`math.pow(x, y)` 计算 `x` 的 `y` 次幂，结果**始终是浮点数**。

这与 Python 内置的 `**` 运算符不同：`2 ** 3` 返回整数 `8`，而 `math.pow(2, 3)` 返回浮点数 `8.0`。

使用场景：当你需要确保结果是浮点数时（如科学计算、与其他浮点运算混用时），使用 `math.pow` 更安全。

#### 示例代码

```python
import math

# 基本幂运算
print(math.pow(2, 3))    # 8.0（注意是浮点数）
print(math.pow(3, 2))    # 9.0
print(math.pow(10, 0))   # 1.0
print(math.pow(2, -1))   # 0.5（负指数 = 取倒数）

# 与 ** 运算符对比
print(2 ** 3)             # 8（整数）
print(math.pow(2, 3))     # 8.0（浮点数）

# 分数指数（等价于开根号）
print(math.pow(27, 1/3))  # 3.0（立方根）
print(math.pow(16, 0.25)) # 2.0（四次方根）

# 实际应用：计算复利
principal = 10000   # 本金
rate = 0.05         # 年利率 5%
years = 10          # 投资年限
amount = principal * math.pow(1 + rate, years)
print(f"10年后金额：{amount:.2f} 元")  # 10年后金额：16288.95 元
```

### 3.3 fabs — 绝对值

#### 概念说明

`math.fabs(x)` 返回 `x` 的绝对值，结果**始终是浮点数**。

与内置 `abs()` 函数的区别：`abs(-3)` 返回整数 `3`，而 `math.fabs(-3)` 返回浮点数 `3.0`。在数值计算中，保持浮点类型有助于避免隐式类型转换带来的精度问题。

#### 示例代码

```python
import math

# 基本用法
print(math.fabs(-5))    # 5.0
print(math.fabs(5))     # 5.0
print(math.fabs(-3.14)) # 3.14
print(math.fabs(0))     # 0.0

# 与内置 abs() 对比
print(abs(-3))           # 3（整数）
print(math.fabs(-3))     # 3.0（浮点数）

# 实际应用：计算两个数的差的绝对值（误差）
measured = 9.81
expected = 9.8
error = math.fabs(measured - expected)
print(f"测量误差：{error:.4f}")  # 测量误差：0.0100
```

### 3.4 factorial — 阶乘

#### 概念说明

`math.factorial(n)` 计算非负整数 `n` 的阶乘（n!）。阶乘定义为：

```
n! = n × (n-1) × (n-2) × ... × 2 × 1
0! = 1（规定）
```

阶乘常用于排列组合、概率计算。

#### 示例代码

```python
import math

# 基本用法
print(math.factorial(0))  # 1
print(math.factorial(1))  # 1
print(math.factorial(5))  # 120（5×4×3×2×1）
print(math.factorial(10)) # 3628800

# 实际应用：计算排列数 P(n, r) = n! / (n-r)!
def permutation(n, r):
    return math.factorial(n) // math.factorial(n - r)

print(permutation(5, 3))  # 60（从5个中取3个的排列数）

# 实际应用：计算组合数 C(n, r) = n! / (r! × (n-r)!)
def combination(n, r):
    return math.factorial(n) // (math.factorial(r) * math.factorial(n - r))

print(combination(5, 2))  # 10（从5个中取2个的组合数）

# 注意：参数必须是非负整数
try:
    math.factorial(-1)
except ValueError as e:
    print(f"错误：{e}")  # 错误：factorial() not defined for negative values
```

### 3.5 gcd 和 lcm — 最大公约数与最小公倍数

#### 概念说明

- `math.gcd(a, b)`：返回 a 和 b 的最大公约数（Greatest Common Divisor）
- `math.lcm(a, b)`：返回 a 和 b 的最小公倍数（Least Common Multiple，Python 3.9+）

这两个函数常用于分数化简、时间周期计算等场景。

#### 示例代码

```python
import math

# 最大公约数
print(math.gcd(12, 8))   # 4
print(math.gcd(100, 75)) # 25
print(math.gcd(7, 13))   # 1（互质）

# 最小公倍数（Python 3.9+）
print(math.lcm(4, 6))    # 12
print(math.lcm(3, 5))    # 15

# 实际应用：分数化简
numerator = 18
denominator = 24
divisor = math.gcd(numerator, denominator)
print(f"18/24 化简为 {numerator//divisor}/{denominator//divisor}")
# 18/24 化简为 3/4
```

---

## 第四部分：取整函数

### 4.1 三种取整方式图解

#### 概念说明

Python 中有三种取整方式，它们的行为在处理负数时有显著区别。以下数轴图解展示了三者的区别：

```
数轴示例（以 2.3 和 -2.3 为例）

        -3      -2.3    -2      0       2       2.3     3
─────────┼───────┼───────┼───────┼───────┼───────┼───────┼────
         │       │       │       │       │       │       │

ceil（向上取整，朝正无穷方向）：
  2.3  → 3      （往右找最近整数）
 -2.3  → -2     （往右找最近整数）

floor（向下取整，朝负无穷方向）：
  2.3  → 2      （往左找最近整数）
 -2.3  → -3     （往左找最近整数）

trunc（截断，直接去掉小数部分，朝零方向）：
  2.3  → 2      （去掉 .3）
 -2.3  → -2     （去掉 .3，朝零方向）
```

注意：`ceil` 和 `floor` 对正数行为相同，但对**负数**行为相反，这是初学者最容易混淆的地方。

### 4.2 ceil — 向上取整

#### 概念说明

`math.ceil(x)` 返回大于或等于 `x` 的最小整数（向上取整，朝正无穷大方向）。

生活类比：你需要购买 2.3 米的布料，但布料只能整米出售，你必须买 3 米（不能少买）。

#### 示例代码

```python
import math

# 正数向上取整
print(math.ceil(2.1))   # 3
print(math.ceil(2.9))   # 3
print(math.ceil(2.0))   # 2（已经是整数，不变）

# 负数向上取整（朝零方向）
print(math.ceil(-2.1))  # -2
print(math.ceil(-2.9))  # -2
print(math.ceil(-3.0))  # -3（已经是整数，不变）

# 实际应用：分页计算
total_items = 23
items_per_page = 5
total_pages = math.ceil(total_items / items_per_page)
print(f"共需 {total_pages} 页")  # 共需 5 页（23/5=4.6，向上取整为5）

# 实际应用：需要多少个容器
water_liters = 7.5
bucket_capacity = 2
buckets_needed = math.ceil(water_liters / bucket_capacity)
print(f"需要 {buckets_needed} 个桶")  # 需要 4 个桶
```

### 4.3 floor — 向下取整

#### 概念说明

`math.floor(x)` 返回小于或等于 `x` 的最大整数（向下取整，朝负无穷方向）。

生活类比：你有 7.9 元，但只能买整元的商品，你最多能买价值 7 元的（不能超额）。

#### 示例代码

```python
import math

# 正数向下取整
print(math.floor(2.1))   # 2
print(math.floor(2.9))   # 2
print(math.floor(2.0))   # 2

# 负数向下取整（远离零方向）
print(math.floor(-2.1))  # -3（注意！）
print(math.floor(-2.9))  # -3（注意！）
print(math.floor(-3.0))  # -3

# 实际应用：将时间（秒）转换为分钟数（完整分钟）
total_seconds = 145
minutes = math.floor(total_seconds / 60)
seconds = total_seconds % 60
print(f"{total_seconds}秒 = {minutes}分{seconds}秒")  # 145秒 = 2分25秒

# 实际应用：计算年龄（完整年数）
import datetime
birth_year = 2000
current_year = datetime.datetime.now().year
age = math.floor(current_year - birth_year)
print(f"大约年龄：{age} 岁")
```

### 4.4 trunc — 截断取整

#### 概念说明

`math.trunc(x)` 直接截断小数部分，返回整数部分（朝零方向取整）。

对于正数，`trunc` 和 `floor` 结果相同；对于负数，`trunc` 和 `ceil` 结果相同。

```
┌───────────────────────────────────────────────────────────┐
│  三种取整函数对比总结                                       │
├──────────┬──────────┬──────────┬──────────┬───────────────┤
│  输入     │  ceil    │  floor   │  trunc   │  说明         │
├──────────┼──────────┼──────────┼──────────┼───────────────┤
│   2.3    │    3     │    2     │    2     │               │
│   2.7    │    3     │    2     │    2     │ 正数：         │
│   2.0    │    2     │    2     │    2     │ ceil向上取整   │
│  -2.3    │   -2     │   -3     │   -2     │ floor/trunc   │
│  -2.7    │   -2     │   -3     │   -2     │ 均向下（正数） │
│  -2.0    │   -2     │   -2     │   -2     │               │
└──────────┴──────────┴──────────┴──────────┴───────────────┘
```

#### 示例代码

```python
import math

# 正数截断（与 floor 相同）
print(math.trunc(2.1))   # 2
print(math.trunc(2.9))   # 2

# 负数截断（与 ceil 相同，朝零方向）
print(math.trunc(-2.1))  # -2（不是 -3！）
print(math.trunc(-2.9))  # -2（不是 -3！）

# 与 int() 的关系
# int() 对浮点数的行为与 trunc() 完全相同
print(int(2.9))           # 2（等同于 trunc）
print(int(-2.9))          # -2（等同于 trunc）

# 对比三种函数
x = -3.7
print(f"ceil({x})  = {math.ceil(x)}")   # ceil(-3.7)  = -3
print(f"floor({x}) = {math.floor(x)}")  # floor(-3.7) = -4
print(f"trunc({x}) = {math.trunc(x)}")  # trunc(-3.7) = -3
```

---

## 第五部分：三角函数

### 5.1 弧度与角度

#### 概念说明

Python 的三角函数使用**弧度（radians）**而不是**角度（degrees）**。这对初学者来说容易造成困惑。

弧度与角度的关系：
```
角度（degrees） × π / 180 = 弧度（radians）
弧度（radians） × 180 / π = 角度（degrees）

常用对应关系：
┌─────────────┬────────────────────────────────┐
│  角度        │  弧度                          │
├─────────────┼────────────────────────────────┤
│     0°      │  0                             │
│    30°      │  π/6  ≈ 0.5236                 │
│    45°      │  π/4  ≈ 0.7854                 │
│    60°      │  π/3  ≈ 1.0472                 │
│    90°      │  π/2  ≈ 1.5708                 │
│   180°      │  π    ≈ 3.1416                 │
│   270°      │  3π/2 ≈ 4.7124                 │
│   360°      │  2π   ≈ 6.2832                 │
└─────────────┴────────────────────────────────┘
```

`math.radians(deg)` 将角度转换为弧度，`math.degrees(rad)` 将弧度转换为角度。

#### 示例代码

```python
import math

# 角度转弧度
print(math.radians(0))    # 0.0
print(math.radians(90))   # 1.5707963267948966（π/2）
print(math.radians(180))  # 3.141592653589793（π）
print(math.radians(360))  # 6.283185307179586（2π）

# 弧度转角度
print(math.degrees(0))         # 0.0
print(math.degrees(math.pi))   # 180.0
print(math.degrees(math.pi/2)) # 90.0
print(math.degrees(math.pi/4)) # 45.0
```

### 5.2 单位圆与三角函数

#### 概念说明

三角函数的直觉理解可以借助单位圆（半径为 1 的圆）：

```
        y
        │
   1    │    (0, 1)
        │   /
        │  / 角度 θ
        │ /
        │/───────────── x
  (-1,0)│(0,0)    (1, 0)
        │
        │
        │
   -1   │   (0, -1)

  对于单位圆上角度为 θ 的点 (x, y)：
  ┌────────────────────────────┐
  │  cos(θ) = x 坐标           │
  │  sin(θ) = y 坐标           │
  │  tan(θ) = y/x = sin/cos   │
  └────────────────────────────┘
```

### 5.3 sin、cos、tan — 基本三角函数

#### 概念说明

- `math.sin(x)`：正弦函数，返回 x（弧度）的正弦值，范围 [-1, 1]
- `math.cos(x)`：余弦函数，返回 x（弧度）的余弦值，范围 [-1, 1]
- `math.tan(x)`：正切函数，返回 x（弧度）的正切值，范围 (-∞, +∞)

#### 示例代码

```python
import math

# sin 函数（注意使用 math.radians 转换角度）
print(math.sin(math.radians(0)))    # 0.0
print(math.sin(math.radians(30)))   # 0.49999999999999994（约 0.5）
print(math.sin(math.radians(90)))   # 1.0
print(math.sin(math.radians(180)))  # 1.2246467991473532e-16（约 0，浮点误差）

# cos 函数
print(math.cos(math.radians(0)))    # 1.0
print(math.cos(math.radians(60)))   # 0.5000000000000001（约 0.5）
print(math.cos(math.radians(90)))   # 6.123233995736766e-17（约 0，浮点误差）
print(math.cos(math.radians(180)))  # -1.0

# tan 函数
print(math.tan(math.radians(0)))    # 0.0
print(math.tan(math.radians(45)))   # 0.9999999999999999（约 1.0）
print(math.tan(math.radians(30)))   # 0.5773502691896257（约 √3/3）

# 实际应用：已知斜边和角度，求直角三角形的两条直角边
hypotenuse = 10  # 斜边
angle_deg = 30   # 一个锐角（度）

angle_rad = math.radians(angle_deg)
opposite = hypotenuse * math.sin(angle_rad)   # 对边
adjacent = hypotenuse * math.cos(angle_rad)   # 邻边

print(f"对边长度：{opposite:.4f}")  # 对边长度：5.0000
print(f"邻边长度：{adjacent:.4f}")  # 邻边长度：8.6603
```

### 5.4 asin、acos、atan — 反三角函数

#### 概念说明

反三角函数是三角函数的逆运算，用于从比值反推角度：

- `math.asin(x)`：反正弦，输入 [-1, 1]，返回弧度 [-π/2, π/2]
- `math.acos(x)`：反余弦，输入 [-1, 1]，返回弧度 [0, π]
- `math.atan(x)`：反正切，输入任意实数，返回弧度 (-π/2, π/2)
- `math.atan2(y, x)`：双参数反正切，能正确处理所有象限，返回 (-π, π]

#### 示例代码

```python
import math

# 反正弦（已知对边/斜边比，求角度）
ratio = 0.5  # sin(30°) = 0.5
angle_rad = math.asin(ratio)
angle_deg = math.degrees(angle_rad)
print(f"asin(0.5) = {angle_deg:.1f}°")  # asin(0.5) = 30.0°

# 反余弦（已知邻边/斜边比，求角度）
ratio = 0.5  # cos(60°) = 0.5
angle_deg = math.degrees(math.acos(ratio))
print(f"acos(0.5) = {angle_deg:.1f}°")  # acos(0.5) = 60.0°

# 实际应用：已知三角形三条边，求角度（余弦定理）
a, b, c = 3, 4, 5  # 勾股数
# 余弦定理：cos(C) = (a² + b² - c²) / (2ab)
cos_C = (a**2 + b**2 - c**2) / (2 * a * b)
angle_C = math.degrees(math.acos(cos_C))
print(f"C 角度：{angle_C:.1f}°")  # C 角度：90.0°（验证了勾股定理）

# atan2：推荐用于计算方向角（正确处理四个象限）
# 例如：向量 (x=1, y=1) 的方向角（与 x 轴夹角）
angle = math.degrees(math.atan2(1, 1))
print(f"(1,1) 方向角：{angle}°")   # 45.0°

angle = math.degrees(math.atan2(1, -1))
print(f"(-1,1) 方向角：{angle}°")  # 135.0°（第二象限，atan 会出错，atan2 正确）
```

---

## 第六部分：对数函数

### 6.1 log — 自然对数与任意底对数

#### 概念说明

对数是指数的逆运算。如果 `a^y = x`，则 `log_a(x) = y`。

```
指数与对数的关系：
┌─────────────────────────────────────────────┐
│  指数形式：2^3 = 8                          │
│  对数形式：log₂(8) = 3                      │
│                                             │
│  指数形式：e^1 ≈ 2.718                      │
│  对数形式：ln(e) = 1（自然对数）             │
│                                             │
│  指数形式：10^2 = 100                       │
│  对数形式：log₁₀(100) = 2（常用对数）        │
└─────────────────────────────────────────────┘
```

- `math.log(x)`：以 e 为底的自然对数，等价于 ln(x)
- `math.log(x, base)`：以 `base` 为底的对数
- `math.log2(x)`：以 2 为底的对数（比 `log(x, 2)` 更精确）
- `math.log10(x)`：以 10 为底的对数（比 `log(x, 10)` 更精确）

#### 示例代码

```python
import math

# 自然对数 ln(x)
print(math.log(1))         # 0.0（ln(1) = 0）
print(math.log(math.e))    # 1.0（ln(e) = 1）
print(math.log(math.e**2)) # 2.0（ln(e²) = 2）

# 以 2 为底的对数（常用于计算机科学：二进制位数）
print(math.log2(1))     # 0.0
print(math.log2(2))     # 1.0
print(math.log2(8))     # 3.0
print(math.log2(1024))  # 10.0（2^10 = 1024）

# 以 10 为底的对数（常用对数）
print(math.log10(1))     # 0.0
print(math.log10(10))    # 1.0
print(math.log10(100))   # 2.0
print(math.log10(1000))  # 3.0

# 任意底数的对数
print(math.log(8, 2))    # 3.0（以 2 为底，8 的对数）
print(math.log(81, 3))   # 4.0（以 3 为底，81 的对数）

# 实际应用：计算存储大量数据需要多少位二进制
data_count = 1000000  # 一百万条数据
bits_needed = math.ceil(math.log2(data_count))
print(f"存储 {data_count} 条数据需要 {bits_needed} 位二进制")
# 存储 1000000 条数据需要 20 位二进制

# 实际应用：pH 值计算（化学）
hydrogen_concentration = 1e-7  # 纯水中 H+ 浓度
ph = -math.log10(hydrogen_concentration)
print(f"pH 值：{ph}")  # pH 值：7.0
```

### 6.2 exp — 指数函数

#### 概念说明

`math.exp(x)` 计算 e 的 x 次幂（e^x），是自然对数的逆运算。

使用 `math.exp(x)` 比 `math.e ** x` 精度更高，推荐用于科学计算。

#### 示例代码

```python
import math

print(math.exp(0))   # 1.0（e^0 = 1）
print(math.exp(1))   # 2.718281828459045（e^1 = e）
print(math.exp(2))   # 7.38905609893065（e^2）
print(math.exp(-1))  # 0.36787944117144233（e^-1）

# 实际应用：人口增长模型 P(t) = P0 * e^(rt)
P0 = 1000      # 初始人口
r = 0.03       # 年增长率 3%
t = 10         # 10 年
population = P0 * math.exp(r * t)
print(f"10 年后人口：{population:.0f}")  # 10 年后人口：1350
```

---

## 第七部分：数学常量

### 7.1 常量一览

#### 概念说明

`math` 模块预定义了几个重要的数学常量，无需手动输入精确值：

```
┌──────────────┬───────────────────────────────┬──────────────────────────────────┐
│  常量         │  值（近似）                   │  含义                            │
├──────────────┼───────────────────────────────┼──────────────────────────────────┤
│  math.pi     │  3.141592653589793            │  圆周率 π，圆的周长与直径之比     │
├──────────────┼───────────────────────────────┼──────────────────────────────────┤
│  math.e      │  2.718281828459045            │  自然常数，是自然对数的底数       │
├──────────────┼───────────────────────────────┼──────────────────────────────────┤
│  math.tau    │  6.283185307179586            │  τ = 2π，完整圆的弧度            │
├──────────────┼───────────────────────────────┼──────────────────────────────────┤
│  math.inf    │  inf                          │  正无穷大（float('inf')）         │
├──────────────┼───────────────────────────────┼──────────────────────────────────┤
│  math.nan    │  nan                          │  非数字（Not a Number）           │
└──────────────┴───────────────────────────────┴──────────────────────────────────┘
```

#### 示例代码

```python
import math

# 圆周率 π
print(math.pi)   # 3.141592653589793
print(math.tau)  # 6.283185307179586（等于 2π）

# 自然常数 e
print(math.e)    # 2.718281828459045

# 无穷大
print(math.inf)         # inf
print(-math.inf)        # -inf
print(math.inf > 10**9) # True（比任何有限数都大）

# 检查是否为无穷大
print(math.isinf(math.inf))   # True
print(math.isinf(1000))       # False

# NaN（非数字）
print(math.nan)               # nan
# NaN 的特性：与任何数（包括自身）比较都返回 False
print(math.nan == math.nan)   # False（！）
# 正确检查 NaN 的方式
print(math.isnan(math.nan))   # True
print(math.isnan(3.14))       # False

# 实际应用：用 inf 表示"尚未找到最小值"
distances = [5.2, 3.1, 8.7, 2.4, 6.0]
min_distance = math.inf
for d in distances:
    if d < min_distance:
        min_distance = d
print(f"最短距离：{min_distance}")  # 最短距离：2.4
```

---

## 第八部分：综合示例

### 8.1 计算圆的面积与周长

#### 概念说明

圆是最基本的几何图形之一，其面积和周长公式都涉及 π。

#### 示例代码

```python
import math

def circle_area(radius):
    """计算圆的面积：S = π × r²"""
    if radius < 0:
        raise ValueError("半径不能为负数")
    return math.pi * radius ** 2

def circle_perimeter(radius):
    """计算圆的周长：C = 2π × r"""
    if radius < 0:
        raise ValueError("半径不能为负数")
    return math.tau * radius  # tau = 2π

# 测试
r = 5
print(f"半径为 {r} 的圆：")
print(f"  面积   = {circle_area(r):.4f}")       # 面积   = 78.5398
print(f"  周长   = {circle_perimeter(r):.4f}")  # 周长   = 31.4159

# 球的体积：V = (4/3) × π × r³
def sphere_volume(radius):
    """计算球的体积"""
    return (4/3) * math.pi * radius ** 3

r = 3
print(f"\n半径为 {r} 的球：")
print(f"  体积 = {sphere_volume(r):.4f}")  # 体积 = 113.0973
```

### 8.2 计算两点之间的距离

#### 概念说明

平面内两点 A(x1, y1) 和 B(x2, y2) 之间的距离公式（欧几里得距离）：

```
d = √[(x2-x1)² + (y2-y1)²]
```

Python 3.8+ 中 `math.dist()` 直接支持此计算。

#### 示例代码

```python
import math

# 方法一：手动实现
def euclidean_distance(x1, y1, x2, y2):
    """计算平面两点间的欧几里得距离"""
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# 方法二：使用 math.dist（Python 3.8+）
def distance_v2(point_a, point_b):
    """使用 math.dist 计算两点距离"""
    return math.dist(point_a, point_b)

# 测试
A = (0, 0)
B = (3, 4)
print(f"A{A} 到 B{B} 的距离：{euclidean_distance(*A, *B)}")  # 5.0
print(f"A{A} 到 B{B} 的距离：{distance_v2(A, B)}")          # 5.0

# 三维空间中的距离（math.dist 支持任意维度）
P1 = (1, 2, 3)
P2 = (4, 6, 3)
print(f"三维距离：{math.dist(P1, P2):.4f}")  # 三维距离：5.0000

# 实际应用：找出离原点最近的点
points = [(3, 4), (1, 1), (6, 8), (2, 2)]
origin = (0, 0)
closest = min(points, key=lambda p: math.dist(p, origin))
print(f"离原点最近的点：{closest}")  # 离原点最近的点：(1, 1)
```

### 8.3 海伦公式计算三角形面积

#### 概念说明

已知三角形三条边 a、b、c，可以用**海伦公式（Heron's Formula）**计算面积：

```
s = (a + b + c) / 2   （半周长）
面积 = √[s × (s-a) × (s-b) × (s-c)]
```

#### 示例代码

```python
import math

def heron_area(a, b, c):
    """
    用海伦公式计算三角形面积
    参数：三条边的长度
    返回：面积，若三边不能构成三角形则返回 None
    """
    # 验证三角形不等式
    if a + b <= c or a + c <= b or b + c <= a:
        print(f"错误：边 {a}, {b}, {c} 不能构成三角形")
        return None

    s = (a + b + c) / 2  # 半周长
    area = math.sqrt(s * (s - a) * (s - b) * (s - c))
    return area

# 测试案例
print(heron_area(3, 4, 5))    # 6.0（直角三角形）
print(heron_area(5, 5, 5))    # 10.825...（等边三角形）
print(heron_area(1, 2, 10))   # 不能构成三角形

# 验证：等边三角形面积公式 S = (√3/4) × a²
a = 5
standard_formula = (math.sqrt(3) / 4) * a**2
heron_result = heron_area(a, a, a)
print(f"等边三角形（边={a}）面积：{standard_formula:.4f}")  # 10.8253
print(f"海伦公式结果：{heron_result:.4f}")                  # 10.8253
```

### 8.4 勾股定理验证与应用

#### 概念说明

勾股定理：直角三角形中，两条直角边 a、b 与斜边 c 满足 `a² + b² = c²`。

#### 示例代码

```python
import math

def is_right_triangle(a, b, c):
    """
    验证三条边是否构成直角三角形
    注意：使用 math.isclose 而非 == 比较浮点数
    """
    sides = sorted([a, b, c])  # 最大的边应该是斜边
    a, b, c = sides[0], sides[1], sides[2]
    return math.isclose(a**2 + b**2, c**2, rel_tol=1e-9)

# 经典勾股数
print(is_right_triangle(3, 4, 5))    # True
print(is_right_triangle(5, 12, 13))  # True
print(is_right_triangle(3, 4, 6))    # False

# 实际应用：求直角三角形斜边
def hypotenuse(a, b):
    """已知两直角边，求斜边"""
    return math.hypot(a, b)  # math.hypot 是专门的斜边计算函数

print(f"3-4-? 的斜边：{hypotenuse(3, 4)}")    # 5.0
print(f"5-12-? 的斜边：{hypotenuse(5, 12)}")  # 13.0

# math.hypot 也支持多维（Python 3.8+）
# 三维空间中从原点到 (3, 4, 0) 的距离
dist_3d = math.hypot(3, 4, 0)
print(f"三维斜边：{dist_3d}")  # 5.0
```

---

## 第九部分：常用函数速查表

```
┌──────────────────────┬────────────────────────────────┬────────────────────────────┐
│  函数/常量            │  说明                          │  示例                      │
├──────────────────────┼────────────────────────────────┼────────────────────────────┤
│  math.sqrt(x)        │  x 的平方根                    │  sqrt(9)  → 3.0            │
│  math.pow(x, y)      │  x 的 y 次幂（返回浮点数）      │  pow(2,3) → 8.0            │
│  math.fabs(x)        │  x 的绝对值（返回浮点数）       │  fabs(-3) → 3.0            │
│  math.factorial(n)   │  n 的阶乘                      │  factorial(5) → 120        │
│  math.gcd(a, b)      │  最大公约数                    │  gcd(12,8) → 4             │
│  math.lcm(a, b)      │  最小公倍数（3.9+）            │  lcm(4,6) → 12             │
├──────────────────────┼────────────────────────────────┼────────────────────────────┤
│  math.ceil(x)        │  向上取整                      │  ceil(2.3) → 3             │
│  math.floor(x)       │  向下取整                      │  floor(2.3) → 2            │
│  math.trunc(x)       │  截断小数（朝零取整）           │  trunc(-2.9) → -2          │
├──────────────────────┼────────────────────────────────┼────────────────────────────┤
│  math.sin(x)         │  正弦（x 为弧度）              │  sin(π/2) → 1.0            │
│  math.cos(x)         │  余弦（x 为弧度）              │  cos(0) → 1.0              │
│  math.tan(x)         │  正切（x 为弧度）              │  tan(π/4) → 1.0            │
│  math.asin(x)        │  反正弦，返回弧度              │  asin(1) → π/2             │
│  math.acos(x)        │  反余弦，返回弧度              │  acos(0) → π/2             │
│  math.atan(x)        │  反正切，返回弧度              │  atan(1) → π/4             │
│  math.atan2(y, x)    │  双参数反正切                  │  atan2(1,1) → π/4          │
│  math.radians(deg)   │  角度转弧度                    │  radians(180) → π          │
│  math.degrees(rad)   │  弧度转角度                    │  degrees(π) → 180.0        │
├──────────────────────┼────────────────────────────────┼────────────────────────────┤
│  math.log(x)         │  自然对数 ln(x)                │  log(e) → 1.0              │
│  math.log2(x)        │  以 2 为底的对数               │  log2(8) → 3.0             │
│  math.log10(x)       │  以 10 为底的对数              │  log10(100) → 2.0          │
│  math.log(x, base)   │  以 base 为底的对数            │  log(8,2) → 3.0            │
│  math.exp(x)         │  e 的 x 次幂                   │  exp(1) → 2.718...         │
├──────────────────────┼────────────────────────────────┼────────────────────────────┤
│  math.hypot(*coords) │  欧几里得范数（斜边）          │  hypot(3,4) → 5.0          │
│  math.dist(p, q)     │  两点间距离（3.8+）            │  dist([0,0],[3,4]) → 5.0   │
│  math.isclose(a, b)  │  判断两浮点数是否近似相等       │  isclose(0.1+0.2, 0.3)     │
│  math.isinf(x)       │  判断是否为无穷大              │  isinf(inf) → True         │
│  math.isnan(x)       │  判断是否为 NaN                │  isnan(nan) → True         │
├──────────────────────┼────────────────────────────────┼────────────────────────────┤
│  math.pi             │  圆周率 π ≈ 3.14159...         │  常量，直接使用             │
│  math.e              │  自然常数 e ≈ 2.71828...       │  常量，直接使用             │
│  math.tau            │  τ = 2π ≈ 6.28318...           │  常量，直接使用             │
│  math.inf            │  正无穷大                      │  常量，直接使用             │
│  math.nan            │  非数字 NaN                    │  常量，直接使用             │
└──────────────────────┴────────────────────────────────┴────────────────────────────┘
```

---

## 第十部分：常见错误与注意事项

### 10.1 忘记导入模块

#### 概念说明

这是最常见的错误：直接使用 `sqrt()`、`pi` 等，而没有先 `import math`。

#### 示例代码

```python
# 错误示例
# print(sqrt(9))  # NameError: name 'sqrt' is not defined
# print(pi)       # NameError: name 'pi' is not defined

# 正确做法一：整体导入
import math
print(math.sqrt(9))  # 3.0
print(math.pi)       # 3.141592653589793

# 正确做法二：按需导入
from math import sqrt, pi
print(sqrt(9))  # 3.0
print(pi)       # 3.141592653589793
```

### 10.2 向负数求平方根

#### 概念说明

`math.sqrt()` 只处理实数，对负数会抛出 `ValueError`。如果需要计算复数的平方根，应使用 `cmath` 模块（复数数学模块）。

#### 示例代码

```python
import math

# 错误：对负数求平方根
try:
    result = math.sqrt(-1)
except ValueError as e:
    print(f"ValueError: {e}")  # math domain error

# 正确：使用 cmath 处理复数
import cmath
result = cmath.sqrt(-1)
print(result)           # 1j（虚数单位 i）
print(result ** 2)      # (-1+0j)（验证：i² = -1）
```

### 10.3 浮点数精度问题

#### 概念说明

三角函数、对数函数等的计算结果可能存在浮点误差。`math.sin(math.pi)` 在数学上应该等于 0，但实际上返回一个极小的非零数。比较浮点数时，应使用 `math.isclose()` 而不是 `==`。

#### 示例代码

```python
import math

# 浮点误差示例
print(math.sin(math.pi))    # 1.2246467991473532e-16（不是精确的 0）
print(math.cos(math.pi/2))  # 6.123233995736766e-17（不是精确的 0）

# 错误：直接用 == 比较
print(math.sin(math.pi) == 0)   # False（！！）

# 正确：用 isclose 比较
print(math.isclose(math.sin(math.pi), 0, abs_tol=1e-10))  # True

# 另一个常见例子
print(0.1 + 0.2)                      # 0.30000000000000004
print(0.1 + 0.2 == 0.3)              # False
print(math.isclose(0.1 + 0.2, 0.3))  # True
```

### 10.4 角度与弧度混淆

#### 概念说明

Python 的三角函数接受**弧度**，不接受角度。直接把角度值传给 `sin/cos/tan` 是最常见的错误之一。

#### 示例代码

```python
import math

angle_degrees = 90

# 错误：直接传入角度（得到错误结果）
wrong_result = math.sin(90)
print(f"sin(90)（错误）= {wrong_result:.6f}")  # sin(90)（错误）= 0.893997（不是 1.0！）

# 正确：先转换为弧度
correct_result = math.sin(math.radians(90))
print(f"sin(90°)（正确）= {correct_result:.6f}")  # sin(90°)（正确）= 1.000000

# 记住这个口诀：
# "先 radians，再三角" 或 "三角函数吃弧度"
```

### 10.5 log 的输入限制

#### 概念说明

对数函数要求输入值**严格大于 0**。输入 0 或负数会抛出异常。

#### 示例代码

```python
import math

# 错误：log(0) 趋向负无穷
try:
    math.log(0)
except ValueError as e:
    print(f"ValueError: {e}")  # math domain error

# 错误：log(-1) 无意义（实数范围）
try:
    math.log(-1)
except ValueError as e:
    print(f"ValueError: {e}")  # math domain error

# 正确做法：在计算前检查输入
def safe_log(x, base=None):
    """安全的对数计算，带输入验证"""
    if x <= 0:
        raise ValueError(f"对数的输入必须大于 0，当前输入：{x}")
    if base is None:
        return math.log(x)
    else:
        if base <= 0 or base == 1:
            raise ValueError(f"对数的底数必须大于 0 且不等于 1，当前底数：{base}")
        return math.log(x, base)

print(safe_log(100, 10))   # 2.0
print(safe_log(math.e))    # 1.0
```

### 10.6 factorial 只接受非负整数

#### 概念说明

`math.factorial()` 只接受**非负整数**。浮点数或负数都会引发异常。

#### 示例代码

```python
import math

# 错误：浮点数
try:
    math.factorial(5.0)
except TypeError as e:
    print(f"TypeError: {e}")  # 'float' object cannot be interpreted as an integer

# 错误：负整数
try:
    math.factorial(-1)
except ValueError as e:
    print(f"ValueError: {e}")  # factorial() not defined for negative values

# 正确
print(math.factorial(5))   # 120
print(math.factorial(0))   # 1
print(math.factorial(10))  # 3628800

# 如果输入可能是浮点数，先转换
def safe_factorial(n):
    n = int(n)  # 先转换为整数
    if n < 0:
        raise ValueError("阶乘不支持负数")
    return math.factorial(n)

print(safe_factorial(5.0))  # 120
```

---

## 总结

`math` 模块是 Python 科学计算的基础。以下是本章的关键要点：

```
┌───────────────────────────────────────────────────────────────┐
│  核心要点回顾                                                  │
├──────────────────────────────────────────────────────────────┤
│ 1. 使用前必须 import math                                     │
│ 2. 三角函数使用弧度，用 math.radians() 转换角度               │
│ 3. ceil/floor/trunc 对负数的行为要特别注意                    │
│ 4. 比较浮点数用 math.isclose()，不要用 ==                     │
│ 5. sqrt/log 对无效输入会抛出 ValueError，需要做输入验证       │
│ 6. math.pi、math.e 等常量已预定义，直接使用即可               │
└───────────────────────────────────────────────────────────────┘
```

学完本章后，你已经掌握了 Python 数学运算的核心工具。在实际项目中，`math` 模块是几何计算、物理模拟、数据分析的基础依赖之一。

---

[返回索引](../README.md) | [返回 11-模块与包](../11-模块与包.md)
