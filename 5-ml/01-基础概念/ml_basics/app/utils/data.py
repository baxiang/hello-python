"""数据处理"""

import numpy as np


def normalize(X: np.ndarray) -> np.ndarray:
    """标准化"""
    mean = np.mean(X, axis=0)
    std = np.std(X, axis=0)
    return (X - mean) / (std + 1e-8)


def one_hot_encode(y: np.ndarray, num_classes: int = None) -> np.ndarray:
    """独热编码"""
    if num_classes is None:
        num_classes = len(np.unique(y))
    
    one_hot = np.zeros((len(y), num_classes))
    one_hot[np.arange(len(y)), y] = 1
    return one_hot