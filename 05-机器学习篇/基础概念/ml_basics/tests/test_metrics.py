"""指标测试"""

import numpy as np
from app.models.metrics import accuracy_score, mean_squared_error, train_test_split


def test_accuracy_score():
    y_true = np.array([1, 1, 0, 0])
    y_pred = np.array([1, 0, 0, 0])
    assert accuracy_score(y_true, y_pred) == 0.75


def test_mean_squared_error():
    y_true = np.array([3.0, 2.0, 1.0])
    y_pred = np.array([2.5, 2.0, 1.5])
    assert mean_squared_error(y_true, y_pred) > 0


def test_train_test_split():
    X = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])
    y = np.array([0, 0, 1, 1])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)
    assert len(X_train) == 2
    assert len(X_test) == 2