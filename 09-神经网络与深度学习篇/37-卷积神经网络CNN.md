# 第 37 章 - 卷积神经网络 CNN（详细版）

本章讲解卷积神经网络（CNN）的原理、结构和应用，包括卷积层、池化层、经典架构和图像分类实战。

---

## 第一部分：卷积层

### 37.1 为什么需要 CNN

#### 概念说明

CNN 专为处理网格状数据（如图像）而设计，相比全连接网络有明显优势。

**全连接 vs 卷积：**

```
┌─────────────────────────────────────────────────────────────┐
│              全连接网络 vs 卷积神经网络                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   全连接网络的问题：                                         │
│   ┌───────────────────────────────────────────────────┐     │
│   │  处理 224x224 RGB 图像：                             │     │
│   │  • 输入维度：224 × 224 × 3 = 150,528               │     │
│   │  • 单隐藏层（1000 神经元）参数量：150M+             │     │
│   │  • 参数过多，容易过拟合                            │     │
│   │  • 忽略图像的空间结构                              │     │
│   └───────────────────────────────────────────────────┘     │
│                                                             │
│   CNN 的优势：                                               │
│   ┌───────────────────────────────────────────────────┐     │
│   │  1. 局部连接（Local Connectivity）                 │     │
│   │     • 每个神经元只连接局部区域                     │     │
│   │     • 大幅减少参数量                              │     │
│   │                                                   │     │
│   │  2. 权值共享（Weight Sharing）                     │     │
│   │     • 同一卷积核在图像上滑动                       │     │
│   │     • 检测相同特征的不同位置                       │     │
│   │                                                   │     │
│   │  3. 空间层次结构                                   │     │
│   │     • 浅层：边缘、纹理                            │     │
│   │     • 中层：形状、部件                            │     │
│   │     • 深层：物体、语义                            │     │
│   └───────────────────────────────────────────────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### 37.2 卷积操作

#### 概念说明

卷积是 CNN 的核心操作，通过卷积核（滤波器）提取图像特征。

**2D 卷积工作原理：**

```
┌─────────────────────────────────────────────────────────────┐
│                  2D 卷积操作                                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   输入图像 (5x5)        卷积核 (3x3)         输出 (3x3)      │
│                                                             │
│   ┌─────────┐          ┌───────┐           ┌─────┐         │
│   │ 1 1 1 0 0│          │ 1 0 1 │           │ 1 1 1│         │
│   │ 1 1 1 0 0│    *     │ 0 1 0 │    =      │ 1 1  │         │
│   │ 1 1 1 0 0│          │ 1 0 1 │           │ 1   │         │
│   │ 0 0 1 1 1│          └───────┘           └─────┘         │
│   │ 0 0 1 1 1│                                               │
│   └─────────┘                                                │
│                                                             │
│   计算过程（以左上角为例）：                                  │
│   1×1 + 1×0 + 1×1 +                                         │
│   1×0 + 1×1 + 1×0 +                                         │
│   1×1 + 1×0 + 1×1 = 5                                       │
│                                                             │
│   关键概念：                                                 │
│   • 卷积核（Kernel/Filter）：提取特征的模板                 │
│   • 步长（Stride）：每次滑动的距离                          │
│   • 填充（Padding）：边缘补零，保持尺寸                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**PyTorch 实现：**

```python
import torch
import torch.nn as nn

# 2D 卷积层
conv = nn.Conv2d(
    in_channels=3,       # 输入通道数（RGB 图像）
    out_channels=64,     # 输出通道数（卷积核数量）
    kernel_size=3,       # 卷积核大小
    stride=1,            # 步长
    padding=1            # 填充（保持尺寸）
)

# 输入：[batch_size, channels, height, width]
x = torch.randn(32, 3, 224, 224)  # 32 张 224x224 RGB 图像
output = conv(x)

print(f"输入形状：{x.shape}")      # [32, 3, 224, 224]
print(f"输出形状：{output.shape}")  # [32, 64, 224, 224]
print(f"参数量：{sum(p.numel() for p in conv.parameters())}")
```

