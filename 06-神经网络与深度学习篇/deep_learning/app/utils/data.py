"""数据处理"""

import numpy as np


def generate_xor_data(n_samples: int = 200) -> tuple:
    """生成 XOR 数据"""
    X = np.random.randn(n_samples, 2)
    y = (X[:, 0] * X[:, 1] > 0).astype(int).reshape(-1, 1)
    return X, y


def generate_circle_data(n_samples: int = 200) -> tuple:
    """生成圆形数据"""
    X = np.random.randn(n_samples, 2) * 2
    y = (np.sqrt(X[:, 0] ** 2 + X[:, 1] ** 2) < 1).astype(int).reshape(-1, 1)
    return X, y