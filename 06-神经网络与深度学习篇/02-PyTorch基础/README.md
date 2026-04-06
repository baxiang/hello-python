# PyTorch 基础

掌握深度学习框架 PyTorch 的核心使用方法。

---

## 学习目标

学完本节，你将掌握：
- ✅ Tensor 的创建和操作
- ✅ 自动求导机制
- ✅ 构建神经网络模型
- ✅ 训练和测试流程

---

## 章节内容

| 文件 | 主题 | 预计时间 |
|------|------|---------|
| [02-PyTorch 入门.md](./02-PyTorch 入门.md) | Tensor、计算图、模型构建 | 3-5天 |

---

## 前置知识

**必备：**
- 神经网络基础概念（上一节）
- Python 编程
- NumPy 使用经验

---

## PyTorch 核心概念

### 1. Tensor（张量）

```python
import torch

# 创建张量
x = torch.tensor([1, 2, 3])

# 张量运算
y = x * 2
z = x + y
```

### 2. 自动求导

```python
x = torch.tensor([2.0], requires_grad=True)
y = x ** 2
y.backward()  # 自动计算梯度
print(x.grad)  # dy/dx = 2x = 4
```

### 3. 神经网络模块

```python
import torch.nn as nn

model = nn.Sequential(
    nn.Linear(10, 20),
    nn.ReLU(),
    nn.Linear(20, 1)
)
```

---

## 快速上手

### 安装 PyTorch

```bash
# 使用 uv 安装
uv add torch torchvision

# 或使用 pip
pip install torch torchvision
```

### 第一个神经网络

```python
import torch
import torch.nn as nn

# 1. 定义模型
model = nn.Sequential(
    nn.Linear(2, 10),
    nn.ReLU(),
    nn.Linear(10, 1)
)

# 2. 定义损失函数和优化器
criterion = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

# 3. 训练
for epoch in range(100):
    # 前向传播
    outputs = model(inputs)
    loss = criterion(outputs, targets)
    
    # 反向传播
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
```

---

## 学习建议

1. **动手实践** - 每个概念都要写代码验证
2. **对比 NumPy** - 理解 Tensor 与 NumPy 的区别
3. **调试技巧** - 学会打印张量形状和梯度
4. **官方文档** - PyTorch 文档非常详细，多查阅

---

## 常见问题

### Q: PyTorch 和 TensorFlow 选哪个？
**A:** 初学者推荐 PyTorch，更符合 Python 编程习惯。

### Q: 需要学习 CUDA 吗？
**A:** 学习阶段不需要，使用 CPU 即可。后面做项目再学 GPU 加速。

### Q: 如何调试神经网络？
**A:** 
- 打印每层的输出形状
- 检查梯度是否正常
- 监控损失变化曲线

---

## 学习检查

完成后，你应该能：
- [ ] 创建和操作 Tensor
- [ ] 理解计算图和自动求导
- [ ] 构建简单的神经网络
- [ ] 完成训练循环

---

## 下一步

学完后，继续学习：
→ [卷积神经网络](../卷积神经网络/) - 处理图像数据