# 数据工具

"""
深度学习数据工具
包含：数据加载、预处理、批处理
"""

import numpy as np
from typing import Tuple, Generator


def one_hot_encode(y: np.ndarray, num_classes: int = None) -> np.ndarray:
    """独热编码"""
    if num_classes is None:
        num_classes = len(np.unique(y))
    
    one_hot = np.zeros((len(y), num_classes))
    one_hot[np.arange(len(y)), y] = 1
    return one_hot


def normalize(x: np.ndarray, axis: int = None) -> np.ndarray:
    """标准化"""
    mean = np.mean(x, axis=axis, keepdims=True)
    std = np.std(x, axis=axis, keepdims=True)
    return (x - mean) / (std + 1e-8)


def train_test_split(
    X: np.ndarray,
    y: np.ndarray,
    test_size: float = 0.2,
    random_state: int = None
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """划分训练集和测试集"""
    if random_state:
        np.random.seed(random_state)
    
    n_samples = len(X)
    indices = np.random.permutation(n_samples)
    
    test_count = int(n_samples * test_size)
    test_indices = indices[:test_count]
    train_indices = indices[test_count:]
    
    return X[train_indices], X[test_indices], y[train_indices], y[test_indices]


def batch_generator(
    X: np.ndarray,
    y: np.ndarray,
    batch_size: int = 32,
    shuffle: bool = True
) -> Generator[Tuple[np.ndarray, np.ndarray], None, None]:
    """批量数据生成器"""
    n_samples = len(X)
    indices = np.arange(n_samples)
    
    if shuffle:
        np.random.shuffle(indices)
    
    for start in range(0, n_samples, batch_size):
        end = min(start + batch_size, n_samples)
        batch_indices = indices[start:end]
        yield X[batch_indices], y[batch_indices]


def generate_spiral_data(
    n_samples: int = 100,
    n_classes: int = 2,
    noise: float = 0.2
) -> Tuple[np.ndarray, np.ndarray]:
    """生成螺旋数据"""
    X = np.zeros((n_samples * n_classes, 2))
    y = np.zeros(n_samples * n_classes, dtype=int)
    
    for class_idx in range(n_classes):
        start = class_idx * n_samples
        end = start + n_samples
        
        r = np.linspace(0, 1, n_samples)
        t = np.linspace(class_idx * 4, (class_idx + 1) * 4, n_samples) + np.random.randn(n_samples) * noise
        
        X[start:end] = np.c_[r * np.sin(t * 2.5), r * np.cos(t * 2.5)]
        y[start:end] = class_idx
    
    return X, y


def generate_xor_data(n_samples: int = 200) -> Tuple[np.ndarray, np.ndarray]:
    """生成 XOR 数据"""
    X = np.random.randn(n_samples, 2)
    y = (X[:, 0] * X[:, 1] > 0).astype(int)
    return X, y


def generate_circle_data(
    n_samples: int = 200,
    noise: float = 0.1
) -> Tuple[np.ndarray, np.ndarray]:
    """生成圆形数据"""
    X = np.random.randn(n_samples, 2) * 2
    y = (np.sqrt(X[:, 0] ** 2 + X[:, 1] ** 2) < 1).astype(int)
    X += np.random.randn(n_samples, 2) * noise
    return X, y