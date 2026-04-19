# math 数学库

> Python 3.11+

---

## 为什么需要 math 模块？

### 问题场景

你需要计算圆的面积、判断一个数是否为 NaN、或者做对数变换：

```python
# ❌ 自己定义常量：精度不够，出错风险高
PI = 3.14159
area = PI * r ** 2

# ✅ 用 math 模块：精确到 15 位有效数字，覆盖所有数学函数
import math
area = math.pi * r ** 2      # math.pi = 3.141592653589793
math.isnan(x)                # 判断 NaN，不能用 x == float('nan')
math.log2(n)                 # 以 2 为底的对数，比 math.log(n, 2) 精度更高
```

`math` 模块提供 C 语言级别的数学运算，精度高、速度快，是科学计算的基础工具。

---

## 章节导航

| 部分 | 内容 |
|------|------|
| 第一部分 | 数学常量、幂对数、三角函数、取整与绝对值 |
| 第二部分 | 阶乘与组合、最大公约数、判断函数 |
| 第三部分 | 实际应用（圆面积、距离、勾股数） |
| L2 实践层 | 推荐做法、反模式、常见陷阱、适用场景 |

---

## 第一部分：数学计算基础

### 1.1 数学常量

#### 实际场景

在科学计算、工程应用或游戏开发中，经常需要使用精确的数学常量。比如计算圆的面积需要 π，计算复利需要自然常数 e。

**问题：如何获取精确的数学常量，而不是自己定义可能不精确的值？**

```python
import math

print(math.pi)      # 3.141592653589793（圆周率）
print(math.e)       # 2.718281828459045（自然常数）
print(math.inf)     # inf（正无穷）
print(math.nan)     # nan（非数字）
print(math.tau)     # 6.283185307179586（2π）
```

### 1.2 幂与对数运算

#### 实际场景

在数据分析中，经常需要进行指数增长计算、对数变换等操作。比如计算复利、信号处理中的对数变换、计算机科学的二进制对数等。

**问题：Python 内置的 `**` 运算符和 `math.pow()` 有什么区别？如何选择合适的对数函数？**

```python
import math

# 幂运算
result: float = math.pow(2, 3)    # 8.0（2 的 3 次方）
root: float = math.sqrt(16)       # 4.0（平方根）
cbrt: float = math.cbrt(27)       # 3.0（立方根，Python 3.11+）

# 对数
natural_log: float = math.log(math.e)   # 1.0（自然对数）
log_10: float = math.log10(100)         # 2.0（以 10 为底）
log_2: float = math.log2(8)             # 3.0（以 2 为底）
custom_log: float = math.log(100, 10)   # 2.0（指定底数）

# 指数
exp_result: float = math.exp(1)      # 2.718281828459045（e 的 1 次方）
expm1_result: float = math.expm1(1)  # e^x - 1，精度更高
```

### 1.3 三角函数

#### 实际场景

在图形学、物理模拟、游戏开发中，三角函数是基础工具。比如计算物体运动轨迹、旋转变换、波形处理等。

**问题：Python 三角函数使用弧度还是角度？如何进行角度和弧度的转换？**

```python
import math

# 弧度与角度转换
degrees_result: float = math.degrees(math.pi)  # 180.0（弧度转角度）
radians_result: float = math.radians(180)      # 3.14159...（角度转弧度）

# 三角函数（参数为弧度）
sin_val: float = math.sin(math.pi / 2)   # 1.0
cos_val: float = math.cos(0)              # 1.0
tan_val: float = math.tan(math.pi / 4)    # 0.9999... ≈ 1

# 反三角函数
asin_val: float = math.asin(1)    # 1.5707...（π/2）
acos_val: float = math.acos(0)    # 1.5707...（π/2）
atan_val: float = math.atan(1)    # 0.7853...（π/4）

# 双曲函数
sinh_val: float = math.sinh(0)    # 0.0
cosh_val: float = math.cosh(0)    # 1.0
tanh_val: float = math.tanh(0)    # 0.0
```

### 1.4 取整与绝对值

#### 实际场景

在金融计算、数据分析中，经常需要控制数值精度。比如货币计算需要精确到分，统计分析需要确定的数据舍入方式。

