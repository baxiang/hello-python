# 09.01.02 - Prompt 与调用

**Prompt 模板：** 可复用的提示词模板，支持变量替换。

```
语法结构：
┌──────────────────────────────────────┐
│  PromptTemplate                       │
│                                       │
│  template="你好，{name}！"            │
│  input_variables=["name"]            │
└──────────────────────────────────────┘
```

### 最简示例

```python
from langchain.prompts import PromptTemplate

template = PromptTemplate(
    template="你好，{name}！请介绍 {topic}",
    input_variables=["name", "topic"],
)

prompt = template.invoke({"name": "小明", "topic": "Python"})
print(prompt.text)
```

### 详细示例：带格式的模板

```python
from langchain.prompts import PromptTemplate
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage

template = PromptTemplate(
    template="""
请用简洁的语言解释 {concept}。

要求：
1. 不超过 100 字
2. 给出一个代码示例
3. 适合初学者理解
""",
    input_variables=["concept"],
)

prompt = template.invoke({"concept": "列表推导式"})

model = init_chat_model("openai:gpt-4o-mini")
response = model.invoke([HumanMessage(prompt.text)])

print(response.content)
```

**关键代码说明：**

| 代码 | 含义 | 为什么这样写 |
|------|------|-------------|
| `template.invoke()` | 生成具体提示词 | 替换变量，生成最终文本 |
| `HumanMessage(prompt.text)` | 转为消息对象 | LLM 需要消息格式 |

---

### 消息格式

**三种消息格式：**

```
消息格式：
┌──────────────────────────────────────┐
│  消息对象    → HumanMessage(...)     │
│  字典格式    → {"role": "user", ...} │
│  字符串简写  → "直接文本"             │
└──────────────────────────────────────┘
```

#### 消息对象格式

```python
from langchain.messages import HumanMessage, AIMessage, SystemMessage

messages = [
    SystemMessage("你是一个 Python 老师"),
    HumanMessage("什么是列表？"),
    AIMessage("列表是 Python 中最常用的数据类型之一..."),
    HumanMessage("如何创建列表？"),
]

response = model.invoke(messages)
```

#### 字典格式（OpenAI 格式）

```python
messages = [
    {"role": "system", "content": "你是一个 Python 老师"},
    {"role": "user", "content": "什么是列表？"},
    {"role": "assistant", "content": "列表是 Python 中最常用的数据类型之一..."},
    {"role": "user", "content": "如何创建列表？"},
]

response = model.invoke(messages)
```

#### 字符串简写

```python
response = model.invoke("什么是 Python？")
```

**关键代码说明：**

| 格式 | 适用场景 | 为什么这样写 |
|------|----------|-------------|
| 消息对象 | 多轮对话、类型安全 | 明确区分角色，便于代码维护 |
| 字典格式 | 与 OpenAI API 兼容 | 直接对接外部系统 |
| 字符串简写 | 单次简单查询 | 代码简洁，快速原型 |

---

### 模型参数

**常用模型参数：**

```
模型参数：
┌──────────────────────────────────────┐
│  temperature    → 控制随机性 (0-2)    │
│  max_tokens     → 输出最大长度        │
│  timeout        → 请求超时时间        │
│  max_retries    → 重试次数            │
└──────────────────────────────────────┘
```

```python
from langchain.chat_models import init_chat_model

model = init_chat_model(
    "openai:gpt-4o-mini",
    temperature=0.7,
    max_tokens=1000,
    timeout=30,
    max_retries=6,
)
```

**关键代码说明：**

| 参数 | 含义 | 常用值 |
|------|------|--------|
| `temperature` | 辧出随机性，越高越创造性 | 0.7（创意）、0（确定性） |
| `max_tokens` | 辧出最大 token 数 | 根据任务调整 |
| `timeout` | 请求超时秒数 | 30-60 秒 |
| `max_retries` | 失败重试次数 | 6（默认），可增至 10-15 |

---

### 调用方式

**三种调用方式：**

```
调用方式：
┌──────────────────────────────────────┐
│  invoke   → 同步单次调用              │
│  stream   → 流式输出                  │
│  batch    → 批量调用                  │
└──────────────────────────────────────┘
```

#### invoke：同步调用

```python
from langchain.chat_models import init_chat_model

model = init_chat_model("openai:gpt-4o-mini")

response = model.invoke("你好")
print(response.content)
```

#### stream：流式输出

```python
from langchain.chat_models import init_chat_model

model = init_chat_model("openai:gpt-4o-mini")

for chunk in model.stream("请介绍 Python"):
    print(chunk.text, end="", flush=True)
```

**流式输出聚合为完整消息：**

```python
full = None
for chunk in model.stream("请介绍 Python"):
    full = chunk if full is None else full + chunk
    print(full.text)

print(full.content_blocks)
```

#### batch：批量调用

```python
from langchain.chat_models import init_chat_model

model = init_chat_model("openai:gpt-4o-mini")

responses = model.batch([
    "什么是变量？",
    "什么是函数？",
    "什么是类？",
])

for r in responses:
    print(r.content)
```

**批量调用并发控制：**

```python
responses = model.batch(
    ["问题1", "问题2", "问题3", "问题4", "问题5"],
    config={"max_concurrency": 3},
)
```

**关键代码说明：**

| 方法 | 含义 | 适用场景 |
|------|------|----------|
| `invoke` | 同步单次调用 | 简单查询 |
| `stream` | 流式逐字输出 | 长文本、实时展示 |
| `batch` | 批量并行调用 | 多个独立问题 |

---

### 流式处理内容块

**Content Blocks：** 标准化的内容格式，支持文本、推理、工具调用等。

```python
for chunk in model.stream("请解释量子计算"):
    for block in chunk.content_blocks:
        if block["type"] == "text":
            print(block["text"])
        elif block["type"] == "reasoning":
            print(f"[推理] {block.get('reasoning')}")
```

**常见 Content Block 类型：**

| 类型 | 含义 | 用途 |
|------|------|------|
| `text` | 文本内容 | 普通响应 |
| `reasoning` | 推理步骤 | 思维链模型 |
| `tool_call` | 工具调用 | Agent 调用工具 |
| `image` | 图片内容 | 多模态输出 |

---

### Token 使用统计

**AIMessage 包含 token 使用信息：**

```python
response = model.invoke("你好")
print(response.usage_metadata)

# 输出：
# {
#   'input_tokens': 8,
#   'output_tokens': 304,
#   'total_tokens': 312,
#   'input_token_details': {'audio': 0, 'cache_read': 0},
#   'output_token_details': {'audio': 0, 'reasoning': 256}
# }
```

---

### 为什么用它？

```python
import openai
import anthropic

openai.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "你好"}],
)

anthropic.messages.create(
    model="claude-3",
    messages=[{"role": "user", "content": "你好"}],
)

from langchain.chat_models import init_chat_model

model = init_chat_model("openai:gpt-4o-mini")
model.invoke("你好")

model = init_chat_model("anthropic:claude-3-sonnet")
model.invoke("你好")
```

**统一接口的优势：**

| 传统方式 | LangChain 方式 |
|----------|----------------|
| 每个 SDK 不同 API | 同一套接口 |
| 需学习各提供商文档 | 只需学习 LangChain |
| 切换模型需改代码 | 只改模型名称字符串 |