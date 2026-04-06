"""预处理器测试"""

import numpy as np
from app.models.preprocessor import StandardScaler, MinMaxScaler


def test_standard_scaler():
    X = np.array([[1, 10], [2, 20], [3, 30]])
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    assert np.allclose(X_scaled.mean(axis=0), 0, atol=1e-10)


def test_minmax_scaler():
    X = np.array([[1, 10], [2, 20], [3, 30]])
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    assert X_scaled.min() >= 0
    assert X_scaled.max() <= 1