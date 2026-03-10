# 第 37 章 - 卷积神经网络 CNN

> 卷积神经网络是计算机视觉的核心技术，本章介绍 CNN 的原理和应用。

---

## 第一部分 - CNN 基础

### 1.1 卷积层

```python
import torch.nn as nn

# 2D 卷积
conv = nn.Conv2d(
    in_channels=3,    # 输入通道数
    out_channels=64,  # 输出通道数
    kernel_size=3,    # 卷积核大小
    stride=1,         # 步长
    padding=1         # 填充
)
```

### 1.2 池化层

```python
# 最大池化
maxpool = nn.MaxPool2d(kernel_size=2, stride=2)

# 平均池化
avgpool = nn.AvgPool2d(kernel_size=2, stride=2)
```

---

## 第二部分 - 经典 CNN 架构

### 2.1 LeNet-5

```python
class LeNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16*4*4, 120)
        self.fc2 = nn.Linear(120, 10)
    
    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = self.pool(torch.relu(self.conv2(x)))
        x = x.view(-1, 16*4*4)
        x = torch.relu(self.fc1(x))
        return self.fc2(x)
```

### 2.2 使用预训练模型

```python
from torchvision import models

# ResNet18
resnet = models.resnet18(pretrained=True)

# VGG16
vgg = models.vgg16(pretrained=True)

# 微调
for param in resnet.parameters():
    param.requires_grad = False

# 替换最后的全连接层
resnet.fc = nn.Linear(resnet.fc.in_features, num_classes)
```

---

## 第三部分 - 图像分类实战

```python
import torch
from torchvision import datasets, transforms

# 数据预处理
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485], std=[0.229])
])

# 加载数据
train_data = datasets.ImageFolder('data/train', transform=transform)
train_loader = torch.utils.data.DataLoader(train_data, batch_size=32)
```
---

[← 上一篇](./07-PyTorch 入门.md) | [下一篇 →](./09-循环神经网络 RNN.md)