**输出尺寸计算：**

```
输出尺寸 = (输入尺寸 - 卷积核大小 + 2×填充) / 步长 + 1

示例：
输入：224×224，卷积核 3×3，stride=1，padding=1
输出 = (224 - 3 + 2×1) / 1 + 1 = 224

输入：224×224，卷积核 3×3，stride=2，padding=1
输出 = (224 - 3 + 2×1) / 2 + 1 = 112
```

---

### 37.3 填充与步长

#### 概念说明

Padding 和 Stride 控制卷积的输出尺寸和感受野。

**Padding（填充）：**

```
┌─────────────────────────────────────────────────────────────┐
│                    Padding 填充                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Valid Padding（无填充）：                                  │
│   ┌───────┐                                                 │
│   │███████│  输入 5x5，卷积核 3x3，输出 3x3                  │
│   │███████│                                                 │
│   │███████│                                                 │
│   │███████│                                                 │
│   │███████│                                                 │
│   └───────┘                                                 │
│                                                             │
│   Same Padding（填充保持尺寸）：                             │
│   ┌───────────┐                                             │
│   │░░░░░░░░░░░│  输入 5x5+padding=7x7，输出 5x5              │
│   │░███████░░░│                                             │
│   │░███████░░░│  边缘补零保持尺寸                           │
│   │░███████░░░│                                             │
│   │░███████░░░│                                             │
│   │░███████░░░│                                             │
│   └───────────┘                                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Stride（步长）：**

```python
import torch.nn as nn

# stride=1（不缩小）
conv1 = nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1)
# 输入 224x224 → 输出 224x224

# stride=2（缩小一半）
conv2 = nn.Conv2d(3, 64, kernel_size=3, stride=2, padding=1)
# 输入 224x224 → 输出 112x112
```

---

## 第二部分：池化层

### 37.4 池化操作

#### 概念说明

池化层用于降低特征图的空间尺寸，减少计算量和参数数量。

**最大池化 vs 平均池化：**

```
┌─────────────────────────────────────────────────────────────┐
│                    池化操作                                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   最大池化（Max Pooling）：                                  │
│   ┌───────────┐      ┌─────┐                               │
│   │ 1 3 2 4   │      │ 3 4 │  取每个区域的最大值            │
│   │ 5 2 1 3   │  →   │ 6 5 │                               │
│   │ 1 4 6 2   │      └─────┘                               │
│   │ 3 2 5 1   │                                            │
│   └───────────┘                                            │
│   2x2 池化，stride=2                                        │
│                                                             │
│   平均池化（Average Pooling）：                              │
│   ┌───────────┐      ┌─────┐                               │
│   │ 1 3 2 4   │      │2.75 3.0│取每个区域的平均值           │
│   │ 5 2 1 3   │  →   │      │                               │
│   │ 1 4 6 2   │      │3.25 2.75│                            │
│   │ 3 2 5 1   │      └─────┘                               │
│   └───────────┘                                            │
│                                                             │
│   作用：                                                     │
│   • 降维：减少计算量                                        │
│   • 不变性：对小平移、旋转不敏感                            │
│   • 防止过拟合：减少参数                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**PyTorch 实现：**

```python
import torch.nn as nn

# 最大池化
max_pool = nn.MaxPool2d(kernel_size=2, stride=2)

# 平均池化
avg_pool = nn.AvgPool2d(kernel_size=2, stride=2)

# 全局平均池化（整个特征图取平均）
global_avg_pool = nn.AdaptiveAvgPool2d((1, 1))

# 输入输出
x = torch.randn(32, 64, 112, 112)
output = max_pool(x)
print(f"输出形状：{output.shape}")  # [32, 64, 56, 56]
```

---

## 第三部分：经典 CNN 架构

### 37.5 LeNet-5

#### 概念说明

LeNet-5 是最早成功的 CNN 架构，由 Yann LeCun 于 1998 年提出，用于手写数字识别。

**网络结构：**

