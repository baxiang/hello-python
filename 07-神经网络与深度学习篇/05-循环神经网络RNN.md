# 第 38 章 - 循环神经网络 RNN（详细版）

本章讲解循环神经网络（RNN）及其变体 LSTM、GRU 的原理和应用，包括序列建模、文本分类和情感分析。

---

## 第一部分：RNN 基础

### 38.1 为什么需要 RNN

#### 概念说明

RNN 专为处理序列数据设计，能够捕捉时间依赖和上下文信息。

**序列数据 vs 独立数据：**

```
┌─────────────────────────────────────────────────────────────┐
│              独立数据 vs 序列数据                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   独立数据（CNN/MLP 处理）：                                  │
│   ┌───────────────────────────────────────────────────┐     │
│   │  图像分类：每张图独立                              │     │
│   │  • 输入：图像 1, 图像 2, 图像 3                    │     │
│   │  • 输出：猫，狗，鸟                                │     │
│   │  • 图像之间无关联                                  │     │
│   └───────────────────────────────────────────────────┘     │
│                                                             │
│   序列数据（RNN 处理）：                                      │
│   ┌───────────────────────────────────────────────────┐     │
│   │  文本情感分析：                                    │     │
│   │  • 输入："这"→"部"→"电"→"影"→"很"→"好"             │     │
│   │  • 输出：正面                                      │     │
│   │  • 需要理解整个句子的上下文                        │     │
│   │                                                   │     │
│   │  语言模型：                                        │     │
│   │  • 输入："今天天气"                                │     │
│   │  • 预测："很好"                                    │     │
│   │  • 需要记住前面的词                               │     │
│   │                                                   │     │
│   │  机器翻译：                                        │     │
│   │  • 输入："I love Python"（英文序列）              │     │
│   │  • 输出："我爱 Python"（中文序列）                 │     │
│   │  • 输入输出都是序列                                │     │
│   └───────────────────────────────────────────────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**RNN 的应用场景：**

| 任务类型 | 输入→输出 | 示例 |
|---------|----------|------|
| 一对一 | 序列→类别 | 情感分析、文本分类 |
| 一对多 | 序列→序列 | 图像描述生成 |
| 多对一 | 序列→类别 | 情感分析 |
| 多对多 | 序列→序列 | 机器翻译、文本生成 |

---

### 38.2 RNN 结构

#### 概念说明

RNN 通过循环连接使信息能够在时间步之间传递。

**RNN 展开结构：**

```
┌─────────────────────────────────────────────────────────────┐
│                  RNN 展开结构                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   输入序列：x₁ → x₂ → x₃ → ... → xₜ                        │
│                                                             │
│   展开后的网络：                                             │
│                                                             │
│   时间步：    t=1      t=2      t=3           t=T           │
│              ┌───┐    ┌───┐    ┌───┐         ┌───┐         │
│   输入：     │x₁ │    │x₂ │    │x₃ │   ...   │xₜ │         │
│              └─┬─┘    └─┬─┘    └─┬─┘         └─┬─┘         │
│                │        │        │             │           │
│              ┌─▼───┐  ┌─▼───┐  ┌─▼───┐       ┌─▼───┐       │
│   隐藏状态：  │h₁  │→ │h₂  │→ │h₃  │   ...  →│hₜ  │       │
│              └─┬───┘  └─┬───┘  └─┬───┘       └─┬───┘       │
│                │        │        │             │           │
│              ┌─▼───┐  ┌─▼───┐  ┌─▼───┐       ┌─▼───┐       │
│   输出：      │y₁  │  │y₂  │  │y₃  │   ...   │yₜ  │       │
│              └─────┘  └─────┘  └─────┘       └─────┘       │
│                                                             │
│   隐藏状态计算：                                             │
│   hₜ = tanh(Wₓₕ·xₜ + Wₕₕ·hₜ₋₁ + bₕ)                        │
│   yₜ = softmax(Wₕᵧ·hₜ + bᵧ)                                 │
│                                                             │
│   关键特性：                                                 │
│   • 参数共享：Wₓₕ、Wₕₕ、Wₕᵧ 在所有时间步相同                   │
│   • 记忆能力：hₜ 包含之前所有时间步的信息                    │
│   • 变长输入：可以处理不同长度的序列                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**PyTorch 实现：**

