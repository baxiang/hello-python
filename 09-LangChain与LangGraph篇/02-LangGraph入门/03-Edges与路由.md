# 09.02.03 - Edges 与路由

**Edges：** 定义节点间的执行顺序和控制流。

```
Edges 类型：
┌──────────────────────────────────────┐
│  Normal Edge      → 固定顺序         │
│  Conditional Edge → 动态路由         │
│  START/END Edge   → 入口/终点        │
│  Command          → 状态更新 + 路由  │
│  Send             → Map-Reduce       │
└──────────────────────────────────────┘
```

---

### Normal Edge：固定顺序

```python
builder.add_edge("node_a", "node_b")
```

**含义：** node_a 执行完后，一定执行 node_b。

---

### Conditional Edge：动态路由

**add_conditional_edges：** 根据条件选择下一个节点。

```
条件路由：
┌──────────────────────────────────────┐
│  add_conditional_edges(              │
│      "node_a",                       │
│      routing_function,               │
│      {True: "node_b",                │
│       False: "node_c"}               │
│  )                                   │
└──────────────────────────────────────┘
```

#### 最简示例：条件路由

```python
from typing import Literal

def route_decision(state: State) -> Literal["node_b", "node_c"]:
    if state["count"] > 5:
        return "node_b"
    return "node_c"

builder.add_conditional_edges("node_a", route_decision)
```

#### 详细示例：完整条件路由

```python
from typing import Literal, TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    value: int
    result: str

def check_node(state: State) -> dict:
    return state

def route(state: State) -> Literal["high", "low"]:
    if state["value"] > 10:
        return "high"
    return "low"

def high_node(state: State) -> dict:
    return {"result": "high value"}

def low_node(state: State) -> dict:
    return {"result": "low value"}

builder = StateGraph(State)
builder.add_node("check", check_node)
builder.add_node("high", high_node)
builder.add_node("low", low_node)

builder.add_edge(START, "check")
builder.add_conditional_edges("check", route)
builder.add_edge("high", END)
builder.add_edge("low", END)

graph = builder.compile()
result = graph.invoke({"value": 15, "result": ""})
print(result["result"])
```

#### 带 mapping 的条件路由

```python
def route(state: State) -> bool:
    return state["value"] > 10

builder.add_conditional_edges(
    "check",
    route,
    {True: "high", False: "low"},
)
```

---

### Command：状态更新 + 路由

**Command：** 在一个函数中同时更新 State 和控制路由。

```
Command：
┌──────────────────────────────────────┐
│  Command(                            │
│      update={"key": value},  # 更新  │
│      goto="next_node"        # 资源  │
│  )                                   │
└──────────────────────────────────────┘
```

#### 最简示例：Command

```python
from langgraph.types import Command
from typing import Literal

def smart_node(state: State) -> Command[Literal["node_b", "node_c"]]:
    if state["value"] > 10:
        return Command(
            update={"result": "high"},
            goto="node_b",
        )
    return Command(
        update={"result": "low"},
        goto="node_c",
    )
```

**关键代码说明：**

| 参数 | 含义 | 必需 |
|------|------|------|
| `update` | State 更新 | 可选 |
| `goto` | 下一个节点 | 可选 |
| `graph` | 目标图（父图） | 用于子图 |
| `resume` | 中断恢复值 | 用于 interrupt |

#### Command vs Conditional Edge

| 方式 | 优点 | 适用场景 |
|------|------|----------|
| Conditional Edge | 分离逻辑清晰 | 只路由不更新 |
| Command | 合并更新和路由 | 需同时更新状态和路由 |

**注意：** 使用 Command 时，必须添加返回类型注解：
```python
def node(state: State) -> Command[Literal["next_node"]]:
    ...
```

---

### Send：Map-Reduce

**Send：** 动态创建多个并行执行分支。

```python
from langgraph.types import Send

def continue_to_items(state: State):
    return [
        Send("process_item", {"item": item})
        for item in state["items"]
    ]

builder.add_conditional_edges("generate_items", continue_to_items)
```

#### 完整 Map-Reduce 示例

```python
from typing import Annotated, TypedDict
from operator import add
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send

class State(TypedDict):
    subjects: list[str]
    jokes: Annotated[list[str], add]

def generate_subjects(state: State) -> dict:
    return {"subjects": ["cat", "dog", "bird"]}

def generate_joke(state: dict) -> dict:
    subject = state["subject"]
    return {"jokes": [f"Why did the {subject} cross the road?"]}

def continue_to_jokes(state: State):
    return [Send("generate_joke", {"subject": s}) for s in state["subjects"]]

builder = StateGraph(State)
builder.add_node("generate_subjects", generate_subjects)
builder.add_node("generate_joke", generate_joke)

builder.add_edge(START, "generate_subjects")
builder.add_conditional_edges("generate_subjects", continue_to_jokes)
builder.add_edge("generate_joke", END)

graph = builder.compile()
result = graph.invoke({})
print(result["jokes"])
```

---

### 多出口并行执行

节点可以有多个出口边，所有目的地**并行执行**：

```python
builder.add_edge("node_a", "node_b")
builder.add_edge("node_a", "node_c")

# node_a 执行完后，node_b 和 node_c 并行执行（同一 super-step）
```

---

### Entry Point：入口点

**START Edge：** 定义图的入口节点。

```python
from langgraph.graph import START

builder.add_edge(START, "first_node")
```

### Conditional Entry Point

**条件入口：** 根据输入决定第一个执行的节点。

```python
from langgraph.graph import START

def route_entry(state: State) -> Literal["node_a", "node_b"]:
    if state["type"] == "query":
        return "node_a"
    return "node_b"

builder.add_conditional_edges(START, route_entry)
```

---

### 子图路由到父图

**Command.PARENT：** 从子图导航到父图节点。

```python
from langgraph.types import Command

def subgraph_node(state: State) -> Command[Literal["other_node"]]:
    return Command(
        update={"result": "done"},
        goto="other_node",  # other_node 在父图中
        graph=Command.PARENT,
    )
```

---

### Interrupt 恢复

**Command(resume)：** 提供值恢复中断执行。

```python
from langgraph.types import Command, interrupt

def review_node(state: State):
    answer = interrupt("Do you approve?")
    return {"approved": answer == "yes"}

# 第一次调用 - 中断等待
graph.invoke({"messages": [...]}, config)

# 恢复执行
graph.invoke(Command(resume="yes"), config)
```

---

### Edges 总结

| Edge 类型 | 用途 | 示例 |
|------|------|------|
| Normal | 固定顺序 | `add_edge("a", "b")` |
| Conditional | 动态路由 | `add_conditional_edges("a", route)` |
| START Edge | 入口定义 | `add_edge(START, "first")` |
| Command | 更新 + 路由 | `Command(update={...}, goto="...")` |
| Send | Map-Reduce | `Send("node", {"item": x})` |

---

### 为什么用 Command？

```python
# 方式一：Conditional Edge（分离逻辑）
def route(state):
    return "node_b" if state["value"] > 10 else "node_c"

def update_node(state):
    return {"result": "processed"}

builder.add_conditional_edges("node_a", route)
builder.add_node("update", update_node)

# 方式二：Command（合并逻辑）
def smart_node(state) -> Command[Literal["node_b", "node_c"]]:
    if state["value"] > 10:
        return Command(update={"result": "high"}, goto="node_b")
    return Command(update={"result": "low"}, goto="node_c")

builder.add_node("smart", smart_node)
```

**Command 适合：** 路由逻辑和状态更新紧密耦合的场景。