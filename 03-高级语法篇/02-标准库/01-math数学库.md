# math 模块参考

Python math 模块提供数学函数和常量。

---

## 数学常量

```python
import math

print(math.pi)      # 3.141592653589793（圆周率）
print(math.e)       # 2.718281828459045（自然常数）
print(math.inf)     # inf（正无穷）
print(math.nan)     # nan（非数字）
print(math.tau)     # 6.283185307179586（2π）
```

---

## 基本函数

### 幂与对数

```python
import math

# 幂运算
print(math.pow(2, 3))    # 8.0（2 的 3 次方）
print(math.sqrt(16))     # 4.0（平方根）
print(math.cbrt(27))     # 3.0（立方根，Python 3.11+）

# 对数
print(math.log(math.e))  # 1.0（自然对数）
print(math.log10(100))   # 2.0（以 10 为底）
print(math.log2(8))      # 3.0（以 2 为底）
print(math.log(100, 10)) # 2.0（指定底数）

# 指数
print(math.exp(1))       # 2.718281828459045（e 的 1 次方）
print(math.expm1(1))     # e^x - 1，精度更高
```

### 三角函数

```python
import math

# 弧度与角度转换
print(math.degrees(math.pi))  # 180.0（弧度转角度）
print(math.radians(180))      # 3.14159...（角度转弧度）

# 三角函数（参数为弧度）
print(math.sin(math.pi / 2))   # 1.0
print(math.cos(0))             # 1.0
print(math.tan(math.pi / 4))   # 0.9999... ≈ 1

# 反三角函数
print(math.asin(1))      # 1.5707...（π/2）
print(math.acos(0))      # 1.5707...（π/2）
print(math.atan(1))      # 0.7853...（π/4）

# 双曲函数
print(math.sinh(0))      # 0.0
print(math.cosh(0))      # 1.0
print(math.tanh(0))      # 0.0
```

### 取整与绝对值

```python
import math

# 绝对值
print(math.fabs(-5))     # 5.0（返回浮点数）

# 取整
print(math.ceil(3.2))    # 4（向上取整）
print(math.floor(3.8))   # 3（向下取整）
print(math.trunc(3.8))   # 3（截断小数部分）

# 四舍五入
print(round(3.5))        # 4（内置函数）
print(round(3.4))        # 3

# 取余
print(math.fmod(7, 3))   # 1.0（浮点取余）
print(math.remainder(7, 3))  # -2.0（IEEE 754 取余）
```

---

## 特殊函数

### 阶乘与组合

```python
import math

# 阶乘
print(math.factorial(5))  # 120（5! = 5×4×3×2×1）

# 组合数 C(n, k)
print(math.comb(5, 2))    # 10（从 5 个中选 2 个）

# 排列数 P(n, k)
print(math.perm(5, 2))    # 20（从 5 个中选 2 个排列）
```

### 最大公约数与最小公倍数

```python
import math

# 最大公约数
print(math.gcd(12, 8))    # 4
print(math.gcd(12, 8, 6)) # 2（多个数）

# 最小公倍数（Python 3.9+）
print(math.lcm(4, 6))     # 12
```

### 判断函数

```python
import math

# 判断是否有限
print(math.isfinite(1.0))    # True
print(math.isfinite(math.inf))  # False

# 判断是否无穷
print(math.isinf(math.inf))  # True

# 判断是否 NaN
print(math.isnan(math.nan))  # True

# 判断是否整数
print(math.isqrt(16))        # 4（整数平方根）
```

---

## 常用示例

### 计算圆的面积和周长

```python
import math

def circle_properties(radius):
    """计算圆的面积和周长"""
    area = math.pi * radius ** 2
    circumference = 2 * math.pi * radius
    return area, circumference

area, circ = circle_properties(5)
print(f"面积: {area:.2f}")        # 面积: 78.54
print(f"周长: {circ:.2f}")        # 周长: 31.42
```

### 计算两点距离

```python
import math

def distance(x1, y1, x2, y2):
    """计算两点之间的距离"""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

dist = distance(0, 0, 3, 4)
print(f"距离: {dist}")  # 距离: 5.0
```

### 勾股数判断

```python
import math

def is_pythagorean_triple(a, b, c):
    """判断是否为勾股数"""
    return a**2 + b**2 == c**2

print(is_pythagorean_triple(3, 4, 5))  # True
print(is_pythagorean_triple(5, 12, 13))  # True
```