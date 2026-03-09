# 第 36 章 - PyTorch 入门（详细版）

本章介绍 PyTorch 深度学习框架的基础，包括 Tensor 操作、自动求导、神经网络搭建和训练流程。

---

## 第一部分：PyTorch 简介

### 36.1 为什么选择 PyTorch

#### 概念说明

PyTorch 是由 Facebook（现 Meta）开发的开源深度学习框架，已成为研究和工业界的主流选择。

**PyTorch 核心优势：**

```
┌─────────────────────────────────────────────────────────────┐
│              PyTorch 核心优势                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   1. 动态计算图 (Dynamic Computation Graph)                 │
│   ┌───────────────────────────────────────────────────┐     │
│   │  • 计算图在运行时动态构建                           │     │
│   │  • 更 Pythonic、调试友好                           │     │
│   │  • 适合变长输入（如 NLP 任务）                       │     │
│   │                                                   │     │
│   │  vs TensorFlow 1.x 的静态计算图：                     │     │
│   │  • TensorFlow：先定义图，再执行（编译式）          │     │
│   │  • PyTorch：边执行边构建（解释式）                │     │
│   └───────────────────────────────────────────────────┘     │
│                                                             │
│   2. 易于使用                                               │
│   ┌───────────────────────────────────────────────────┐     │
│   │  • API 设计简洁直观                                 │     │
│   │  • 与 NumPy 接口相似，学习曲线平缓                   │     │
│   │  • Python 原生风格，易于调试                         │     │
│   └───────────────────────────────────────────────────┘     │
│                                                             │
│   3. 强大的 GPU 支持                                         │
│   ┌───────────────────────────────────────────────────┐     │
│   │  • 无缝 CPU/GPU 切换                                 │     │
│   │  • CUDA/cuDNN 优化                                  │     │
│   │  • 分布式训练支持                                  │     │
│   └───────────────────────────────────────────────────┘     │
│                                                             │
│   4. 丰富的生态系统                                         │
│   ┌───────────────────────────────────────────────────┐     │
│   │  • torchvision：计算机视觉工具                     │     │
│   │  • torchtext：自然语言处理工具                     │     │
│   │  • torchaudio：音频处理工具                        │     │
│   │  • PyTorch Lightning：高级训练框架                │     │
│   │  • Hugging Face：预训练模型库                      │     │
│   └───────────────────────────────────────────────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### 36.2 安装与配置

#### 概念说明

正确安装 PyTorch 是开始深度学习的第一步。

**安装命令：**

```bash
# 创建项目
uv init pytorch-learning
cd pytorch-learning

# CPU 版本（适合学习）
uv add torch torchvision torchaudio

# GPU 版本（需要 NVIDIA GPU 和 CUDA）
# 访问 https://pytorch.org 获取最新安装命令
# 例如 CUDA 11.8:
# uv add torch --index https://download.pytorch.org/whl/cu118

# 验证安装
python -c "import torch; print(torch.__version__)"
```

**验证 GPU 支持：**

```python
import torch

print(f"PyTorch 版本：{torch.__version__}")
print(f"CUDA 可用：{torch.cuda.is_available()}")
print(f"cuDNN 版本：{torch.backends.cudnn.version()}")

if torch.cuda.is_available():
    print(f"GPU 数量：{torch.cuda.device_count()}")
    print(f"当前 GPU: {torch.cuda.get_device_name(0)}")
    print(f"GPU 内存：{torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB")
```

---

## 第二部分：Tensor 基础

### 36.3 Tensor 创建

#### 概念说明

Tensor（张量）是 PyTorch 的基本数据结构，类似于 NumPy 的 ndarray，但支持 GPU 加速和自动求导。

**创建 Tensor 的方法：**

```python
import torch
import numpy as np

# 方法 1：从列表创建
x = torch.tensor([1, 2, 3, 4, 5])
print(f"从列表：{x}")

# 方法 2：指定形状
x_zeros = torch.zeros(3, 4)        # 全 0 张量
x_ones = torch.ones(2, 3, 4)       # 全 1 张量
x_full = torch.full((2, 2), 7)     # 填充指定值
x_eye = torch.eye(3)               # 单位矩阵

