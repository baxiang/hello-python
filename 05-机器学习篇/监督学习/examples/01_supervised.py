# 监督学习示例

"""
监督学习示例
包含：线性回归、逻辑回归、决策树、KNN
"""

import numpy as np
from typing import Optional


# 1. 线性回归
class LinearRegression:
    """线性回归"""
    
    def __init__(self, learning_rate: float = 0.01, n_iterations: int = 1000):
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
        self.weights = None
        self.bias = None
    
    def fit(self, X: np.ndarray, y: np.ndarray) -> "LinearRegression":
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0
        
        for _ in range(self.n_iterations):
            y_pred = np.dot(X, self.weights) + self.bias
            dw = (1 / n_samples) * np.dot(X.T, (y_pred - y))
            db = (1 / n_samples) * np.sum(y_pred - y)
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db
        
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        return np.dot(X, self.weights) + self.bias


# 2. 逻辑回归
class LogisticRegression:
    """逻辑回归"""
    
    def __init__(self, learning_rate: float = 0.01, n_iterations: int = 1000):
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
        self.weights = None
        self.bias = None
    
    def _sigmoid(self, z: np.ndarray) -> np.ndarray:
        return 1 / (1 + np.exp(-np.clip(z, -500, 500)))
    
    def fit(self, X: np.ndarray, y: np.ndarray) -> "LogisticRegression":
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0
        
        for _ in range(self.n_iterations):
            linear_model = np.dot(X, self.weights) + self.bias
            y_pred = self._sigmoid(linear_model)
            dw = (1 / n_samples) * np.dot(X.T, (y_pred - y))
            db = (1 / n_samples) * np.sum(y_pred - y)
            self.weights -= self.learning_rate * dw
            self.bias -= self.learning_rate * db
        
        return self
    
    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        return self._sigmoid(np.dot(X, self.weights) + self.bias)
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        return (self.predict_proba(X) >= 0.5).astype(int)


# 3. K近邻
class KNNClassifier:
    """K近邻分类器"""
    
    def __init__(self, k: int = 3):
        self.k = k
        self.X_train = None
        self.y_train = None
    
    def fit(self, X: np.ndarray, y: np.ndarray) -> "KNNClassifier":
        self.X_train = X
        self.y_train = y
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        predictions = []
        for x in X:
            distances = np.sqrt(np.sum((self.X_train - x) ** 2, axis=1))
            k_indices = np.argsort(distances)[:self.k]
            k_labels = self.y_train[k_indices]
            most_common = np.bincount(k_labels).argmax()
            predictions.append(most_common)
        return np.array(predictions)


# 4. 决策树
class DecisionTreeClassifier:
    """简单决策树分类器"""
    
    def __init__(self, max_depth: int = 3):
        self.max_depth = max_depth
        self.tree = None
    
    def _gini(self, y: np.ndarray) -> float:
        classes, counts = np.unique(y, return_counts=True)
        probabilities = counts / len(y)
        return 1 - np.sum(probabilities ** 2)
    
    def _best_split(self, X: np.ndarray, y: np.ndarray):
        best_gini = 1
        best_feature = None
        best_threshold = None
        
        for feature in range(X.shape[1]):
            thresholds = np.unique(X[:, feature])
            for threshold in thresholds:
                left_mask = X[:, feature] <= threshold
                right_mask = ~left_mask
                
                if np.sum(left_mask) == 0 or np.sum(right_mask) == 0:
                    continue
                
                gini = (np.sum(left_mask) * self._gini(y[left_mask]) +
                        np.sum(right_mask) * self._gini(y[right_mask])) / len(y)
                
                if gini < best_gini:
                    best_gini = gini
                    best_feature = feature
                    best_threshold = threshold
        
        return best_feature, best_threshold
    
    def fit(self, X: np.ndarray, y: np.ndarray, depth: int = 0) -> dict:
        if depth >= self.max_depth or len(np.unique(y)) == 1:
            return {"leaf": True, "class": np.bincount(y).argmax()}
        
        feature, threshold = self._best_split(X, y)
        if feature is None:
            return {"leaf": True, "class": np.bincount(y).argmax()}
        
        left_mask = X[:, feature] <= threshold
        
        return {
            "leaf": False,
            "feature": feature,
            "threshold": threshold,
            "left": self.fit(X[left_mask], y[left_mask], depth + 1),
            "right": self.fit(X[~left_mask], y[~left_mask], depth + 1)
        }
    
    def _predict_one(self, x: np.ndarray, tree: dict) -> int:
        if tree["leaf"]:
            return tree["class"]
        
        if x[tree["feature"]] <= tree["threshold"]:
            return self._predict_one(x, tree["left"])
        else:
            return self._predict_one(x, tree["right"])
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        return np.array([self._predict_one(x, self.tree) for x in X])


if __name__ == "__main__":
    print("=" * 40)
    print("监督学习示例")
    print("=" * 40)
    
    # 线性回归
    print("\n【线性回归】")
    X_reg = np.array([[1], [2], [3], [4], [5]])
    y_reg = np.array([2, 4, 6, 8, 10])
    
    lr = LinearRegression()
    lr.fit(X_reg, y_reg)
    print(f"权重: {lr.weights}, 偏置: {lr.bias}")
    print(f"预测: {lr.predict(np.array([[6], [7]]))}")
    
    # 逻辑回归
    print("\n【逻辑回归】")
    X_cls = np.array([[1, 2], [2, 3], [3, 4], [4, 5]])
    y_cls = np.array([0, 0, 1, 1])
    
    log_reg = LogisticRegression()
    log_reg.fit(X_cls, y_cls)
    print(f"预测: {log_reg.predict(np.array([[2.5, 3.5], [3.5, 4.5]]))}")
    
    # KNN
    print("\n【K近邻】")
    knn = KNNClassifier(k=3)
    knn.fit(X_cls, y_cls)
    print(f"预测: {knn.predict(np.array([[2.5, 3.5]]))}")
    
    # 决策树
    print("\n【决策树】")
    X_tree = np.array([[1, 1], [1, 2], [2, 1], [2, 2], [3, 3], [4, 4]])
    y_tree = np.array([0, 0, 0, 1, 1, 1])
    
    dt = DecisionTreeClassifier(max_depth=2)
    dt.tree = dt.fit(X_tree, y_tree)
    print(f"预测: {dt.predict(np.array([[1.5, 1.5], [3.5, 3.5]]))}")