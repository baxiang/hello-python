"""数据处理"""

import numpy as np


def handle_missing(X: np.ndarray, strategy: str = "mean") -> np.ndarray:
    """处理缺失值"""
    if strategy == "mean":
        fill_value = np.nanmean(X, axis=0)
    elif strategy == "median":
        fill_value = np.nanmedian(X, axis=0)
    else:
        fill_value = 0
    
    X_filled = X.copy()
    for i in range(X.shape[1]):
        mask = np.isnan(X[:, i])
        X_filled[mask, i] = fill_value[i]
    return X_filled