# 方法 3：随机初始化
x_rand = torch.rand(3, 4)          # [0,1) 均匀分布
x_randn = torch.randn(3, 4)        # 标准正态分布
x_randint = torch.randint(0, 10, (2, 3))  # 随机整数

# 方法 4：从 NumPy 转换
np_array = np.array([[1, 2], [3, 4]])
x_from_np = torch.from_numpy(np_array)

# 方法 5：arange 和 linspace
x_range = torch.arange(0, 10, 2)        # [0, 2, 4, 6, 8]
x_space = torch.linspace(0, 1, 5)       # [0, 0.25, 0.5, 0.75, 1]

# 方法 6：复制已有 Tensor
x_clone = x_rand.clone()           # 深拷贝
x_copy = x_rand.new_tensor([1, 2, 3])  # 使用相同设备/dtype
```

**Tensor 属性：**

```python
x = torch.randn(3, 4, 5)

print(f"形状：{x.shape}")      # torch.Size([3, 4, 5])
print(f"维度：{x.dim()}")      # 3
print(f"元素数：{x.numel()}")  # 60
print(f"数据类型：{x.dtype}")  # torch.float32
print(f"设备：{x.device}")     # cpu 或 cuda:0
print(f"需要梯度：{x.requires_grad}")  # False
```

---

### 36.4 Tensor 操作

#### 概念说明

PyTorch 提供丰富的 Tensor 操作函数。

**索引与切片：**

```python
x = torch.arange(12).reshape(3, 4)
print(x)
# tensor([[ 0,  1,  2,  3],
#         [ 4,  5,  6,  7],
#         [ 8,  9, 10, 11]])

# 索引
print(x[0, 2])      # 2
print(x[:, 1])      # 第 2 列
print(x[1, :])      # 第 2 行

# 切片
print(x[0:2, 1:3])  # 子矩阵

# 布尔索引
mask = x > 5
print(x[mask])      # [6, 7, 8, 9, 10, 11]
```

**形状变换：**

```python
x = torch.arange(12)

# reshape
x_reshaped = x.reshape(3, 4)

# view（返回同一数据的视图）
x_view = x.view(2, 6)

# transpose / permute
x_t = x_reshaped.t()           # 2D 转置
x_perm = x_reshaped.permute(1, 0)  # 多维排列

# squeeze / unsqueeze
x = torch.randn(3, 1, 4, 1)
x_squeezed = x.squeeze()       # 移除所有大小为 1 的维度
x_unsqueeze = x_squeezed.unsqueeze(0)  # 增加维度
```

**数学运算：**

```python
a = torch.randn(3, 4)
b = torch.randn(3, 4)

# 逐元素运算
c = a + b          # 加法
c = a * b          # 乘法
c = torch.add(a, b)

# 矩阵乘法
c = torch.matmul(a, b.t())    # 矩阵乘法
c = a @ b.t()                 # 简化写法

# 统计运算
mean = a.mean()      # 均值
std = a.std()        # 标准差
max_val, max_idx = a.max(dim=1)  # 最大值及其索引
sum_val = a.sum()    # 求和
```

---

### 36.5 GPU 加速

#### 概念说明

PyTorch 可以轻松地将 Tensor 移动到 GPU 进行加速计算。

```python
import torch

# 检查 CUDA 可用性
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"使用设备：{device}")

# 创建 Tensor 并移动到 GPU
x = torch.randn(3, 4)
x_gpu = x.to(device)

# 或直接在 GPU 上创建
y = torch.randn(3, 4, device=device)

# GPU 计算
z = x_gpu + y

# 移回 CPU
z_cpu = z.cpu()

