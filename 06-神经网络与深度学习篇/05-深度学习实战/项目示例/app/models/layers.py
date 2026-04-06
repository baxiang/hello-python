"""神经网络层"""

import numpy as np
from typing import Callable


def sigmoid(x: np.ndarray) -> np.ndarray:
    """Sigmoid 激活函数"""
    return 1 / (1 + np.exp(-np.clip(x, -500, 500)))


def relu(x: np.ndarray) -> np.ndarray:
    """ReLU 激活函数"""
    return np.maximum(0, x)


def softmax(x: np.ndarray) -> np.ndarray:
    """Softmax 激活函数"""
    exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=1, keepdims=True)


class Dense:
    """全连接层"""
    
    def __init__(self, input_size: int, output_size: int):
        self.weights = np.random.randn(input_size, output_size) * 0.01
        self.bias = np.zeros(output_size)
        self.input = None
        self.grad_weights = None
        self.grad_bias = None
    
    def forward(self, x: np.ndarray) -> np.ndarray:
        self.input = x
        return x @ self.weights + self.bias
    
    def backward(self, grad: np.ndarray) -> np.ndarray:
        self.grad_weights = self.input.T @ grad
        self.grad_bias = np.sum(grad, axis=0)
        return grad @ self.weights.T
    
    def update(self, learning_rate: float) -> None:
        self.weights -= learning_rate * self.grad_weights
        self.bias -= learning_rate * self.grad_bias


class Activation:
    """激活函数层"""
    
    def __init__(self, activation: str = "relu"):
        self.activation_name = activation
        self.input = None
        
        if activation == "relu":
            self._forward = relu
            self._backward = lambda x: (x > 0).astype(float)
        elif activation == "sigmoid":
            self._forward = sigmoid
            self._backward = lambda x: sigmoid(x) * (1 - sigmoid(x))
    
    def forward(self, x: np.ndarray) -> np.ndarray:
        self.input = x
        return self._forward(x)
    
    def backward(self, grad: np.ndarray) -> np.ndarray:
        return grad * self._backward(self.input)


class NeuralNetwork:
    """前馈神经网络"""
    
    def __init__(self, layers: list):
        self.layers = layers
        self.history = {"loss": [], "accuracy": []}
    
    def forward(self, x: np.ndarray) -> np.ndarray:
        for layer in self.layers:
            x = layer.forward(x)
        return x
    
    def backward(self, grad: np.ndarray) -> None:
        for layer in reversed(self.layers):
            grad = layer.backward(grad)
    
    def update(self, learning_rate: float) -> None:
        for layer in self.layers:
            if hasattr(layer, "update"):
                layer.update(learning_rate)
    
    def fit(self, X: np.ndarray, y: np.ndarray, epochs: int = 100, learning_rate: float = 0.01) -> "NeuralNetwork":
        for epoch in range(epochs):
            y_pred = self.forward(X)
            loss = np.mean((y_pred - y) ** 2)
            grad = 2 * (y_pred - y) / y.size
            
            self.backward(grad)
            self.update(learning_rate)
            
            self.history["loss"].append(loss)
            accuracy = np.mean((y_pred.flatten() > 0.5) == y.flatten())
            self.history["accuracy"].append(accuracy)
        
        return self
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.forward(X)