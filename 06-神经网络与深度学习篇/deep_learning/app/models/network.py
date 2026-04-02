"""
神经网络模型模块

提供神经网络模型的构建和训练功能。
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Literal, Optional, Tuple, Union

import numpy as np

from app.models.layers import Layer, get_activation


class NeuralNetwork:
    """
    神经网络基类

    定义神经网络的基本接口。

    Attributes:
        layers: 网络层列表
    """

    def __init__(self) -> None:
        """初始化神经网络"""
        self.layers: List[Layer] = []

    def add(self, layer: Layer) -> None:
        """
        添加网络层

        Args:
            layer: 要添加的网络层
        """
        self.layers.append(layer)

    def forward(self, x: np.ndarray) -> np.ndarray:
        """
        前向传播

        Args:
            x: 输入数据

        Returns:
            输出数据
        """
        for layer in self.layers:
            x = layer.forward(x)
        return x

    def backward(self, grad_output: np.ndarray) -> np.ndarray:
        """
        反向传播

        Args:
            grad_output: 来自损失函数的梯度

        Returns:
            输入梯度
        """
        grad = grad_output
        for layer in reversed(self.layers):
            grad = layer.backward(grad)
        return grad

    def train(self) -> None:
        """将所有层设置为训练模式"""
        for layer in self.layers:
            layer.train()

    def eval(self) -> None:
        """将所有层设置为评估模式"""
        for layer in self.layers:
            layer.eval()

    def parameters(self) -> Dict[str, np.ndarray]:
        """
        获取所有可训练参数

        Returns:
            参数字典
        """
        params = {}
        for i, layer in enumerate(self.layers):
            for name, param in layer.params.items():
                params[f"layer_{i}_{name}"] = param
        return params

    def gradients(self) -> Dict[str, np.ndarray]:
        """
        获取所有参数梯度

        Returns:
            梯度字典
        """
        grads = {}
        for i, layer in enumerate(self.layers):
            for name, grad in layer.grads.items():
                grads[f"layer_{i}_{name}"] = grad
        return grads


class Sequential(NeuralNetwork):
    """
    序列模型

    按顺序堆叠多个网络层。

    Example:
        >>> model = Sequential([
        ...     Dense(784, 128),
        ...     ReLU(),
        ...     Dense(128, 10),
        ...     Softmax(),
        ... ])
        >>> output = model.forward(x)
    """

    def __init__(self, layers: Optional[List[Layer]] = None) -> None:
        """
        初始化序列模型

        Args:
            layers: 网络层列表
        """
        super().__init__()
        if layers is not None:
            self.layers = layers

    def __len__(self) -> int:
        """返回层数"""
        return len(self.layers)

    def __getitem__(self, idx: int) -> Layer:
        """获取指定索引的层"""
        return self.layers[idx]

    def summary(self) -> str:
        """
        生成模型摘要

        Returns:
            模型摘要字符串
        """
        lines = ["=" * 50, "Model Summary", "=" * 50]

        total_params = 0
        for i, layer in enumerate(self.layers):
            layer_str = str(layer)
            params = sum(p.size for p in layer.params.values())
            total_params += params
            lines.append(f"Layer {i}: {layer_str} ({params:,} params)")

        lines.extend([
            "-" * 50,
            f"Total Parameters: {total_params:,}",
            "=" * 50,
        ])

        return "\n".join(lines)


class Trainer:
    """
    模型训练器

    提供模型训练、评估等功能。

    Attributes:
        model: 神经网络模型
        learning_rate: 学习率
        loss_fn: 损失函数名称
        optimizer: 优化器名称

    Example:
        >>> trainer = Trainer(model, learning_rate=0.01)
        >>> history = trainer.train(x_train, y_train, epochs=10)
    """

    def __init__(
        self,
        model: NeuralNetwork,
        learning_rate: float = 0.001,
        loss_fn: Literal["mse", "cross_entropy"] = "cross_entropy",
        optimizer: Literal["sgd", "momentum"] = "sgd",
        momentum: float = 0.9,
    ) -> None:
        """
        初始化训练器

        Args:
            model: 神经网络模型
            learning_rate: 学习率
            loss_fn: 损失函数，支持 "mse" 和 "cross_entropy"
            optimizer: 优化器，支持 "sgd" 和 "momentum"
            momentum: 动量系数，仅当 optimizer="momentum" 时使用
        """
        self.model = model
        self.learning_rate = learning_rate
        self.loss_fn = loss_fn
        self.optimizer = optimizer
        self.momentum = momentum

        # 动量优化器的速度缓存
        self._velocity: Dict[str, np.ndarray] = {}

        # 损失函数映射
        self._loss_functions: Dict[str, Callable] = {
            "mse": mean_squared_error,
            "cross_entropy": cross_entropy_loss,
        }
        self._loss_gradients: Dict[str, Callable] = {
            "mse": mean_squared_error_gradient,
            "cross_entropy": cross_entropy_gradient,
        }

    def train_step(
        self,
        x: np.ndarray,
        y: np.ndarray,
    ) -> float:
        """
        执行单步训练

        Args:
            x: 输入数据
            y: 目标数据

        Returns:
            当前批次的损失值
        """
        # 前向传播
        predictions = self.model.forward(x)

        # 计算损失
        loss_fn = self._loss_functions[self.loss_fn]
        loss = loss_fn(predictions, y)

        # 计算梯度
        loss_grad_fn = self._loss_gradients[self.loss_fn]
        grad = loss_grad_fn(predictions, y)

        # 反向传播
        self.model.backward(grad)

        # 更新参数
        self._update_parameters()

        return loss

    def _update_parameters(self) -> None:
        """更新模型参数"""
        for i, layer in enumerate(self.model.layers):
            for name, param in layer.params.items():
                grad = layer.grads[name]
                key = f"layer_{i}_{name}"

                if self.optimizer == "momentum":
                    # 动量更新
                    if key not in self._velocity:
                        self._velocity[key] = np.zeros_like(grad)
                    self._velocity[key] = (
                        self.momentum * self._velocity[key] - self.learning_rate * grad
                    )
                    layer.params[name] = param + self._velocity[key]
                else:
                    # SGD 更新
                    layer.params[name] = param - self.learning_rate * grad

    def train(
        self,
        x: np.ndarray,
        y: np.ndarray,
        epochs: int = 10,
        batch_size: int = 32,
        validation_data: Optional[Tuple[np.ndarray, np.ndarray]] = None,
        verbose: bool = True,
    ) -> Dict[str, List[float]]:
        """
        训练模型

        Args:
            x: 训练数据
            y: 训练标签
            epochs: 训练轮数
            batch_size: 批次大小
            validation_data: 验证数据元组 (x_val, y_val)
            verbose: 是否打印训练进度

        Returns:
            训练历史字典，包含 loss 和 val_loss
        """
        history: Dict[str, List[float]] = {"loss": []}
        if validation_data is not None:
            history["val_loss"] = []

        n_samples = x.shape[0]
        n_batches = (n_samples + batch_size - 1) // batch_size

        self.model.train()

        for epoch in range(epochs):
            # 打乱数据
            indices = np.random.permutation(n_samples)
            x_shuffled = x[indices]
            y_shuffled = y[indices]

            epoch_loss = 0.0

            for batch_idx in range(n_batches):
                start = batch_idx * batch_size
                end = min(start + batch_size, n_samples)

                x_batch = x_shuffled[start:end]
                y_batch = y_shuffled[start:end]

                batch_loss = self.train_step(x_batch, y_batch)
                epoch_loss += batch_loss

            epoch_loss /= n_batches
            history["loss"].append(epoch_loss)

            # 验证
            if validation_data is not None:
                val_loss = self.evaluate(validation_data[0], validation_data[1])["loss"]
                history["val_loss"].append(val_loss)

            if verbose:
                msg = f"Epoch {epoch + 1}/{epochs} - Loss: {epoch_loss:.4f}"
                if validation_data is not None:
                    msg += f" - Val Loss: {val_loss:.4f}"
                print(msg)

        return history

    def evaluate(
        self,
        x: np.ndarray,
        y: np.ndarray,
    ) -> Dict[str, float]:
        """
        评估模型

        Args:
            x: 测试数据
            y: 测试标签

        Returns:
            评估指标字典
        """
        self.model.eval()

        # 前向传播
        predictions = self.model.forward(x)

        # 计算损失
        loss_fn = self._loss_functions[self.loss_fn]
        loss = loss_fn(predictions, y)

        metrics = {"loss": loss}

        # 计算准确率（分类任务）
        if self.loss_fn == "cross_entropy":
            predicted_classes = np.argmax(predictions, axis=1)
            if y.ndim > 1:
                true_classes = np.argmax(y, axis=1)
            else:
                true_classes = y
            accuracy = np.mean(predicted_classes == true_classes)
            metrics["accuracy"] = accuracy

        return metrics

    def predict(self, x: np.ndarray) -> np.ndarray:
        """
        预测

        Args:
            x: 输入数据

        Returns:
            预测结果
        """
        self.model.eval()
        return self.model.forward(x)


# ==================== 损失函数 ====================


def mean_squared_error(predictions: np.ndarray, targets: np.ndarray) -> float:
    """
    均方误差损失

    Args:
        predictions: 预测值
        targets: 目标值

    Returns:
        损失值

    Example:
        >>> predictions = np.array([[1, 2], [3, 4]])
        >>> targets = np.array([[1, 2], [3, 4]])
        >>> mean_squared_error(predictions, targets)
        0.0
    """
    return float(np.mean((predictions - targets) ** 2))


def mean_squared_error_gradient(
    predictions: np.ndarray, targets: np.ndarray
) -> np.ndarray:
    """
    均方误差梯度

    Args:
        predictions: 预测值
        targets: 目标值

    Returns:
        损失对预测值的梯度
    """
    batch_size = predictions.shape[0]
    return 2 * (predictions - targets) / batch_size


def cross_entropy_loss(
    predictions: np.ndarray,
    targets: np.ndarray,
    epsilon: float = 1e-15,
) -> float:
    """
    交叉熵损失

    Args:
        predictions: 预测概率，形状为 (batch_size, num_classes)
        targets: 目标标签，可以是 one-hot 编码或类别索引
        epsilon: 数值稳定性常数

    Returns:
        损失值

    Example:
        >>> predictions = np.array([[0.9, 0.05, 0.05], [0.1, 0.8, 0.1]])
        >>> targets = np.array([0, 1])
        >>> cross_entropy_loss(predictions, targets)
        0.164...
    """
    # 裁剪预测值以避免 log(0)
    predictions = np.clip(predictions, epsilon, 1 - epsilon)

    # 处理不同格式的 targets
    if targets.ndim == 1:
        # targets 是类别索引
        batch_size = predictions.shape[0]
        loss = -np.mean(np.log(predictions[np.arange(batch_size), targets]))
    else:
        # targets 是 one-hot 编码
        loss = -np.mean(np.sum(targets * np.log(predictions), axis=1))

    return float(loss)


def cross_entropy_gradient(
    predictions: np.ndarray,
    targets: np.ndarray,
    epsilon: float = 1e-15,
) -> np.ndarray:
    """
    交叉熵损失梯度

    结合 softmax 和交叉熵的梯度，简化计算。

    Args:
        predictions: 预测概率
        targets: 目标标签
        epsilon: 数值稳定性常数

    Returns:
        损失对预测值的梯度
    """
    batch_size = predictions.shape[0]

    # 裁剪预测值
    predictions = np.clip(predictions, epsilon, 1 - epsilon)

    # 处理不同格式的 targets
    if targets.ndim == 1:
        # targets 是类别索引，转换为 one-hot
        num_classes = predictions.shape[1]
        targets_onehot = np.zeros((batch_size, num_classes))
        targets_onehot[np.arange(batch_size), targets] = 1
        targets = targets_onehot

    # Softmax + Cross Entropy 的简化梯度
    return (predictions - targets) / batch_size