# 最佳实践：在代码开头定义设备
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# 后续所有 Tensor 和模型都使用这个设备
```

---

## 第三部分：自动求导（autograd）

### 36.6 autograd 基础

#### 概念说明

PyTorch 的 autograd 模块提供自动微分功能，是神经网络训练的核心。

```
┌─────────────────────────────────────────────────────────────┐
│                  autograd 工作原理                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   1. 创建 Tensor 时设置 requires_grad=True                   │
│      • PyTorch 会跟踪所有对该 Tensor 的操作                   │
│      • 构建计算图                                            │
│                                                             │
│   2. 计算损失函数                                            │
│      • 所有中间结果都被记录                                  │
│                                                             │
│   3. 调用 backward()                                          │
│      • 自动计算梯度                                           │
│      • 梯度存储在 .grad 属性中                                │
│                                                             │
│   4. 更新参数                                                │
│      • 使用梯度下降更新权重                                  │
│      • 清零梯度（重要！）                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**代码示例：**

```python
import torch

# 创建需要梯度的 Tensor
x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
w = torch.tensor([0.5, 1.0, 1.5], requires_grad=True)
b = torch.tensor([0.1], requires_grad=True)

# 前向计算
z = x * w + b      # 线性变换
y = z.sum()        # 输出标量

# 反向传播
y.backward()

# 查看梯度
print(f"x 的梯度：{x.grad}")  # [0.5, 1.0, 1.5]
print(f"w 的梯度：{w.grad}")  # [1.0, 2.0, 3.0]
print(f"b 的梯度：{b.grad}")  # [3.0]

# 停止梯度追踪
with torch.no_grad():
    w -= 0.01 * w.grad
    b -= 0.01 * b.grad
    # 清零梯度
    w.grad.zero_()
    b.grad.zero_()
```

---

### 36.7 计算图

#### 概念说明

PyTorch 动态构建计算图，记录所有操作以便反向传播。

```python
import torch

# 构建计算图
x = torch.tensor(2.0, requires_grad=True)
y = torch.tensor(3.0, requires_grad=True)

z = x ** 2 + y ** 2 + x * y  # 复杂运算
w = z * 2

# 反向传播
w.backward()

print(f"dz/dx = {x.grad}")  # 2x + y = 7
print(f"dz/dy = {y.grad}")  # 2y + x = 8

# 查看计算图
print(f"\nz 的梯度函数：{z.grad_fn}")
print(f"w 的梯度函数：{w.grad_fn}")
```

---

## 第四部分：神经网络搭建

### 36.8 nn.Module

#### 概念说明

`nn.Module` 是 PyTorch 中所有神经网络模块的基类。

**基本用法：**

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class SimpleNN(nn.Module):
    """简单全连接神经网络"""

    def __init__(self, input_size, hidden_size, output_size):
        super(SimpleNN, self).__init__()

        # 定义层
        self.fc1 = nn.Linear(input_size, hidden_size)  # 全连接层 1
        self.fc2 = nn.Linear(hidden_size, hidden_size)  # 全连接层 2
        self.fc3 = nn.Linear(hidden_size, output_size)  # 输出层

        # 可选：批量归一化
        self.bn1 = nn.BatchNorm1d(hidden_size)
        self.bn2 = nn.BatchNorm1d(hidden_size)

        # 可选：Dropout
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):
        """前向传播"""
        # 第 1 层 + ReLU + BN + Dropout
        x = self.fc1(x)
        x = F.relu(x)
        x = self.bn1(x)
        x = self.dropout(x)

        # 第 2 层 + ReLU + BN + Dropout
        x = self.fc2(x)
        x = F.relu(x)
        x = self.bn2(x)
        x = self.dropout(x)

        # 输出层
        x = self.fc3(x)

        return x


# 创建模型
model = SimpleNN(input_size=784, hidden_size=128, output_size=10)
print(model)
```

**常用 nn 模块：**

```python
# 全连接层
nn.Linear(in_features, out_features)

# 卷积层
nn.Conv2d(in_channels, out_channels, kernel_size, stride=1, padding=0)

# 池化层
nn.MaxPool2d(kernel_size, stride)
nn.AvgPool2d(kernel_size)

# 归一化层
nn.BatchNorm1d/2d(num_features)
nn.LayerNorm(normalized_shape)

# 激活函数（也可以用 F.函数形式）
nn.ReLU()
nn.Sigmoid()
nn.Softmax(dim=1)
nn.GELU()

# Dropout
nn.Dropout(p=0.5)

# Embedding（词嵌入）
nn.Embedding(num_embeddings, embedding_dim)