```
LeNet-5 结构：

输入 (32x32) → Conv1(6@28x28) → AvgPool → Conv2(16@10x10) → AvgPool →
FC1(120) → FC2(84) → Output(10)
```

**PyTorch 实现：**

```python
import torch.nn as nn
import torch.nn.functional as F

class LeNet5(nn.Module):
    def __init__(self):
        super(LeNet5, self).__init__()

        # 卷积层
        self.conv1 = nn.Conv2d(1, 6, kernel_size=5)  # 32x32 → 28x28
        self.conv2 = nn.Conv2d(6, 16, kernel_size=5) # 14x14 → 10x10

        # 池化层
        self.pool = nn.AvgPool2d(2, 2)

        # 全连接层
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))  # 32x32 → 14x14
        x = self.pool(F.relu(self.conv2(x)))  # 14x14 → 5x5
        x = x.view(-1, 16 * 5 * 5)            # 展平
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x
```

---

### 37.6 AlexNet

#### 概念说明

AlexNet 在 2012 年 ImageNet 竞赛中取得突破性成果，开启了深度学习革命。

**关键创新：**
- ReLU 激活函数
- Dropout 防止过拟合
- GPU 训练
- 数据增强

**简化版实现：**

```python
class AlexNet(nn.Module):
    def __init__(self, num_classes=1000):
        super(AlexNet, self).__init__()

        # 特征提取部分
        self.features = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=11, stride=4, padding=2),  # 224→55
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=3, stride=2),                   # 55→27
            nn.Conv2d(64, 192, kernel_size=3, padding=1),           # 27→27
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=3, stride=2),                   # 27→13
            nn.Conv2d(192, 384, kernel_size=3, padding=1),          # 13→13
            nn.ReLU(),
            nn.Conv2d(384, 256, kernel_size=3, padding=1),          # 13→13
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=3, stride=2),                   # 13→6
        )

        # 分类部分
        self.classifier = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(256 * 6 * 6, 4096),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(4096, 4096),
            nn.ReLU(),
            nn.Linear(4096, num_classes),
        )

    def forward(self, x):
        x = self.features(x)
        x = x.view(x.size(0), -1)  # 展平
        x = self.classifier(x)
        return x
```

---

### 37.7 ResNet

#### 概念说明

ResNet（残差网络）通过跳跃连接解决了深层网络的梯度消失问题，使训练数百层的网络成为可能。

**残差块（Residual Block）：**

```
┌─────────────────────────────────────────────────────────────┐
│                  ResNet 残差块                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   普通块：                                                   │
│   x → Conv → BN → ReLU → Conv → BN → (+x) → ReLU → output  │
│                         ↑                                    │
│                         └───────┘                           │
│                        跳跃连接                              │
│                                                             │
│   公式：output = F(x) + x                                   │
│                                                             │
│   优势：                                                     │
│   • 解决梯度消失问题                                        │
│   • 可以训练非常深的网络（18/34/50/101/152 层）              │
│   • 恒等映射更容易学习                                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**PyTorch 实现：**

```python
import torch.nn as nn

class ResidualBlock(nn.Module):
    """基本残差块"""

    def __init__(self, in_channels, out_channels, stride=1):
        super(ResidualBlock, self).__init__()

        self.conv1 = nn.Conv2d(in_channels, out_channels,
                                kernel_size=3, stride=stride,
                                padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.conv2 = nn.Conv2d(out_channels, out_channels,
                                kernel_size=3, stride=1,
                                padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)

        # 跳跃连接（可能需要 1x1 卷积调整维度）
        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=1,
                         stride=stride, bias=False),
                nn.BatchNorm2d(out_channels)
            )

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += self.shortcut(x)  # 跳跃连接
        out = F.relu(out)
        return out


# 使用 torchvision 的预训练 ResNet
from torchvision import models

resnet18 = models.resnet18(pretrained=True)
resnet50 = models.resnet50(pretrained=True)

# 迁移学习：冻结骨干网络，只训练分类头
for param in resnet18.parameters():
    param.requires_grad = False

