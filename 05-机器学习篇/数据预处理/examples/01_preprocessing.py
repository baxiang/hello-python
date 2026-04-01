# 数据预处理示例

"""
数据预处理示例
包含：缺失值处理、标准化、编码、特征选择
"""

import numpy as np
from typing import Optional


# 1. 缺失值处理
class SimpleImputer:
    """简单缺失值填充"""
    
    def __init__(self, strategy: str = "mean"):
        self.strategy = strategy
        self.fill_values = None
    
    def fit(self, X: np.ndarray) -> "SimpleImputer":
        """计算填充值"""
        if self.strategy == "mean":
            self.fill_values = np.nanmean(X, axis=0)
        elif self.strategy == "median":
            self.fill_values = np.nanmedian(X, axis=0)
        elif self.strategy == "most_frequent":
            self.fill_values = np.array([
                np.bincount(X[~np.isnan(X[:, i]), i].astype(int)).argmax()
                for i in range(X.shape[1])
            ])
        return self
    
    def transform(self, X: np.ndarray) -> np.ndarray:
        """填充缺失值"""
        X_filled = X.copy()
        for i in range(X.shape[1]):
            mask = np.isnan(X[:, i])
            X_filled[mask, i] = self.fill_values[i]
        return X_filled
    
    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        return self.fit(X).transform(X)


# 2. 标准化
class StandardScaler:
    """Z-score 标准化"""
    
    def __init__(self):
        self.mean_ = None
        self.scale_ = None
    
    def fit(self, X: np.ndarray) -> "StandardScaler":
        self.mean_ = np.mean(X, axis=0)
        self.scale_ = np.std(X, axis=0)
        return self
    
    def transform(self, X: np.ndarray) -> np.ndarray:
        return (X - self.mean_) / self.scale_
    
    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        return self.fit(X).transform(X)
    
    def inverse_transform(self, X: np.ndarray) -> np.ndarray:
        return X * self.scale_ + self.mean_


class MinMaxScaler:
    """Min-Max 归一化"""
    
    def __init__(self, feature_range: tuple = (0, 1)):
        self.feature_range = feature_range
        self.min_ = None
        self.scale_ = None
    
    def fit(self, X: np.ndarray) -> "MinMaxScaler":
        self.min_ = np.min(X, axis=0)
        self.scale_ = np.max(X, axis=0) - self.min_
        return self
    
    def transform(self, X: np.ndarray) -> np.ndarray:
        X_scaled = (X - self.min_) / self.scale_
        return X_scaled * (self.feature_range[1] - self.feature_range[0]) + self.feature_range[0]
    
    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        return self.fit(X).transform(X)


# 3. 编码
class LabelEncoder:
    """标签编码"""
    
    def __init__(self):
        self.classes_ = None
    
    def fit(self, y: np.ndarray) -> "LabelEncoder":
        self.classes_ = np.unique(y)
        return self
    
    def transform(self, y: np.ndarray) -> np.ndarray:
        return np.array([np.where(self.classes_ == label)[0][0] for label in y])
    
    def fit_transform(self, y: np.ndarray) -> np.ndarray:
        return self.fit(y).transform(y)
    
    def inverse_transform(self, y: np.ndarray) -> np.ndarray:
        return self.classes_[y]


class OneHotEncoder:
    """独热编码"""
    
    def __init__(self):
        self.categories_ = None
    
    def fit(self, X: np.ndarray) -> "OneHotEncoder":
        self.categories_ = [np.unique(X[:, i]) for i in range(X.shape[1])]
        return self
    
    def transform(self, X: np.ndarray) -> np.ndarray:
        encoded = []
        for i in range(X.shape[1]):
            for cat in self.categories_[i]:
                encoded.append((X[:, i] == cat).astype(int))
        return np.column_stack(encoded)
    
    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        return self.fit(X).transform(X)


# 4. 特征选择
def variance_threshold(X: np.ndarray, threshold: float = 0.0) -> np.ndarray:
    """方差阈值特征选择"""
    variances = np.var(X, axis=0)
    return X[:, variances > threshold]


def correlation_filter(X: np.ndarray, y: np.ndarray, threshold: float = 0.1) -> np.ndarray:
    """相关性过滤"""
    correlations = np.array([np.corrcoef(X[:, i], y)[0, 1] for i in range(X.shape[1])])
    return X[:, np.abs(correlations) > threshold]


if __name__ == "__main__":
    print("=" * 40)
    print("数据预处理示例")
    print("=" * 40)
    
    # 缺失值处理
    print("\n【缺失值处理】")
    X_missing = np.array([[1, 2, np.nan], [3, np.nan, 6], [np.nan, 8, 9]])
    print(f"原始数据:\n{X_missing}")
    
    imputer = SimpleImputer(strategy="mean")
    X_filled = imputer.fit_transform(X_missing)
    print(f"填充后:\n{X_filled}")
    
    # 标准化
    print("\n【标准化】")
    X = np.array([[1, 10], [2, 20], [3, 30], [4, 40]])
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    print(f"Z-score 标准化:\n{X_scaled}")
    
    minmax = MinMaxScaler()
    X_norm = minmax.fit_transform(X)
    print(f"Min-Max 归一化:\n{X_norm}")
    
    # 编码
    print("\n【编码】")
    labels = np.array(["cat", "dog", "cat", "bird", "dog"])
    
    le = LabelEncoder()
    encoded = le.fit_transform(labels)
    print(f"标签编码: {labels} -> {encoded}")
    print(f"解码: {le.inverse_transform(encoded)}")
    
    categories = np.array([["A"], ["B"], ["A"], ["C"]])
    ohe = OneHotEncoder()
    onehot = ohe.fit_transform(categories)
    print(f"独热编码:\n{onehot}")
    
    # 特征选择
    print("\n【特征选择】")
    X_features = np.array([[1, 1, 1], [2, 1, 2], [3, 1, 3], [4, 1, 4]])
    print(f"原始特征:\n{X_features}")
    print(f"方差阈值过滤后:\n{variance_threshold(X_features, threshold=0.1)}")