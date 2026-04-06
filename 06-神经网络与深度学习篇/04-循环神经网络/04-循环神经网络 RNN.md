# 第 38 章 - 循环神经网络 RNN

> **Python 版本要求：** 本章代码需要 Python 3.11+ 运行环境
>
> 循环神经网络适用于序列数据处理，本章介绍 RNN、LSTM、GRU 及其应用。

---

## 实际场景

**文本序列预测：预测下一个词**

假设你在开发一个智能输入法，需要根据用户已输入的文字预测下一个词。使用 RNN，你可以：

1. 将文本转换为词向量序列
2. RNN/LSTM 逐词处理，记住上下文信息
3. 根据隐藏状态预测下一个词的概率分布

RNN 特别适合处理序列数据（文本、语音、时间序列），因为它能记住历史信息，理解上下文关系。

---

## 第一部分 - RNN 基础

### 1.1 RNN 原理

RNN 通过隐藏状态保存序列信息，适用于时间序列、文本等序列数据。

### 1.2 PyTorch 实现

```python
import torch.nn as nn

# 基础 RNN
rnn = nn.RNN(
    input_size=100,   # 输入特征维度
    hidden_size=256,  # 隐藏层维度
    num_layers=2,     # 层数
    batch_first=True  # 输入格式 (batch, seq, feature)
)

# LSTM（长短期记忆网络）
lstm = nn.LSTM(
    input_size=100,
    hidden_size=256,
    num_layers=2,
    batch_first=True
)

# GRU（门控循环单元）
gru = nn.GRU(
    input_size=100,
    hidden_size=256,
    num_layers=2,
    batch_first=True
)
```

---

## 第二部分 - 文本分类实战

```python
import torch.nn as nn
from torch import Tensor

class TextClassifier(nn.Module):
    def __init__(self, vocab_size: int, embed_dim: int, hidden_dim: int, num_classes: int) -> None:
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, num_classes)
    
    def forward(self, x: Tensor) -> Tensor:
        embedded: Tensor = self.embedding(x)
        _, (hidden, _) = self.lstm(embedded)
        return self.fc(hidden[-1])

model = TextClassifier(vocab_size=10000, embed_dim=128, hidden_dim=256, num_classes=10)
```

---

## 第三部分 - 序列到序列

```python
import torch.nn as nn
from torch import Tensor

class Seq2Seq(nn.Module):
    def __init__(self, encoder: nn.Module, decoder: nn.Module) -> None:
        super().__init__()
        self.encoder = encoder
        self.decoder = decoder
    
    def forward(self, src: Tensor, tgt: Tensor) -> Tensor:
        enc_output: Tensor
        enc_hidden: Tensor
        enc_output, enc_hidden = self.encoder(src)
        
        dec_output: Tensor
        dec_hidden: Tensor
        dec_output, dec_hidden = self.decoder(tgt, enc_hidden)
        
        return dec_output
```
