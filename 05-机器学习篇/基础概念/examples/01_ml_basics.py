# 机器学习基础概念示例

"""
机器学习基础概念示例
包含：数据集划分、交叉验证、评估指标
"""

import numpy as np
from typing import Tuple


# 1. 数据集划分
def train_test_split(
    X: np.ndarray,
    y: np.ndarray,
    test_size: float = 0.2,
    random_state: int = None
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    手动实现训练集/测试集划分
    
    Args:
        X: 特征矩阵
        y: 标签
        test_size: 测试集比例
        random_state: 随机种子
    """
    if random_state:
        np.random.seed(random_state)
    
    n_samples = len(X)
    indices = np.random.permutation(n_samples)
    
    test_count = int(n_samples * test_size)
    test_indices = indices[:test_count]
    train_indices = indices[test_count:]
    
    return X[train_indices], X[test_indices], y[train_indices], y[test_indices]


# 2. K折交叉验证
def k_fold_split(n_samples: int, k: int = 5):
    """
    K折交叉验证
    
    Args:
        n_samples: 样本数量
        k: 折数
    """
    indices = np.arange(n_samples)
    fold_size = n_samples // k
    
    for i in range(k):
        val_start = i * fold_size
        val_end = (i + 1) * fold_size if i < k - 1 else n_samples
        
        val_indices = indices[val_start:val_end]
        train_indices = np.concatenate([indices[:val_start], indices[val_end:]])
        
        yield train_indices, val_indices


# 3. 分类评估指标
def accuracy_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """准确率"""
    return np.mean(y_true == y_pred)


def precision_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """精确率"""
    true_positives = np.sum((y_pred == 1) & (y_true == 1))
    predicted_positives = np.sum(y_pred == 1)
    return true_positives / predicted_positives if predicted_positives > 0 else 0


def recall_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """召回率"""
    true_positives = np.sum((y_pred == 1) & (y_true == 1))
    actual_positives = np.sum(y_true == 1)
    return true_positives / actual_positives if actual_positives > 0 else 0


def f1_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """F1 分数"""
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    return 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0


def confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    """混淆矩阵"""
    classes = np.unique(np.concatenate([y_true, y_pred]))
    n_classes = len(classes)
    matrix = np.zeros((n_classes, n_classes), dtype=int)
    
    for i, c1 in enumerate(classes):
        for j, c2 in enumerate(classes):
            matrix[i, j] = np.sum((y_true == c1) & (y_pred == c2))
    
    return matrix


# 4. 回归评估指标
def mean_squared_error(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """均方误差"""
    return np.mean((y_true - y_pred) ** 2)


def mean_absolute_error(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """平均绝对误差"""
    return np.mean(np.abs(y_true - y_pred))


def r2_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """R² 分数"""
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return 1 - ss_res / ss_tot if ss_tot > 0 else 0


if __name__ == "__main__":
    print("=" * 40)
    print("机器学习基础概念示例")
    print("=" * 40)
    
    # 数据集划分
    print("\n【数据集划分】")
    X = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]])
    y = np.array([0, 0, 1, 1, 1])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)
    print(f"训练集: X={X_train.tolist()}, y={y_train.tolist()}")
    print(f"测试集: X={X_test.tolist()}, y={y_test.tolist()}")
    
    # K折交叉验证
    print("\n【K折交叉验证】")
    for i, (train_idx, val_idx) in enumerate(k_fold_split(10, k=5)):
        print(f"Fold {i+1}: train={train_idx.tolist()}, val={val_idx.tolist()}")
    
    # 分类评估
    print("\n【分类评估指标】")
    y_true = np.array([1, 1, 0, 0, 1, 1, 0, 0])
    y_pred = np.array([1, 0, 0, 0, 1, 1, 0, 1])
    
    print(f"准确率: {accuracy_score(y_true, y_pred):.4f}")
    print(f"精确率: {precision_score(y_true, y_pred):.4f}")
    print(f"召回率: {recall_score(y_true, y_pred):.4f}")
    print(f"F1分数: {f1_score(y_true, y_pred):.4f}")
    print(f"混淆矩阵:\n{confusion_matrix(y_true, y_pred)}")
    
    # 回归评估
    print("\n【回归评估指标】")
    y_true_reg = np.array([3.0, -0.5, 2.0, 7.0])
    y_pred_reg = np.array([2.5, 0.0, 2.0, 8.0])
    
    print(f"MSE: {mean_squared_error(y_true_reg, y_pred_reg):.4f}")
    print(f"MAE: {mean_absolute_error(y_true_reg, y_pred_reg):.4f}")
    print(f"R²: {r2_score(y_true_reg, y_pred_reg):.4f}")