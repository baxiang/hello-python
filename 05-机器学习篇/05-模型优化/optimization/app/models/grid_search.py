"""优化算法"""

import numpy as np
from typing import Dict, List, Any


class GridSearchCV:
    """网格搜索交叉验证"""
    
    def __init__(self, model_class: type, param_grid: Dict[str, List], cv: int = 5):
        self.model_class = model_class
        self.param_grid = param_grid
        self.cv = cv
        self.best_params = None
        self.best_score = None
    
    def fit(self, X: np.ndarray, y: np.ndarray) -> "GridSearchCV":
        from itertools import product
        
        best_score = -np.inf
        best_params = None
        
        param_names = list(self.param_grid.keys())
        param_values = list(self.param_grid.values())
        
        for values in product(*param_values):
            params = dict(zip(param_names, values))
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
            train_indices = np.concatenate([np.arange(0, val_start), np.arange(val_end, n_samples)])
            
            X_train, X_val = X[train_indices], X[val_indices]
            y_train, y_val = y[train_indices], y[val_indices]
            
            model = self.model_class(**params)
            model.fit(X_train, y_train)
            y_pred = model.predict(X_val)
            scores.append(np.mean(y_pred == y_val))
        
        return scores


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