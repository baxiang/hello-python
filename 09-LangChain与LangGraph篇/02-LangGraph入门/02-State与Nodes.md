# 09.02.02 - State 与 Nodes

**State：** 图中所有节点共享的数据结构，承载整个工作流的上下文。

```
State 结构：
┌──────────────────────────────────────┐
│  TypedDict                            │
│                                       │
│  class State(TypedDict):              │
│      messages: list[str]              │
│      count: int                       │
│                                       │
│  Reducer ← 定义更新策略               │
└──────────────────────────────────────┘
```

### 最简示例：定义 State

```python
from typing import TypedDict

class State(TypedDict):
    messages: list[str]
    count: int
```

### Reducer：更新策略

**Reducer：** 定义节点返回值如何更新 State。

```
Reducer 类型：
┌──────────────────────────────────────┐
│  默认 Reducer → 覆盖更新              │
│  operator.add  → 列表追加             │
│  add_messages → 消息追加（ID追踪）    │
└──────────────────────────────────────┘
```

### 详细示例：带 Reducer 的 State

```python
from typing import Annotated, TypedDict
from operator import add

class State(TypedDict):
    messages: Annotated[list[str], add]  # 追加而非覆盖
    count: int  # 默认：覆盖更新
```

**关键代码说明：**

| 代码 | 含义 | 为什么这样写 |
|------|------|-------------|
| `Annotated[list[str], add]` | 带Reducer的类型 | 使用 operator.add 追加列表 |
| `int` | 默认Reducer | 无Reducer时，返回值直接覆盖 |

---

### MessagesState

LangGraph 提供预置的 `MessagesState`，适合对话场景：

```python
from langgraph.graph import MessagesState

class State(MessagesState):
    documents: list[str]  # 扩展额外字段
```

---

### Nodes：节点函数

**节点函数：** 接收 State，执行逻辑，返回更新。

```
节点函数签名：
┌──────────────────────────────────────┐
│  def node(state: State) -> dict:     │
│      # 读取 state                     │
│      # 执行逻辑                       │
│      # 返回更新                       │
│      return {"key": new_value}       │
└──────────────────────────────────────┘
```

### 最简示例：节点函数

```python
def increment_node(state: State) -> dict:
    new_count = state["count"] + 1
    return {"count": new_count}
```

### 详细示例：访问 config

节点可以访问 runtime config：

```python
from langchain_core.runnables import RunnableConfig

def node_with_config(state: State, config: RunnableConfig) -> dict:
    thread_id = config["configurable"]["thread_id"]
    return {"messages": [f"Thread: {thread_id}"]}
```

---

### START 和 END

```
特殊节点：
┌──────────────────────────────────────┐
│  START → 图入口，用户输入起点         │
│  END   → 图终点，执行结束             │
└──────────────────────────────────────┘
```

```python
from langgraph.graph import START, END

builder.add_edge(START, "first_node")
builder.add_edge("last_node", END)
```