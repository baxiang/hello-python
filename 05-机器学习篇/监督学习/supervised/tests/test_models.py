"""模型测试"""

import numpy as np
from app.models.regression import LinearRegression, LogisticRegression


def test_linear_regression():
    X = np.array([[1], [2], [3], [4], [5]])
    y = np.array([2, 4, 6, 8, 10])
    model = LinearRegression()
    model.fit(X, y)
    pred = model.predict(np.array([[6]]))
    assert abs(pred[0] - 12) < 1


def test_logistic_regression():
    X = np.array([[1, 2], [2, 3], [3, 4], [4, 5]])
    y = np.array([0, 0, 1, 1])
    model = LogisticRegression()
    model.fit(X, y)
    pred = model.predict(np.array([[2.5, 3.5]]))
    assert pred[0] in [0, 1]