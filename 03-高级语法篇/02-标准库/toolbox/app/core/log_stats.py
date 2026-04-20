"""日志统计模块 - math和random模块示例

演示math和random模块的核心功能:
- 统计计算 (math.sqrt/ceil/floor)
- 百分比计算
- 随机采样 (random.sample/choice)
- 随机打乱 (random.shuffle)
"""

import math
import random
from collections.abc import Sequence


class LogStats:
    """日志统计计算器"""

    def __init__(self, values: Sequence[float]):
        self.values = list(values)

    def mean(self) -> float:
        """计算平均值"""
        if not self.values:
            return 0.0
        return sum(self.values) / len(self.values)

    def variance(self) -> float:
        """计算方差"""
        if len(self.values) < 2:
            return 0.0
        mean_val = self.mean()
        return sum((x - mean_val) ** 2 for x in self.values) / len(self.values)

    def std_dev(self) -> float:
        """计算标准差"""
        return self.sqrt(self.variance())

    def min(self) -> float:
        """最小值"""
        return min(self.values) if self.values else 0.0

    def max(self) -> float:
        """最大值"""
        return max(self.values) if self.values else 0.0

    def range(self) -> float:
        """范围"""
        return self.max() - self.min()

    def median(self) -> float:
        """中位数"""
        sorted_vals = sorted(self.values)
        n = len(sorted_vals)
        if n == 0:
            return 0.0
        if n % 2 == 1:
            return sorted_vals[n // 2]
        return (sorted_vals[n // 2 - 1] + sorted_vals[n // 2]) / 2

    def percentile(self, p: float) -> float:
        """计算百分位数"""
        sorted_vals = sorted(self.values)
        n = len(sorted_vals)
        if n == 0:
            return 0.0
        index = (p / 100) * (n - 1)
        lower = int(self.floor(index))
        upper = int(self.ceil(index))
        if lower == upper:
            return sorted_vals[lower]
        weight = index - lower
        return sorted_vals[lower] * (1 - weight) + sorted_vals[upper] * weight

    def count(self) -> int:
        """计数"""
        return len(self.values)

    def sum(self) -> float:
        """求和"""
        return sum(self.values)

    def sqrt(self, value: float) -> float:
        """平方根"""
        return math.sqrt(value)

    def power(self, base: float, exp: float) -> float:
        """幂运算"""
        return math.pow(base, exp)

    def log(self, value: float) -> float:
        """自然对数"""
        return math.log(value)

    def ceil(self, value: float) -> int:
        """向上取整"""
        return math.ceil(value)

    def floor(self, value: float) -> int:
        """向下取整"""
        return math.floor(value)

    def round_to_int(self, value: float) -> int:
        """四舍五入"""
        return round(value)

    def percentage(self, part: float, total: float) -> float:
        """计算百分比"""
        if total == 0:
            return 0.0
        return (part / total) * 100

    def percentage_change(self, old: float, new: float) -> float:
        """计算变化百分比"""
        if old == 0:
            return 0.0
        return ((new - old) / old) * 100

    def random_sample(self, k: int) -> list[float]:
        """随机采样"""
        return random_sample(self.values, k)


def calculate_mean(values: Sequence[float]) -> float:
    """计算平均值

    Args:
        values: 数值序列

    Returns:
        平均值
    """
    if not values:
        return 0.0
    return sum(values) / len(values)


def calculate_std_dev(values: Sequence[float]) -> float:
    """计算标准差

    Args:
        values: 数值序列

    Returns:
        标准差
    """
    if len(values) < 2:
        return 0.0
    mean_val = calculate_mean(values)
    variance = sum((x - mean_val) ** 2 for x in values) / len(values)
    return math.sqrt(variance)


def calculate_percentile(values: Sequence[float], p: float) -> float:
    """计算百分位数

    Args:
        values: 数值序列
        p: 百分位 (0-100)

    Returns:
        百分位数值
    """
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    if n == 0:
        return 0.0
    index = (p / 100) * (n - 1)
    lower = int(math.floor(index))
    upper = int(math.ceil(index))
    if lower == upper:
        return sorted_vals[lower]
    weight = index - lower
    return sorted_vals[lower] * (1 - weight) + sorted_vals[upper] * weight


def random_sample(values: Sequence, k: int) -> list:
    """随机采样

    Args:
        values: 序列
        k: 采样数量

    Returns:
        采样结果
    """
    if k >= len(values):
        return list(values)
    return random.sample(list(values), k)


def weighted_choice(items: Sequence, weights: Sequence[float]) -> any:
    """加权随机选择

    Args:
        items: 选项序列
        weights: 权重序列

    Returns:
        随机选择的结果
    """
    if len(items) == 1:
        return items[0]
    return random.choices(items, weights=weights, k=1)[0]
