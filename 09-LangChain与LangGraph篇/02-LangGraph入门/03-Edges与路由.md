# 09.02.03 - Edges 与路由

**Edges：** 定义节点间的执行顺序和控制流。

```
Edges 类型：
┌──────────────────────────────────────┐
│  Normal Edge      → 固定顺序         │
│  Conditional Edge → 动态路由         │
│  START/END Edge   → 入口/终点        │
└──────────────────────────────────────┘
```

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

### 最简示例：条件路由

```python
from typing import Literal

def route_decision(state: State) -> Literal["node_b", "node_c"]:
    if state["count"] > 5:
        return "node_b"
    return "node_c"

builder.add_conditional_edges("node_a", route_decision)
```

### 详细示例：完整条件路由

```python
from typing import Literal, TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    value: int
    result: str

def check_node(state: State) -> dict:
    return state  # 不修改，只检查

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

---

### Command：状态更新 + 路由

**Command：** 在一个函数中同时更新 State 和控制路由。

```
Command：
┌──────────────────────────────────────┐
│  Command(                            │
│      update={"key": value},  # 更新  │
│      goto="next_node"        # 路由  │
│  )                                   │
└──────────────────────────────────────┘
```

### 最简示例：Command

```python
from langgraph.types import Command
from typing import Literal

def smart_node(state: State) -> Command[Literal["node_b", "node_c"]]:
    if state["value"] > 10:
        return Command(
            update={"result": "high"},
            goto="node_b"
        )
    return Command(
        update={"result": "low"},
        goto="node_c"
    )
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

---

### 多出口并行执行

节点可以有多个出口边，所有目的地**并行执行**：

```python
builder.add_edge("node_a", "node_b")
builder.add_edge("node_a", "node_c")

# node_a 执行完后，node_b 和 node_c 并行执行
```