# RNN/LSTM/GRU
nn.RNN(input_size, hidden_size, num_layers)
nn.LSTM(input_size, hidden_size, num_layers)
nn.GRU(input_size, hidden_size, num_layers)
```

---

### 36.9 Sequential 模型

#### 概念说明

`nn.Sequential` 用于快速搭建简单的顺序网络。

```python
import torch.nn as nn

# 方式 1：传入有序字典
model = nn.Sequential(
    nn.Linear(784, 256),
    nn.ReLU(),
    nn.Dropout(0.5),
    nn.Linear(256, 128),
    nn.ReLU(),
    nn.Dropout(0.5),
    nn.Linear(128, 10)
)

# 方式 2：使用 OrderedDict
from collections import OrderedDict

model = nn.Sequential(OrderedDict([
    ('fc1', nn.Linear(784, 256)),
    ('relu1', nn.ReLU()),
    ('drop1', nn.Dropout(0.5)),
    ('fc2', nn.Linear(256, 128)),
    ('relu2', nn.ReLU()),
    ('drop2', nn.Dropout(0.5)),
    ('fc3', nn.Linear(128, 10))
]))

# 使用模型
x = torch.randn(32, 784)
output = model(x)
```

---

## 第五部分：数据加载

### 36.10 Dataset 与 DataLoader

#### 概念说明

PyTorch 提供 `Dataset` 和 `DataLoader` 用于高效数据加载。

**Dataset 基础：**

```python
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
import os

class CustomDataset(Dataset):
    """自定义数据集"""

    def __init__(self, data_dir, transform=None):
        self.data_dir = data_dir
        self.transform = transform

        # 获取所有文件路径
        self.file_paths = []
        for filename in os.listdir(data_dir):
            if filename.endswith('.jpg'):
                self.file_paths.append(os.path.join(data_dir, filename))

        # 加载标签（假设文件名包含类别）
        self.labels = [int(p.split('/')[-1].split('_')[0])
                       for p in self.file_paths]

    def __len__(self):
        """返回数据集大小"""
        return len(self.file_paths)

    def __getitem__(self, idx):
        """获取单个样本"""
        img_path = self.file_paths[idx]
        label = self.labels[idx]

        # 加载图片
        image = Image.open(img_path).convert('RGB')

        # 应用变换
        if self.transform:
            image = self.transform(image)

        return image, label


# 数据变换
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

# 创建数据集
train_dataset = CustomDataset('data/train', transform=transform)
val_dataset = CustomDataset('data/val', transform=transform)

# 创建 DataLoader
train_loader = DataLoader(
    train_dataset,
    batch_size=32,
    shuffle=True,      # 训练时打乱
    num_workers=4,     # 数据加载进程数
    pin_memory=True    # 加速 CPU 到 GPU 传输
)

val_loader = DataLoader(
    val_dataset,
    batch_size=32,
    shuffle=False,
    num_workers=4
)
```

**使用内置数据集：**

```python
from torchvision import datasets, transforms

# MNIST 手写数字
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])

train_dataset = datasets.MNIST(
    root='./data',
    train=True,
    download=True,
    transform=transform
)

