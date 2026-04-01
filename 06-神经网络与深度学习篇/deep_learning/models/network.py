# 神经网络模型

"""
神经网络模型实现
包含：前馈神经网络、训练器
"""

import numpy as np
from typing import List, Callable, Optional
from .layers import Layer, Dense, Activation, Dropout, softmax
from .layers import mse_loss, mse_loss_derivative, cross_entropy_loss


class NeuralNetwork:
    """前馈神经网络"""
    
    def __init__(self, layers: List[Layer]):
        self.layers = layers
        self.history = {"loss": [], "accuracy": []}
    
    def forward(self, x: np.ndarray, training: bool = True) -> np.ndarray:
        """前向传播"""
        for layer in self.layers:
            if isinstance(layer, Dropout):
                x = layer.forward(x, training)
            else:
                x = layer.forward(x)
        return x
    
    def backward(self, grad: np.ndarray) -> None:
        """反向传播"""
        for layer in reversed(self.layers):
            grad = layer.backward(grad)
    
    def update(self, learning_rate: float) -> None:
        """更新参数"""
        for layer in self.layers:
            if hasattr(layer, "update"):
                layer.update(learning_rate)
    
    def fit(
        self,
        X: np.ndarray,
        y: np.ndarray,
        epochs: int = 100,
        batch_size: int = 32,
        learning_rate: float = 0.01,
        loss_fn: str = "mse",
        verbose: int = 1
    ) -> "NeuralNetwork":
        """训练模型"""
        n_samples = len(X)
        
        for epoch in range(epochs):
            # 打乱数据
            indices = np.random.permutation(n_samples)
            X_shuffled = X[indices]
            y_shuffled = y[indices]
            
            epoch_loss = 0
            n_batches = 0
            
            # 批量训练
            for i in range(0, n_samples, batch_size):
                X_batch = X_shuffled[i:i + batch_size]
                y_batch = y_shuffled[i:i + batch_size]
                
                # 前向传播
                y_pred = self.forward(X_batch, training=True)
                
                # 计算损失
                if loss_fn == "mse":
                    loss = mse_loss(y_batch, y_pred)
                    grad = mse_loss_derivative(y_batch, y_pred)
                else:
                    loss = cross_entropy_loss(y_batch, y_pred)
                    grad = y_pred - y_batch
                
                epoch_loss += loss
                n_batches += 1
                
                # 反向传播
                self.backward(grad)
                
                # 更新参数
                self.update(learning_rate)
            
            # 记录历史
            avg_loss = epoch_loss / n_batches
            self.history["loss"].append(avg_loss)
            
            # 计算准确率
            y_pred_all = self.forward(X, training=False)
            if y.ndim == 1:
                accuracy = np.mean((y_pred_all.flatten() > 0.5) == y)
            else:
                accuracy = np.mean(np.argmax(y_pred_all, axis=1) == np.argmax(y, axis=1))
            self.history["accuracy"].append(accuracy)
            
            if verbose and (epoch + 1) % 10 == 0:
                print(f"Epoch {epoch + 1}/{epochs} - Loss: {avg_loss:.4f} - Accuracy: {accuracy:.4f}")
        
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """预测"""
        return self.forward(X, training=False)
    
    def predict_classes(self, X: np.ndarray) -> np.ndarray:
        """预测类别"""
        y_pred = self.predict(X)
        if y_pred.shape[1] == 1:
            return (y_pred > 0.5).astype(int).flatten()
        return np.argmax(y_pred, axis=1)


class Sequential(NeuralNetwork):
    """序列模型"""
    
    def __init__(self):
        self._layers = []
        super().__init__([])
    
    def add(self, layer: Layer) -> "Sequential":
        """添加层"""
        self._layers.append(layer)
        self.layers = self._layers
        return self
    
    def compile(
        self,
        optimizer: str = "sgd",
        loss: str = "mse",
        metrics: List[str] = None
    ) -> "Sequential":
        """编译模型"""
        self.optimizer = optimizer
        self.loss = loss
        self.metrics = metrics or ["accuracy"]
        return self


# 工具函数
def create_mlp(
    input_size: int,
    hidden_sizes: List[int],
    output_size: int,
    activation: str = "relu",
    dropout_rate: float = 0.0
) -> NeuralNetwork:
    """创建多层感知机"""
    layers = []
    
    # 输入层到第一个隐藏层
    prev_size = input_size
    
    for hidden_size in hidden_sizes:
        layers.append(Dense(prev_size, hidden_size))
        layers.append(Activation(activation))
        if dropout_rate > 0:
            layers.append(Dropout(dropout_rate))
        prev_size = hidden_size
    
    # 输出层
    layers.append(Dense(prev_size, output_size))
    
    return NeuralNetwork(layers)