**问题：`math.ceil()`、`math.floor()`、`round()` 有什么区别？什么时候用哪个？**

```python
import math

# 绝对值
abs_value: float = math.fabs(-5)     # 5.0（返回浮点数）

# 取整
ceil_value: int = math.ceil(3.2)     # 4（向上取整）
floor_value: int = math.floor(3.8)   # 3（向下取整）
trunc_value: int = math.trunc(3.8)   # 3（截断小数部分）

# 四舍五入（内置函数）
rounded_1: int = round(3.5)    # 4
rounded_2: int = round(3.4)     # 3

# 取余
fmod_result: float = math.fmod(7, 3)        # 1.0（浮点取余）
remainder: float = math.remainder(7, 3)      # -2.0（IEEE 754 取余）
```

## 第二部分：组合数学与判断函数

### 2.1 阶乘与组合

#### 实际场景

在概率统计、算法分析、密码学中，阶乘和组合数是常见运算。比如计算排列组合、分析时间复杂度、生成密码组合等。

**问题：如何高效计算大数的阶乘和组合数？**

```python
import math

# 阶乘
factorial_5: int = math.factorial(5)  # 120（5! = 5×4×3×2×1）

# 组合数 C(n, k)
comb_5_2: int = math.comb(5, 2)    # 10（从 5 个中选 2 个）

# 排列数 P(n, k)
perm_5_2: int = math.perm(5, 2)    # 20（从 5 个中选 2 个排列）
```

### 2.2 最大公约数与最小公倍数

#### 实际场景

在数学计算、分数化简、密码学算法中，需要计算最大公约数和最小公倍数。比如化简分数、RSA 加密算法等。

**问题：如何快速计算多个数的最大公约数和最小公倍数？**

```python
import math

# 最大公约数
gcd_2: int = math.gcd(12, 8)      # 4
gcd_multi: int = math.gcd(12, 8, 6)  # 2（多个数）

# 最小公倍数（Python 3.9+）
lcm_result: int = math.lcm(4, 6)   # 12
```

### 2.3 判断函数

#### 实际场景

在数值计算中，需要判断数值的有效性。比如处理除法结果时检查是否为无穷大或 NaN，防止后续计算出错。

**问题：如何判断一个数是无穷大、NaN 还是有限数？**

```python
import math

# 判断是否有限
is_finite_1: bool = math.isfinite(1.0)       # True
is_finite_2: bool = math.isfinite(math.inf)  # False

# 判断是否无穷
is_infinite: bool = math.isinf(math.inf)  # True

# 判断是否 NaN
is_nan: bool = math.isnan(math.nan)  # True

# 判断是否整数平方根
sqrt_int: int = math.isqrt(16)  # 4（整数平方根）
```

## 第三部分：实际应用示例

### 3.1 计算圆的面积和周长

#### 实际场景

在图形计算、工程设计中，经常需要计算圆形的相关参数。

```python
import math

def circle_properties(radius: float) -> tuple[float, float]:
    """计算圆的面积和周长"""
    area: float = math.pi * radius ** 2
    circumference: float = 2 * math.pi * radius
    return area, circumference

area, circ = circle_properties(5)
print(f"面积: {area:.2f}")        # 面积: 78.54
print(f"周长: {circ:.2f}")        # 周长: 31.42
```

### 3.2 计算两点距离

#### 实际场景

在游戏开发、地理信息系统、数据分析中，经常需要计算两点之间的欧几里得距离。

```python
import math

def distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """计算两点之间的距离"""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

dist: float = distance(0, 0, 3, 4)
print(f"距离: {dist}")  # 距离: 5.0
```

### 3.3 勾股数判断

#### 实际场景

在数学教育和几何计算中，需要判断三个数是否构成勾股数（直角三角形边长）。

```python
import math

def is_pythagorean_triple(a: int, b: int, c: int) -> bool:
    """判断是否为勾股数"""
    return a**2 + b**2 == c**2

result1: bool = is_pythagorean_triple(3, 4, 5)     # True
result2: bool = is_pythagorean_triple(5, 12, 13)   # True
```

---

## L2 实践层：最佳实践

### 推荐做法