test_dataset = datasets.MNIST(
    root='./data',
    train=False,
    download=True,
    transform=transform
)

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=128, shuffle=False)
```

---

## 第六部分：训练流程

### 36.11 完整训练循环

#### 概念说明

一个标准的深度学习训练流程包含以下步骤。

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms

# 1. 准备数据
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

train_dataset = datasets.MNIST('./data', train=True, download=True, transform=transform)
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)

test_dataset = datasets.MNIST('./data', train=False, transform=transform)
test_loader = DataLoader(test_dataset, batch_size=128, shuffle=False)

# 2. 创建模型
model = nn.Sequential(
    nn.Flatten(),
    nn.Linear(28*28, 128),
    nn.ReLU(),
    nn.Dropout(0.5),
    nn.Linear(128, 10)
)

# 3. 定义损失函数和优化器
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 4. 训练循环
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

num_epochs = 10

for epoch in range(num_epochs):
    model.train()  # 训练模式
    running_loss = 0.0
    correct = 0
    total = 0

    for batch_idx, (data, target) in enumerate(train_loader):
        data, target = data.to(device), target.to(device)

        # 前向传播
        optimizer.zero_grad()  # 清零梯度
        output = model(data)
        loss = criterion(output, target)

        # 反向传播
        loss.backward()
        optimizer.step()

        # 统计
        running_loss += loss.item()
        _, predicted = output.max(1)
        total += target.size(0)
        correct += predicted.eq(target).sum().item()

    # 计算 epoch 平均结果
    train_loss = running_loss / len(train_loader)
    train_acc = 100. * correct / total

    print(f"Epoch {epoch+1}/{num_epochs}")
    print(f"  Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.2f}%")

    # 5. 验证
    model.eval()  # 评估模式
    test_loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():
        for data, target in test_loader:
            data, target = data.to(device), target.to(device)
            output = model(data)
            test_loss += criterion(output, target).item()
            _, predicted = output.max(1)
            total += target.size(0)
            correct += predicted.eq(target).sum().item()

    test_loss /= len(test_loader)
    test_acc = 100. * correct / total

    print(f"  Test Loss: {test_loss:.4f}, Test Acc: {test_acc:.2f}%")
```

---

### 36.12 模型保存与加载

#### 概念说明

训练好的模型可以保存下来供后续使用。

```python
# 保存模型参数（推荐方式）
torch.save(model.state_dict(), 'model.pth')

# 加载模型参数
model = SimpleNN()  # 先创建模型实例
model.load_state_dict(torch.load('model.pth'))
model.eval()  # 设置为评估模式

# 保存完整模型（不推荐，依赖具体类定义）
torch.save(model, 'complete_model.pth')

# 加载完整模型
model = torch.load('complete_model.pth')
```

**保存检查点（包含更多训练信息）：**

```python
# 保存检查点
checkpoint = {
    'epoch': epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'loss': loss,
    'acc': acc
}
torch.save(checkpoint, 'checkpoint.pth')

# 加载检查点
checkpoint = torch.load('checkpoint.pth')
model.load_state_dict(checkpoint['model_state_dict'])
optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
epoch = checkpoint['epoch']
loss = checkpoint['loss']
```

---

## 本章小结

```
┌─────────────────────────────────────────────────────────────┐
│                      第 36 章 知识要点                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   PyTorch 基础：                                              │
│   ✓ 优势：动态计算图、易用、GPU 支持、生态丰富                │
│   ✓ 安装：torch + torchvision + torchaudio                  │
│   ✓ 设备：device = cuda if available else cpu               │
│                                                             │
│   Tensor 操作：                                              │
│   ✓ 创建：tensor/zeros/ones/rand/randn/arange              │
│   ✓ 属性：shape/dim/numel/dtype/device                     │
│   ✓ 操作：索引切片/reshape/transpose/math                   │
│   ✓ GPU：to(device)/cuda()/cpu()                            │
│                                                             │
│   autograd:                                                  │
│   ✓ requires_grad=True: 开启梯度追踪                        │
│   ✓ backward(): 反向传播计算梯度                            │
│   ✓ .grad: 存储梯度                                          │
│   ✓ no_grad(): 停止梯度追踪                                  │
│                                                             │
│   nn.Module:                                                 │
│   ✓ 定义：继承 nn.Module，实现__init__和 forward            │
│   ✓ 层：Linear/Conv2d/BatchNorm/Dropout                     │
│   ✓ Sequential: 快速搭建顺序网络                             │
│                                                             │
│   Dataset/DataLoader:                                        │
│   ✓ Dataset: __len__() 和__getitem__()                      │
│   ✓ DataLoader: batch_size/shuffle/num_workers              │
│   ✓ transforms: Resize/ToTensor/Normalize                   │
│                                                             │
│   训练流程：                                                 │
│   ✓ 训练模式：model.train()                                 │
│   ✓ 评估模式：model.eval()                                  │
│   ✓ 步骤：zero_grad → forward → loss → backward → step      │
│   ✓ 保存：state_dict() / load_state_dict()                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

[上一章](./35-神经网络基础.md) | [下一章](./37-卷积神经网络 CNN.md)
