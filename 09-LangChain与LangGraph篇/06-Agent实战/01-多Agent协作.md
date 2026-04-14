# 09.06.01 - 多 Agent 协作

**多 Agent 协作：** 多个 Agent 共同完成任务，通过 Subgraph 和 Handoffs 实现。

```
多 Agent 结构：
┌──────────────────────────────────────┐
│  主图 (Supervisor)                     │
│                                       │
│  ┌─────┐  ┌─────┐  ┌─────┐           │
│  │Agent│  │Agent│  │Agent│           │
│  │ A   │  │ B   │  │ C   │           │
│  └─────┘  └─────┘  └─────┘           │
│                                       │
│  Handoffs → Agent间任务传递           │
└──────────────────────────────────────┘
```

### Subgraph：子图

将复杂工作流拆分为独立模块：

```python
from langgraph.graph import StateGraph, START, END

# 子图：单个 Agent 的工作流
def create_agent_subgraph():
    builder = StateGraph(AgentState)
    builder.add_node("think", think_node)
    builder.add_node("act", act_node)
    builder.add_edge(START, "think")
    builder.add_edge("think", "act")
    builder.add_edge("act", END)
    return builder.compile()
```

---

### Handoffs：任务传递

Agent 间传递任务：

```python
from langgraph.types import Command

def agent_a(state: State) -> Command:
    if state["task"].startswith("搜索"):
        return Command(goto="agent_b")
    return Command(goto="agent_c")
```

---

### 并行执行

多个 Agent 同时执行：

```python
builder.add_edge("supervisor", "agent_a")
builder.add_edge("supervisor", "agent_b")

# agent_a 和 agent_b 并行执行
```

---

### 详细示例：Supervisor 模式

```python
from typing import Literal, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command

class State(TypedDict):
    task: str
    result: str
    next_agent: str

def supervisor(state: State) -> Command:
    if "搜索" in state["task"]:
        return Command(goto="search_agent")
    elif "计算" in state["task"]:
        return Command(goto="calc_agent")
    return Command(goto=END)

def search_agent(state: State) -> dict:
    return {"result": "搜索结果", "next_agent": "done"}

def calc_agent(state: State) -> dict:
    return {"result": "计算结果", "next_agent": "done"}

builder = StateGraph(State)
builder.add_node("supervisor", supervisor)
builder.add_node("search_agent", search_agent)
builder.add_node("calc_agent", calc_agent)

builder.add_edge(START, "supervisor")
builder.add_edge("search_agent", END)
builder.add_edge("calc_agent", END)

graph = builder.compile()
```