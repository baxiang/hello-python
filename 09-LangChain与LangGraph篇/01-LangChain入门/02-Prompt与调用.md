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

# 第一步：创建模板
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

# 第二步：生成提示词
prompt = template.invoke({"concept": "列表推导式"})

# 第三步：调用模型
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

### invoke：同步调用

```python
from langchain.chat_models import init_chat_model

model = init_chat_model("openai:gpt-4o-mini")

response = model.invoke("你好")
print(response.content)
```

### stream：流式输出

```python
from langchain.chat_models import init_chat_model

model = init_chat_model("openai:gpt-4o-mini")

for chunk in model.stream("请介绍 Python"):
    print(chunk.content, end="", flush=True)
```

### batch：批量调用

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

**关键代码说明：**

| 方法 | 含义 | 适用场景 |
|------|------|----------|
| `invoke` | 同步单次调用 | 简单查询 |
| `stream` | 流式逐字输出 | 长文本、实时展示 |
| `batch` | 批量并行调用 | 多个独立问题 |