"""数据处理"""

import numpy as np


def generate_clusters(n_samples: int = 100, n_clusters: int = 3) -> np.ndarray:
    """生成聚类数据"""
    np.random.seed(42)
    data = []
    for _ in range(n_clusters):
        center = np.random.randn(2) * 3
        cluster = np.random.randn(n_samples // n_clusters, 2) + center
        data.append(cluster)
    return np.vstack(data)