```python
import torch
import torch.nn as nn

# 创建 RNN 层
rnn = nn.RNN(
    input_size=100,     # 输入特征维度
    hidden_size=256,    # 隐藏层维度
    num_layers=2,       # RNN 层数
    batch_first=True,   # 输入格式：[batch, seq, feature]
    dropout=0.2         # Dropout（多层时）
)

# 输入：[batch_size, sequence_length, input_size]
x = torch.randn(32, 50, 100)  # 32 个样本，每句 50 词，词向量 100 维

# 前向传播
output, h_n = rnn(x)

print(f"输入形状：{x.shape}")        # [32, 50, 100]
print(f"输出形状：{output.shape}")   # [32, 50, 256]
print(f"隐藏状态形状：{h_n.shape}")  # [2, 32, 256]
```

---

## 第二部分：LSTM 与 GRU

### 38.3 LSTM（长短期记忆网络）

#### 概念说明

LSTM 通过门控机制解决了传统 RNN 的长距离依赖问题。

**LSTM 结构：**

```
┌─────────────────────────────────────────────────────────────┐
│                  LSTM 单元结构                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   细胞状态（Cell State）：Cₜ₋₁ ──────→ Cₜ                  │
│   （长期记忆，贯穿整个序列）                                  │
│                                                             │
│   门控机制：                                                 │
│   ┌───────────────────────────────────────────────────┐     │
│   │                                                   │     │
│   │  1. 遗忘门（Forget Gate）：决定丢弃什么信息        │     │
│   │     fₜ = σ(Wf·[hₜ₋₁, xₜ] + bf)                    │     │
│   │     输出 0-1，0 表示完全丢弃，1 表示完全保留         │     │
│   │                                                   │     │
│   │  2. 输入门（Input Gate）：决定更新什么信息         │     │
│   │     iₜ = σ(Wi·[hₜ₋₁, xₜ] + bi)                    │     │
│   │     C̃ₜ = tanh(Wc·[hₜ₋₁, xₜ] + bc)                 │     │
│   │                                                   │     │
│   │  3. 更新细胞状态：                                 │     │
│   │     Cₜ = fₜ * Cₜ₋₁ + iₜ * C̃ₜ                      │     │
│   │                                                   │     │
│   │  4. 输出门（Output Gate）：决定输出什么信息        │     │
│   │     oₜ = σ(Wo·[hₜ₋₁, xₜ] + bo)                    │     │
│   │     hₜ = oₜ * tanh(Cₜ)                            │     │
│   │                                                   │     │
│   └───────────────────────────────────────────────────┘     │
│                                                             │
│   优势：                                                     │
│   ✓ 可以学习长距离依赖（100+ 时间步）                        │
│   ✓ 梯度流动更稳定                                          │
│   ✓ 广泛应用于 NLP 任务                                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**PyTorch 实现：**

```python
import torch.nn as nn

# 创建 LSTM 层
lstm = nn.LSTM(
    input_size=100,      # 输入特征维度
    hidden_size=256,     # 隐藏层维度
    num_layers=2,        # LSTM 层数
    batch_first=True,
    dropout=0.2,
    bidirectional=False  # 单向 LSTM
)

# 双向 LSTM
bi_lstm = nn.LSTM(
    input_size=100,
    hidden_size=128,     # 双向时每方向 128，总输出 256
    num_layers=1,
    batch_first=True,
    bidirectional=True   # 双向
)

# 输入输出
x = torch.randn(32, 50, 100)
output, (h_n, c_n) = lstm(x)

print(f"输出形状：{output.shape}")    # [32, 50, 256]
print(f"隐藏状态：{h_n.shape}")       # [2, 32, 256]
print(f"细胞状态：{c_n.shape}")       # [2, 32, 256]
```

---

### 38.4 GRU（门控循环单元）

#### 概念说明

GRU 是 LSTM 的简化版本，参数更少，训练更快。

**GRU vs LSTM：**

| 特性 | LSTM | GRU |
|------|------|-----|
| 门控数量 | 3 个（遗忘、输入、输出） | 2 个（更新、重置） |
| 细胞状态 | 有（Cₜ） | 无 |
| 参数数量 | 多 | 少（约 LSTM 的 75%） |
| 训练速度 | 较慢 | 较快 |
| 性能 | 略好（长序列） | 相当（中等序列） |

**GRU 结构：**

```
┌─────────────────────────────────────────────────────────────┐
│                    GRU 单元结构                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   1. 重置门（Reset Gate）：决定忘记多少过去                │
│      rₜ = σ(Wr·[hₜ₋₁, xₜ])                                 │
│                                                             │
│   2. 更新门（Update Gate）：决定更新多少                   │
│      zₜ = σ(Wz·[hₜ₋₁, xₜ])                                 │
│                                                             │
│   3. 候选隐藏状态：                                         │
│      h̃ₜ = tanh(rₜ * hₜ₋₁ + W·xₜ)                          │
│                                                             │
│   4. 新隐藏状态：                                           │
│      hₜ = (1 - zₜ) * hₜ₋₁ + zₜ * h̃ₜ                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**PyTorch 实现：**