| 做法 | 原因 | 示例 |
|------|------|------|
| 用 `math.pi` 而非自定义常量 | 精确到 15 位，避免累积误差 | `math.pi * r ** 2` |
| 用 `math.isnan()` 判断 NaN | `float('nan') == float('nan')` 永远为 `False` | `math.isnan(x)` |
| 用 `math.log2()` / `math.log10()` 而非 `math.log(x, 2)` | 专用函数数值精度更高 | `math.log2(1024)` → `10.0` |
| 用 `math.hypot()` 计算距离 | 比手动 `sqrt(x²+y²)` 更准确，避免溢出 | `math.hypot(3, 4)` → `5.0` |
| 用 `math.comb()` / `math.perm()` 计算组合排列 | 内置实现，大整数无溢出 | `math.comb(10, 3)` → `120` |
| 向量/矩阵运算用 `numpy` | `math` 只处理标量，批量计算需换库 | `import numpy as np` |

### 实际应用示例

```python
import math

# 计算斜边（避免手写 sqrt(x²+y²) 的溢出问题）
hypotenuse: float = math.hypot(3, 4)   # 5.0

# 安全对数（避免 log(0) 报错）
def safe_log(x: float, base: float = math.e) -> float | None:
    if x <= 0:
        return None
    return math.log(x, base)

# 角度转弧度再计算
angle_deg = 45
sin_45: float = math.sin(math.radians(angle_deg))  # 0.7071...
```

### 反模式：不要这样做

```python
# ❌ 用 == 判断 NaN
x = float('nan')
if x == float('nan'):       # 永远是 False，逻辑错误
    print("是 NaN")

# ✅ 正确方式
if math.isnan(x):
    print("是 NaN")

# ❌ 用 math 处理数组（逐元素循环）
data = [1.0, 2.0, 3.0]
result = [math.sqrt(x) for x in data]   # 数据量大时极慢

# ✅ 大量数据用 numpy
import numpy as np
result = np.sqrt(np.array(data))

# ❌ math.pow(2, 3) 不如 2 ** 3
# math.pow 返回 float，** 支持整数幂，更快
x = math.pow(2, 3)   # 8.0（float）
x = 2 ** 3           # 8（int，更自然）
```

### 常见陷阱

| 陷阱 | 现象 | 解决方案 |
|------|------|---------|
| `math.sqrt(-1)` | `ValueError: math domain error` | 改用 `cmath.sqrt(-1)` 处理复数 |
| `math.log(0)` | `ValueError: math domain error` | 先判断 `x > 0` 再求对数 |
| `float('nan') == float('nan')` | 结果是 `False` | 用 `math.isnan()` |
| 三角函数输入角度 | `math.sin(90)` ≠ 1（参数是弧度） | 先 `math.radians(90)` 转换 |
| `math.pow` vs `**` | `math.pow(2,3)` 返回 `float`，`2**3` 返回 `int` | 整数幂用 `**`，浮点精确用 `math.pow` |

### 适用场景

| 场景 | 是否推荐 | 说明 |
|------|---------|------|
| 单个数值的数学计算 | ✅ 推荐 | 精度高、无需安装依赖 |
| 角度/弧度转换 | ✅ 推荐 | `degrees()`/`radians()` 标准方式 |
| 判断 NaN / 无穷 | ✅ 推荐 | 不能用 `==` 比较 |
| 大量数组运算 | ❌ 不适合 | 用 `numpy`，速度快 100 倍以上 |
| 复数运算 | ❌ 不适合 | 改用 `cmath` 模块 |

---

## 本章小结

```
┌──────────────────────────────────────────────────────────────┐
│                   math 模块 知识要点                          │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   常量：math.pi  math.e  math.inf  math.nan  math.tau        │
│                                                              │
│   幂对数：pow()  sqrt()  cbrt()  log()  log2()  log10()      │
│   三角函数：sin/cos/tan + 反三角 + degrees/radians 转换       │
│   取整：ceil()（上）floor()（下）trunc()（截断）              │
│   组合数学：factorial()  comb()  perm()  gcd()  lcm()        │
│   判断：isnan()  isinf()  isfinite()  isqrt()                │
│                                                              │
│   注意：                                                     │
│   三角函数参数是弧度，不是角度                                │
│   判断 NaN 必须用 isnan()，不能用 ==                         │
│   批量数组运算请改用 numpy                                    │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```