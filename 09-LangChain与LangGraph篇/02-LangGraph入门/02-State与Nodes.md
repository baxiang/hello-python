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

---

### 最简示例：定义 State

```python
from typing import TypedDict

class State(TypedDict):
    messages: list[str]
    count: int
```

---

### Reducer：更新策略

**Reducer：** 定义节点返回值如何更新 State。

```
Reducer 类型：
┌──────────────────────────────────────┐
│  默认 Reducer   → 覆盖更新            │
│  operator.add   → 列表追加            │
│  add_messages   → 消息追加（ID追踪）  │
└──────────────────────────────────────┘
```

#### 默认 Reducer（覆盖）

```python
from typing import TypedDict

class State(TypedDict):
    count: int
    result: str

# 输入: {"count": 1, "result": "hi"}
# 节点返回: {"count": 2}
# 结果: {"count": 2, "result": "hi"}  ← count 被覆盖

# 节点返回: {"result": "bye"}
# 结果: {"count": 2, "result": "bye"}  ← result 被覆盖
```

#### operator.add（列表追加）

```python
from typing import Annotated, TypedDict
from operator import add

class State(TypedDict):
    items: Annotated[list[str], add]

# 输入: {"items": ["a"]}
# 节点返回: {"items": ["b"]}
# 结果: {"items": ["a", "b"]}  ← 列表追加而非覆盖
```

**关键代码说明：**

| 代码 | 含义 | 为什么这样写 |
|------|------|-------------|
| `Annotated[list[str], add]` | 带 Reducer 的类型 | 使用 operator.add 追加列表 |
| `int` 或 `str` | 默认 Reducer | 无 Reducer 时，返回值直接覆盖 |

---

### add_messages：消息处理

**add_messages：** 专门处理消息列表的 Reducer，支持 ID 追踪。

```python
from typing import Annotated
from langchain.messages import AnyMessage
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
```

**add_messages 的优势：**

| 功能 | 说明 |
|------|------|
| ID 追踪 | 新消息追加，相同 ID 的消息会覆盖 |
| 自动反序列化 | 支持字典格式消息自动转为 Message 对象 |

```python
# 支持两种格式
{"messages": [HumanMessage(content="hi")]}
{"messages": [{"type": "human", "content": "hi"}]}
```

---

### MessagesState

LangGraph 提供预置的 `MessagesState`，适合对话场景：

```python
from langgraph.graph import MessagesState

class State(MessagesState):
    documents: list[str]

# MessagesState 已包含:
# messages: Annotated[list[AnyMessage], add_messages]
```

---

### 多 Schema 支持

**三种 Schema：** 输入、输出、内部状态。

```python
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class InputState(TypedDict):
    user_input: str

class OutputState(TypedDict):
    graph_output: str

class OverallState(TypedDict):
    foo: str
    user_input: str
    graph_output: str

class PrivateState(TypedDict):
    bar: str

def node_1(state: InputState) -> OverallState:
    return {"foo": state["user_input"] + " name"}

def node_2(state: OverallState) -> PrivateState:
    return {"bar": state["foo"] + " is"}

def node_3(state: PrivateState) -> OutputState:
    return {"graph_output": state["bar"] + " Lance"}

builder = StateGraph(
    OverallState,
    input_schema=InputState,
    output_schema=OutputState,
)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)
builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")
builder.add_edge("node_2", "node_3")
builder.add_edge("node_3", END)

graph = builder.compile()
graph.invoke({"user_input": "My"})
# {'graph_output': 'My name is Lance'}
```

**关键代码说明：**

| Schema | 用途 | 说明 |
|------|------|------|
| `InputState` | 约束输入 | 用户传入的数据结构 |
| `OutputState` | 约束输出 | 返回给用户的数据结构 |
| `OverallState` | 内部状态 | 图内所有节点共享的状态 |
| `PrivateState` | 私有状态 | 仅特定节点间传递 |

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

#### 最简示例：节点函数

```python
def increment_node(state: State) -> dict:
    new_count = state["count"] + 1
    return {"count": new_count}
```

#### 带 Runtime 的节点

```python
from dataclasses import dataclass
from langgraph.runtime import Runtime

@dataclass
class Context:
    user_id: str

def node_with_runtime(state: State, runtime: Runtime[Context]):
    user_id = runtime.context.user_id
    return {"result": f"Hello, {user_id}!"}
```

#### 带 config 的节点

```python
from langchain_core.runnables import RunnableConfig

def node_with_config(state: State, config: RunnableConfig) -> dict:
    thread_id = config["configurable"]["thread_id"]
    current_step = config["metadata"]["langgraph_step"]
    return {"messages": [f"Thread: {thread_id}, Step: {current_step}"]}
```

**Runtime 可访问的对象：**

| 属性 | 用途 | 说明 |
|------|------|------|
| `runtime.context` | 运行时上下文 | 自定义配置信息 |
| `runtime.store` | 跨线程存储 | 长期记忆 |
| `runtime.stream_writer` | 流式输出 | 实时推送数据 |
| `runtime.execution_info` | 执行信息 | thread_id 等 |

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

---

### 节点缓存

**CachePolicy：** 为节点启用缓存，避免重复计算。

```python
from langgraph.cache.memory import InMemoryCache
from langgraph.types import CachePolicy

def expensive_node(state: State) -> dict:
    time.sleep(2)
    return {"result": state["x"] * 2}

builder.add_node("expensive_node", expensive_node, cache_policy=CachePolicy(ttl=3))
builder.set_entry_point("expensive_node")

graph = builder.compile(cache=InMemoryCache())

graph.invoke({"x": 5})  # 第一次执行，耗时 2 秒
graph.invoke({"x": 5})  # 第二次执行，命中缓存，瞬间返回
```

**关键代码说明：**

| 参数 | 含义 | 常用值 |
|------|------|--------|
| `CachePolicy(ttl=3)` | 缓存有效期 | 秒数，None 表示永不过期 |
| `InMemoryCache()` | 内存缓存 | 适合开发测试 |

---

### 图执行原理

**Super-step：** 图执行的离散迭代单位。

```
执行流程：
┌──────────────────────────────────────┐
│  节点状态：inactive / active          │
│                                       │
│  1. 收到消息 → active                 │
│  2. 执行函数 → 发送更新               │
│  3. 无新消息 → halt → inactive        │
│  4. 全部 inactive → 图终止            │
└──────────────────────────────────────┘
```

**并行节点属于同一 super-step，串行节点属于不同 super-step。**

---

### Recursion Limit

**递归限制：** 最大执行步数，防止无限循环。

```python
graph.invoke(inputs, config={"recursion_limit": 10})
```

**默认限制：1000 步。超过限制会抛出 `GraphRecursionError`。**

#### RemainingSteps：剩余步数追踪

```python
from langgraph.managed import RemainingSteps

class State(TypedDict):
    messages: list[str]
    remaining_steps: RemainingSteps

def check_node(state: State) -> dict:
    if state["remaining_steps"] <= 2:
        return {"messages": ["即将达到限制，返回结果"]}
    return {"messages": ["继续处理..."]}
```

---

### 为什么用 TypedDict？

| 方式 | 优点 | 缺点 |
|------|------|------|
| TypedDict | 性能好，简单 | 无运行时验证 |
| Pydantic | 自动验证，嵌套支持 | 性能较低 |
| dataclass | 支持默认值 | 需要额外导入 |