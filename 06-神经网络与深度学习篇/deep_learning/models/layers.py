# 神经网络层

"""
神经网络层实现
包含：全连接层、激活函数、损失函数
"""

import numpy as np
from typing import Optional, Callable


# 激活函数
def sigmoid(x: np.ndarray) -> np.ndarray:
    """Sigmoid 激活函数"""
    return 1 / (1 + np.exp(-np.clip(x, -500, 500)))


def sigmoid_derivative(x: np.ndarray) -> np.ndarray:
    """Sigmoid 导数"""
    s = sigmoid(x)
    return s * (1 - s)


def relu(x: np.ndarray) -> np.ndarray:
    """ReLU 激活函数"""
    return np.maximum(0, x)


def relu_derivative(x: np.ndarray) -> np.ndarray:
    """ReLU 导数"""
    return (x > 0).astype(float)


def softmax(x: np.ndarray) -> np.ndarray:
    """Softmax 激活函数"""
    exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
    return exp_x / np.sum(exp_x, axis=1, keepdims=True)


def tanh(x: np.ndarray) -> np.ndarray:
    """Tanh 激活函数"""
    return np.tanh(x)


def tanh_derivative(x: np.ndarray) -> np.ndarray:
    """Tanh 导数"""
    return 1 - np.tanh(x) ** 2


# 损失函数
def mse_loss(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """均方误差损失"""
    return np.mean((y_true - y_pred) ** 2)


def mse_loss_derivative(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    """MSE 损失导数"""
    return 2 * (y_pred - y_true) / y_true.size


def cross_entropy_loss(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """交叉熵损失"""
    epsilon = 1e-15
    y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
    return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))


def cross_entropy_derivative(y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    """交叉熵导数"""
    epsilon = 1e-15
    y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
    return -(y_true / y_pred) + (1 - y_true) / (1 - y_pred)


# 层定义
class Layer:
    """神经网络层基类"""
    
    def forward(self, x: np.ndarray) -> np.ndarray:
        raise NotImplementedError
    
    def backward(self, grad: np.ndarray) -> np.ndarray:
        raise NotImplementedError


class Dense(Layer):
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


class Activation(Layer):
    """激活函数层"""
    
    def __init__(self, activation: str = "relu"):
        self.activation_name = activation
        self.input = None
        
        if activation == "relu":
            self._forward = relu
            self._backward = relu_derivative
        elif activation == "sigmoid":
            self._forward = sigmoid
            self._backward = sigmoid_derivative
        elif activation == "tanh":
            self._forward = tanh
            self._backward = tanh_derivative
        else:
            raise ValueError(f"未知激活函数: {activation}")
    
    def forward(self, x: np.ndarray) -> np.ndarray:
        self.input = x
        return self._forward(x)
    
    def backward(self, grad: np.ndarray) -> np.ndarray:
        return grad * self._backward(self.input)


class Dropout(Layer):
    """Dropout 层"""
    
    def __init__(self, rate: float = 0.5):
        self.rate = rate
        self.mask = None
    
    def forward(self, x: np.ndarray, training: bool = True) -> np.ndarray:
        if training:
            self.mask = (np.random.rand(*x.shape) > self.rate) / (1 - self.rate)
            return x * self.mask
        return x
    
    def backward(self, grad: np.ndarray) -> np.ndarray:
        return grad * self.mask


class BatchNormalization(Layer):
    """批归一化层"""
    
    def __init__(self, size: int, momentum: float = 0.9, epsilon: float = 1e-5):
        self.gamma = np.ones(size)
        self.beta = np.zeros(size)
        self.momentum = momentum
        self.epsilon = epsilon
        
        self.running_mean = np.zeros(size)
        self.running_var = np.ones(size)
        
        self.input = None
        self.mean = None
        self.var = None
    
    def forward(self, x: np.ndarray, training: bool = True) -> np.ndarray:
        if training:
            self.mean = np.mean(x, axis=0)
            self.var = np.var(x, axis=0)
            
            self.running_mean = self.momentum * self.running_mean + (1 - self.momentum) * self.mean
            self.running_var = self.momentum * self.running_var + (1 - self.momentum) * self.var
            
            x_norm = (x - self.mean) / np.sqrt(self.var + self.epsilon)
        else:
            x_norm = (x - self.running_mean) / np.sqrt(self.running_var + self.epsilon)
        
        self.input = x_norm
        return self.gamma * x_norm + self.beta
    
    def backward(self, grad: np.ndarray) -> np.ndarray:
        # 简化的反向传播
        return grad * self.gamma