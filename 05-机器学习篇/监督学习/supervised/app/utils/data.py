"""数据处理"""

import numpy as np


def generate_data(n_samples: int = 100) -> tuple:
    """生成示例数据"""
    np.random.seed(42)
    X = np.random.randn(n_samples, 2)
    y = (X[:, 0] + X[:, 1] > 0).astype(int)
    return X, y