```python
import torch.nn as nn

# 创建 GRU 层
gru = nn.GRU(
    input_size=100,
    hidden_size=256,
    num_layers=2,
    batch_first=True,
    dropout=0.2
)

# 输入输出
x = torch.randn(32, 50, 100)
output, h_n = gru(x)

print(f"输出形状：{output.shape}")  # [32, 50, 256]
print(f"隐藏状态：{h_n.shape}")     # [2, 32, 256]
```

---

## 第三部分：词嵌入

### 38.5 Embedding 层

#### 概念说明

Embedding 层将离散的词索引转换为连续的向量表示。

```
┌─────────────────────────────────────────────────────────────┐
│                  词嵌入（Word Embedding）                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   问题：                                                     │
│   • 词是离散的符号，无法直接输入神经网络                    │
│   • One-hot 编码：维度高、稀疏、无语义信息                  │
│                                                             │
│   解决方案：词嵌入                                          │
│   • 将每个词映射到低维连续向量                              │
│   • 语义相近的词向量也相近                                  │
│   • 可以学习得到或使用预训练（Word2Vec、GloVe）             │
│                                                             │
│   示例：                                                     │
│   "猫" → [0.2, -0.5, 0.8, ...]                             │
│   "狗" → [0.3, -0.4, 0.7, ...]  ← 与"猫"相近                │
│   "汽车" → [-0.8, 0.9, -0.2, ...] ← 与"猫"较远              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**PyTorch 实现：**

```python
import torch
import torch.nn as nn

# 创建 Embedding 层
embedding = nn.Embedding(
    num_embeddings=10000,   # 词汇表大小
    embedding_dim=300,      # 词向量维度
    padding_idx=0           # 填充标记的索引
)

# 输入：词索引序列
# [batch_size, sequence_length]
input_indices = torch.randint(1, 10000, (32, 50))  # 32 句，每句 50 词

# 输出：词向量序列
# [batch_size, sequence_length, embedding_dim]
embedded = embedding(input_indices)

print(f"输入形状：{input_indices.shape}")  # [32, 50]
print(f"输出形状：{embedded.shape}")       # [32, 50, 300]

# 使用预训练词向量（如 GloVe）
# pretrained_weights = load_glove_vectors()
# embedding = nn.Embedding.from_pretrained(pretrained_weights)
```

---

## 第四部分：应用实战

### 38.6 文本情感分析

#### 概念说明

使用 LSTM 进行电影评论情感分析（正面/负面）。

**完整实现：**

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class SentimentLSTM(nn.Module):
    """基于 LSTM 的情感分析模型"""

    def __init__(self, vocab_size, embedding_dim, hidden_dim, output_dim,
                 n_layers=2, bidirectional=True, dropout=0.5, pad_idx=0):
        super(SentimentLSTM, self).__init__()

        # Embedding 层
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=pad_idx)

        # LSTM 层
        self.lstm = nn.LSTM(
            embedding_dim,
            hidden_dim,
            num_layers=n_layers,
            bidirectional=bidirectional,
            dropout=dropout if n_layers > 1 else 0,
            batch_first=True
        )

        # 全连接层
        fc_dim = hidden_dim * 2 if bidirectional else hidden_dim
        self.fc = nn.Linear(fc_dim, output_dim)

        # Dropout
        self.dropout = nn.Dropout(dropout)

    def forward(self, text, text_lengths=None):
        # text: [batch_size, seq_len]

        # Embedding
        embedded = self.dropout(self.embedding(text))
        # [batch_size, seq_len, embedding_dim]

        # LSTM
        if text_lengths is not None:
            # 打包序列（处理变长）
            packed = nn.utils.rnn.pack_padded_sequence(
                embedded, text_lengths.cpu(),
                batch_first=True, enforce_sorted=False
            )
            packed_output, (hidden, cell) = self.lstm(packed)
            output, _ = nn.utils.rnn.pad_packed_sequence(packed_output, batch_first=True)
        else:
            output, (hidden, cell) = self.lstm(embedded)

        # hidden: [n_layers * n_directions, batch_size, hidden_dim]
        # 连接最后两层的双向隐藏状态
        if self.lstm.bidirectional:
            hidden = torch.cat((hidden[-2,:,:], hidden[-1,:,:]), dim=1)
        else:
            hidden = hidden[-1,:,:]

        # [batch_size, hidden_dim * 2]

        # Dropout + 全连接
        hidden = self.dropout(hidden)
        output = self.fc(hidden)

        return output


# 创建模型
vocab_size = 25000      # 词汇表大小
embedding_dim = 300     # 词向量维度
hidden_dim = 256        # 隐藏层维度
output_dim = 2          # 二分类
n_layers = 2
bidirectional = True

model = SentimentLSTM(vocab_size, embedding_dim, hidden_dim, output_dim,
                      n_layers, bidirectional)

print(model)
print(f"参数量：{sum(p.numel() for p in model.parameters()):,}")
```

