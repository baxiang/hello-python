# 第 38 章 - 循环神经网络 RNN

> 循环神经网络适用于序列数据处理，本章介绍 RNN、LSTM、GRU 及其应用。

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
class TextClassifier(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, num_classes):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, num_classes)
    
    def forward(self, x):
        # x: (batch, seq_len)
        embedded = self.embedding(x)  # (batch, seq_len, embed_dim)
        _, (hidden, _) = self.lstm(embedded)
        return self.fc(hidden[-1])  # 使用最后时刻的隐藏状态

# 使用
model = TextClassifier(vocab_size=10000, embed_dim=128, hidden_dim=256, num_classes=10)
```

---

## 第三部分 - 序列到序列

```python
class Seq2Seq(nn.Module):
    def __init__(self, encoder, decoder):
        super().__init__()
        self.encoder = encoder
        self.decoder = decoder
    
    def forward(self, src, tgt):
        # Encoder
        enc_output, enc_hidden = self.encoder(src)
        
        # Decoder
        dec_output, dec_hidden = self.decoder(tgt, enc_hidden)
        
        return dec_output
```
---

[← 上一篇](./08-卷积神经网络 CNN.md) | [下一篇 →](./10-深度学习实战.md)
