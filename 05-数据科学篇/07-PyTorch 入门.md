# 第 36 章 - PyTorch 入门

> PyTorch 是当前最流行的深度学习框架之一，本章介绍 PyTorch 的核心概念和基本用法。

---

## 第一部分 - PyTorch 简介

### 1.1 什么是 PyTorch

PyTorch 是由 Facebook AI Research（FAIR）开发的开源深度学习框架。

**主要特点：**
- **动态计算图**：支持运行时构建计算图
- **Pythonic**：易于学习和使用
- **丰富的生态**：torchvision、torchtext 等
- **GPU 加速**：无缝支持 CUDA

### 1.2 安装 PyTorch

```bash
# CPU 版本
pip install torch

# GPU 版本（CUDA 11.8）
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

---

## 第二部分 - Tensor 基础

### 2.1 创建 Tensor

```python
import torch

# 从列表创建
x = torch.tensor([1, 2, 3])

# 创建零张量
zeros = torch.zeros(3, 4)

# 创建一张量
ones = torch.ones(2, 3)

# 随机张量
rand = torch.rand(3, 3)

# 从 numpy 转换
import numpy as np
np_array = np.array([1, 2, 3])
tensor = torch.from_numpy(np_array)
```

### 2.2 Tensor 操作

```python
# 形状操作
x = torch.rand(2, 3, 4)
print(x.shape)      # torch.Size([2, 3, 4])
print(x.view(6, 4)) # 改变形状

# 数学运算
a = torch.rand(3, 3)
b = torch.rand(3, 3)
c = a + b           # 加法
d = a * b           # 逐元素乘法
e = a @ b           # 矩阵乘法

# GPU 操作
if torch.cuda.is_available():
    x_gpu = x.cuda()
```

---

## 第三部分 - 自动求导

### 3.1 autograd 基础

```python
import torch

# 创建需要梯度的张量
x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)

# 计算
y = x ** 2 + 2 * x + 1

# 反向传播
y.sum().backward()

# 获取梯度
print(x.grad)  # tensor([4., 6., 8.])
```

---

## 第四部分 - nn.Module

### 4.1 定义神经网络

```python
import torch.nn as nn

class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.layers = nn.Sequential(
            nn.Linear(28*28, 128),
            nn.ReLU(),
            nn.Linear(128, 10)
        )
    
    def forward(self, x):
        x = self.flatten(x)
        return self.layers(x)

model = NeuralNetwork()
```

### 4.2 训练流程

```python
# 损失函数和优化器
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

# 训练循环
for epoch in range(10):
    for X, y in dataloader:
        # 前向传播
        pred = model(X)
        loss = criterion(pred, y)
        
        # 反向传播
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
```
---

[← 上一篇](./06-神经网络基础.md) | [下一篇 →](./08-卷积神经网络 CNN.md)
