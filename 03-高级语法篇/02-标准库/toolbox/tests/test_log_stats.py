"""LogStats测试 - math和random模块"""

import math

from app.core.log_stats import (
    LogStats,
    calculate_mean,
    calculate_percentile,
    calculate_std_dev,
    random_sample,
    weighted_choice,
)


class TestLogStats:
    def test_create_stats(self):
        stats = LogStats([1.0, 2.0, 3.0, 4.0, 5.0])
        assert len(stats.values) == 5

    def test_mean(self):
        stats = LogStats([1.0, 2.0, 3.0, 4.0, 5.0])
        assert stats.mean() == 3.0

    def test_std_dev(self):
        stats = LogStats([2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0])
        assert abs(stats.std_dev() - 2.0) < 0.01

    def test_variance(self):
        stats = LogStats([1.0, 2.0, 3.0])
        expected_var = 0.666
        assert abs(stats.variance() - expected_var) < 0.01

    def test_min_max(self):
        stats = LogStats([1.0, 5.0, 10.0])
        assert stats.min() == 1.0
        assert stats.max() == 10.0

    def test_range(self):
        stats = LogStats([1.0, 5.0, 10.0])
        assert stats.range() == 9.0

    def test_median(self):
        stats = LogStats([1.0, 3.0, 5.0, 7.0, 9.0])
        assert stats.median() == 5.0

    def test_median_even_count(self):
        stats = LogStats([1.0, 2.0, 3.0, 4.0])
        assert stats.median() == 2.5

    def test_percentile(self):
        stats = LogStats([1.0, 2.0, 3.0, 4.0, 5.0])
        assert stats.percentile(50) == 3.0
        assert stats.percentile(25) == 2.0

    def test_round_to_int(self):
        stats = LogStats([1.5, 2.5, 3.5])
        rounded = stats.round_to_int(2.7)
        assert rounded == 3

    def test_ceil(self):
        stats = LogStats([1.0])
        assert stats.ceil(2.1) == 3

    def test_floor(self):
        stats = LogStats([1.0])
        assert stats.floor(2.9) == 2

    def test_count(self):
        stats = LogStats([1.0, 2.0, 3.0])
        assert stats.count() == 3

    def test_sum(self):
        stats = LogStats([1.0, 2.0, 3.0])
        assert stats.sum() == 6.0


class TestCalculateMean:
    def test_calculate_mean(self):
        assert calculate_mean([1, 2, 3, 4, 5]) == 3.0

    def test_calculate_mean_empty(self):
        assert calculate_mean([]) == 0.0

    def test_calculate_mean_single(self):
        assert calculate_mean([5]) == 5.0


class TestCalculateStdDev:
    def test_calculate_std_dev(self):
        std = calculate_std_dev([2, 4, 4, 4, 5, 5, 7, 9])
        assert abs(std - 2.0) < 0.01

    def test_calculate_std_dev_empty(self):
        assert calculate_std_dev([]) == 0.0


class TestCalculatePercentile:
    def test_calculate_percentile_50(self):
        values = [1, 2, 3, 4, 5]
        assert calculate_percentile(values, 50) == 3

    def test_calculate_percentile_25(self):
        values = [1, 2, 3, 4, 5]
        assert calculate_percentile(values, 25) == 2


class TestRandomSample:
    def test_random_sample(self):
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        sample = random_sample(values, 3)
        assert len(sample) == 3
        assert all(v in values for v in sample)

    def test_random_sample_all(self):
        values = [1, 2, 3]
        sample = random_sample(values, 3)
        assert len(sample) == 3

    def test_random_sample_too_large(self):
        values = [1, 2, 3]
        sample = random_sample(values, 5)
        assert len(sample) == 3


class TestWeightedChoice:
    def test_weighted_choice(self):
        items = ["a", "b", "c"]
        weights = [1, 2, 3]
        result = weighted_choice(items, weights)
        assert result in items

    def test_weighted_choice_single(self):
        items = ["a"]
        weights = [1]
        assert weighted_choice(items, weights) == "a"


class TestMathOperations:
    def test_sqrt(self):
        stats = LogStats([1.0])
        assert stats.sqrt(16) == 4.0

    def test_power(self):
        stats = LogStats([1.0])
        assert stats.power(2, 3) == 8.0

    def test_log(self):
        stats = LogStats([1.0])
        assert abs(stats.log(math.e) - 1.0) < 0.01

    def test_percentage(self):
        stats = LogStats([100.0])
        assert stats.percentage(25, 100) == 25.0

    def test_percentage_change(self):
        stats = LogStats([100.0])
        assert stats.percentage_change(100, 120) == 20.0