# 替换最后的全连接层
resnet18.fc = nn.Linear(resnet18.fc.in_features, num_classes)
```

---

## 第四部分：图像分类实战

### 37.8 完整训练代码

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
import time

# 1. 数据准备
data_transforms = {
    'train': transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                            [0.229, 0.224, 0.225])
    ]),
    'val': transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406],
                            [0.229, 0.224, 0.225])
    ]),
}

data_dir = 'data/hymenoptera_data'
image_datasets = {
    x: datasets.ImageFolder(root=f'{data_dir}/{x}',
                           transform=data_transforms[x])
    for x in ['train', 'val']
}

dataloaders = {
    x: DataLoader(image_datasets[x], batch_size=32, shuffle=True, num_workers=4)
    for x in ['train', 'val']
}

dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'val']}
class_names = image_datasets['train'].classes

# 2. 创建模型（使用预训练 ResNet18）
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = models.resnet18(pretrained=True)

# 冻结骨干网络
for param in model.parameters():
    param.requires_grad = False

# 替换分类头
num_features = model.fc.in_features
model.fc = nn.Linear(num_features, len(class_names))
model = model.to(device)

# 3. 损失函数和优化器
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.fc.parameters(), lr=0.001)

# 4. 训练函数
def train_model(model, criterion, optimizer, num_epochs=25):
    since = time.time()

    for epoch in range(num_epochs):
        print(f'Epoch {epoch+1}/{num_epochs}')
        print('-' * 10)

        # 每个 epoch 有训练和验证阶段
        for phase in ['train', 'val']:
            if phase == 'train':
                model.train()
            else:
                model.eval()

            running_loss = 0.0
            running_corrects = 0

            # 迭代数据
            for inputs, labels in dataloaders[phase]:
                inputs = inputs.to(device)
                labels = labels.to(device)

                # 前向
                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)

                    # 后向（仅训练阶段）
                    if phase == 'train':
                        optimizer.zero_grad()
                        loss.backward()
                        optimizer.step()

                # 统计
                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)

            epoch_loss = running_loss / dataset_sizes[phase]
            epoch_acc = running_corrects.double() / dataset_sizes[phase]

            print(f'{phase} Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}')

        print()

    time_elapsed = time.time() - since
    print(f'训练完成 耗时：{time_elapsed // 60:.0f}m {time_elapsed % 60:.0f}s')

    return model

# 5. 开始训练
model = train_model(model, criterion, optimizer, num_epochs=25)

# 6. 保存模型
torch.save(model.state_dict(), 'resnet18_finetuned.pth')
```

---

## 本章小结

```
┌─────────────────────────────────────────────────────────────┐
│                      第 37 章 知识要点                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   卷积层：                                                   │
│   ✓ 优势：局部连接、权值共享、空间层次结构                  │
│   ✓ 卷积操作：卷积核滑动、特征提取                          │
│   ✓ 输出计算：(W-K+2P)/S + 1                                │
│   ✓ 参数：in_channels、out_channels、kernel_size、stride、padding │
│                                                             │
│   池化层：                                                   │
│   ✓ 最大池化：取区域最大值（常用）                          │
│   ✓ 平均池化：取区域平均值                                  │
│   ✓ 全局池化：整个特征图取平均                              │
│   ✓ 作用：降维、不变性、防过拟合                            │
│                                                             │
│   经典架构：                                                 │
│   ✓ LeNet-5：早期成功应用（手写数字）                       │
│   ✓ AlexNet：ReLU、Dropout、GPU 训练                         │
│   ✓ ResNet：残差连接、训练深层网络                          │
│                                                             │
│   图像分类实战：                                             │
│   ✓ 数据增强：RandomCrop、RandomFlip、Normalize             │
│   ✓ 迁移学习：预训练模型、冻结骨干、微调分类头              │
│   ✓ 训练循环：train/eval 模式、梯度控制                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

[上一章](./36-PyTorch 入门.md) | [下一章](./38-循环神经网络 RNN.md)
