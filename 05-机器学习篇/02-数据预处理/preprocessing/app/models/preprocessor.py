"""预处理器"""

import numpy as np


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