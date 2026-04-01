# 模型优化示例

"""
模型优化示例
包含：网格搜索、交叉验证、正则化、学习曲线
"""

import numpy as np
from typing import Dict, List, Callable, Any


# 1. 网格搜索
class GridSearchCV:
    """网格搜索交叉验证"""
    
    def __init__(
        self,
        model_class: type,
        param_grid: Dict[str, List],
        cv: int = 5,
        scoring: str = "accuracy"
    ):
        self.model_class = model_class
        self.param_grid = param_grid
        self.cv = cv
        self.scoring = scoring
        self.best_params = None
        self.best_score = None
    
    def fit(self, X: np.ndarray, y: np.ndarray) -> "GridSearchCV":
        from itertools import product
        
        best_score = -np.inf
        best_params = None
        
        # 生成所有参数组合
        param_names = list(self.param_grid.keys())
        param_values = list(self.param_grid.values())
        
        for values in product(*param_values):
            params = dict(zip(param_names, values))
            
            # 交叉验证
            scores = self._cross_validate(X, y, params)
            mean_score = np.mean(scores)
            
            if mean_score > best_score:
                best_score = mean_score
                best_params = params
        
        self.best_params = best_params
        self.best_score = best_score
        
        return self
    
    def _cross_validate(self, X: np.ndarray, y: np.ndarray, params: dict) -> List[float]:
        n_samples = len(X)
        fold_size = n_samples // self.cv
        scores = []
        
        for i in range(self.cv):
            val_start = i * fold_size
            val_end = (i + 1) * fold_size if i < self.cv - 1 else n_samples
            
            val_indices = np.arange(val_start, val_end)
            train_indices = np.concatenate([
                np.arange(0, val_start),
                np.arange(val_end, n_samples)
            ])
            
            X_train, X_val = X[train_indices], X[val_indices]
            y_train, y_val = y[train_indices], y[val_indices]
            
            model = self.model_class(**params)
            model.fit(X_train, y_train)
            y_pred = model.predict(X_val)
            
            score = np.mean(y_pred == y_val)
            scores.append(score)
        
        return scores


# 2. 正则化线性回归
class RidgeRegression:
    """岭回归（L2 正则化）"""
    
    def __init__(self, alpha: float = 1.0):
        self.alpha = alpha
        self.weights = None
        self.bias = None
    
    def fit(self, X: np.ndarray, y: np.ndarray) -> "RidgeRegression":
        n_samples, n_features = X.shape
        
        # 添加偏置项
        X_b = np.c_[np.ones(n_samples), X]
        
        # 岭回归解析解
        I = np.eye(n_features + 1)
        I[0, 0] = 0  # 不正则化偏置项
        
        self.weights = np.linalg.inv(X_b.T @ X_b + self.alpha * I) @ X_b.T @ y
        self.bias = self.weights[0]
        self.weights = self.weights[1:]
        
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        return X @ self.weights + self.bias


class LassoRegression:
    """Lasso 回归（L1 正则化）"""
    
    def __init__(self, alpha: float = 1.0, max_iter: int = 1000):
        self.alpha = alpha
        self.max_iter = max_iter
        self.weights = None
        self.bias = None
    
    def fit(self, X: np.ndarray, y: np.ndarray) -> "LassoRegression":
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0
        
        for _ in range(self.max_iter):
            # 坐标下降
            for j in range(n_features):
                # 计算残差
                residual = y - X @ self.weights - self.bias + X[:, j] * self.weights[j]
                
                # 软阈值
                rho = X[:, j] @ residual
                if rho < -self.alpha:
                    self.weights[j] = (rho + self.alpha) / (X[:, j] @ X[:, j])
                elif rho > self.alpha:
                    self.weights[j] = (rho - self.alpha) / (X[:, j] @ X[:, j])
                else:
                    self.weights[j] = 0
            
            # 更新偏置
            self.bias = np.mean(y - X @ self.weights)
        
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        return X @ self.weights + self.bias


# 3. 学习曲线
def learning_curve(
    model,
    X: np.ndarray,
    y: np.ndarray,
    train_sizes: np.ndarray = None
) -> tuple:
    """计算学习曲线"""
    if train_sizes is None:
        train_sizes = np.linspace(0.1, 1.0, 10)
    
    train_scores = []
    val_scores = []
    
    n_samples = len(X)
    
    for size in train_sizes:
        n_train = int(n_samples * size)
        indices = np.random.permutation(n_samples)[:n_train]
        
        X_train, y_train = X[indices], y[indices]
        
        # 简单划分验证集
        n_val = int(n_train * 0.2)
        X_val, y_val = X_train[:n_val], y_train[:n_val]
        X_train, y_train = X_train[n_val:], y_train[n_val:]
        
        model.fit(X_train, y_train)
        
        train_score = np.mean(model.predict(X_train) == y_train)
        val_score = np.mean(model.predict(X_val) == y_val)
        
        train_scores.append(train_score)
        val_scores.append(val_score)
    
    return train_sizes, np.array(train_scores), np.array(val_scores)


# 4. 早停
class EarlyStopping:
    """早停机制"""
    
    def __init__(self, patience: int = 5, min_delta: float = 0.001):
        self.patience = patience
        self.min_delta = min_delta
        self.counter = 0
        self.best_score = None
        self.should_stop = False
    
    def __call__(self, score: float) -> bool:
        if self.best_score is None:
            self.best_score = score
        elif score < self.best_score + self.min_delta:
            self.counter += 1
            if self.counter >= self.patience:
                self.should_stop = True
        else:
            self.best_score = score
            self.counter = 0
        
        return self.should_stop


if __name__ == "__main__":
    print("=" * 40)
    print("模型优化示例")
    print("=" * 40)
    
    # 生成数据
    np.random.seed(42)
    X = np.random.randn(100, 5)
    y = (X[:, 0] + X[:, 1] > 0).astype(int)
    
    # 网格搜索
    print("\n【网格搜索】")
    from types import SimpleNamespace
    
    # 模拟一个简单的模型类
    class SimpleModel:
        def __init__(self, learning_rate=0.01, n_iterations=100):
            self.lr = learning_rate
            self.n_iter = n_iterations
            self.weights = None
        
        def fit(self, X, y):
            self.weights = np.random.randn(X.shape[1])
            return self
        
        def predict(self, X):
            return (X @ self.weights > 0).astype(int)
    
    grid = GridSearchCV(
        SimpleModel,
        {"learning_rate": [0.001, 0.01, 0.1], "n_iterations": [50, 100]},
        cv=3
    )
    grid.fit(X, y)
    print(f"最佳参数: {grid.best_params}")
    print(f"最佳分数: {grid.best_score:.4f}")
    
    # 正则化
    print("\n【正则化回归】")
    X_reg = np.random.randn(50, 3)
    y_reg = X_reg @ np.array([1, 2, 3]) + np.random.randn(50) * 0.1
    
    ridge = RidgeRegression(alpha=0.1)
    ridge.fit(X_reg, y_reg)
    print(f"岭回归权重: {ridge.weights}")
    
    lasso = LassoRegression(alpha=0.1)
    lasso.fit(X_reg, y_reg)
    print(f"Lasso权重: {lasso.weights}")
    
    # 早停
    print("\n【早停机制】")
    early_stop = EarlyStopping(patience=3)
    scores = [0.5, 0.6, 0.7, 0.75, 0.76, 0.75, 0.74, 0.73]
    
    for i, score in enumerate(scores):
        if early_stop(score):
            print(f"在第 {i+1} 轮停止，分数: {score:.2f}")
            break