**训练代码：**

```python
# 训练循环
def train_epoch(model, dataloader, optimizer, criterion, device):
    model.train()
    total_loss = 0
    total_acc = 0

    for batch in dataloader:
        text, text_lengths, labels = batch
        text = text.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()
        predictions = model(text, text_lengths)
        loss = criterion(predictions, labels)

        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        preds = predictions.argmax(dim=1)
        total_acc += (preds == labels).sum().item()

    return total_loss / len(dataloader), total_acc / len(dataloader.dataset)


# 使用示例
from torchtext.datasets import IMDB
from torchtext.data.utils import get_tokenizer
from torchtext.vocab import build_vocab_from_iterator

# 分词器
tokenizer = get_tokenizer("basic_english")

# 构建词汇表
def yield_tokens(data_iter):
    for text in data_iter:
        yield tokenizer(text[1])

train_iter = IMDB(split='train')
vocab = build_vocab_from_iterator(yield_tokens(train_iter), specials=["<pad>", "<unk>"])
vocab.set_default_index(vocab["<unk>"])

# 转换函数
def collate_batch(batch):
    labels = []
    texts = []
    lengths = []

    for label, text, _ in batch:
        labels.append(label)
        tokenized = tokenizer(text)
        lengths.append(len(tokenized))
        texts.append(torch.tensor(vocab(tokenized)))

    # 填充
    texts = nn.utils.rnn.pad_sequence(texts, batch_first=True, padding_value=0)
    return texts, torch.tensor(lengths), torch.tensor(labels)
```

---

## 本章小结

```
┌─────────────────────────────────────────────────────────────┐
│                      第 38 章 知识要点                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   RNN 基础：                                                  │
│   ✓ 适用场景：序列数据、时间依赖、上下文信息                │
│   ✓ 结构：循环连接、隐藏状态传递                            │
│   ✓ 问题：梯度消失/爆炸、长距离依赖困难                     │
│                                                             │
│   LSTM：                                                     │
│   ✓ 门控：遗忘门、输入门、输出门                            │
│   ✓ 细胞状态：长期记忆传递                                  │
│   ✓ 优势：学习长距离依赖                                    │
│                                                             │
│   GRU：                                                      │
│   ✓ 简化 LSTM：更新门、重置门                               │
│   ✓ 参数更少、训练更快                                      │
│   ✓ 性能与 LSTM 相当                                         │
│                                                             │
│   Embedding：                                                │
│   ✓ 词嵌入：离散索引→连续向量                               │
│   ✓ nn.Embedding：num_embeddings、embedding_dim             │
│   ✓ 预训练词向量：Word2Vec、GloVe                           │
│                                                             │
│   应用：                                                     │
│   ✓ 情感分析：LSTM+Embedding                                │
│   ✓ 变长序列：pack_padded_sequence                          │
│   ✓ 双向 LSTM：捕捉前后文                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```
---

[← 上一篇](./04-卷积神经网络CNN.md) | [下一篇 →](./06-深度学习实战.md)
