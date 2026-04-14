# 09.06.01 - 多 Agent 协作

**多 Agent 协作：** 多个 Agent 共同完成任务，通过 Subagents、Handoffs、Skills、Router 等模式实现。

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
│  Subagents → Agent作为工具调用        │
└──────────────────────────────────────┘
```

### 为什么用多 Agent？

- 上下文管理：避免单一 Agent 上下文过大
- 分布式开发：不同团队维护不同能力
- 并行执行：多个 Agent 同时处理子任务

---

### 四种模式对比

| 模式 | 工作方式 | 分布式开发 | 并行执行 | 多跳 | 直接交互 |
|------|----------|-----------|---------|------|---------|
| Subagents | 主 Agent 调用子 Agent 作为工具 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ |
| Handoffs | Agent 通过工具调用传递控制 | - | - | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Skills | 按需加载专业知识和 Prompt | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Router | 路由步骤分类输入分发给 Agent | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | - | ⭐⭐⭐ |

---

### Subagents：子 Agent 作为工具

**主 Agent 协调子 Agent，所有路由通过主 Agent：**

```python
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """获取天气"""
    return f"{city}: sunny"

weather_agent = create_agent(
    model="moonshot:moonshot-v1-8k",
    tools=[get_weather],
    name="weather_agent",
)

def call_weather_agent(query: str) -> str:
    """调用天气 Agent"""
    result = weather_agent.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].text

supervisor = create_agent(
    model="moonshot:moonshot-v1-8k",
    tools=[call_weather_agent],
    name="supervisor",
)
```

**优点：**
- 上下文隔离：每个子 Agent 只看相关内容
- 并行执行：可同时调用多个子 Agent
- 团队独立：各子 Agent 可独立开发

---

### Handoffs：任务传递

**Agent 通过工具调用传递控制权：**

```python
from langchain.agents import create_agent
from langchain.tools import tool

@tool
def handoff_to_research(query: str) -> str:
    """传递给研究 Agent"""
    return "handoff:research_agent"

@tool
def handoff_to_writer(content: str) -> str:
    """传递给写作 Agent"""
    return "handoff:writer_agent"

research_agent = create_agent(
    model="moonshot:moonshot-v1-8k",
    tools=[handoff_to_writer],
    name="research_agent",
)

writer_agent = create_agent(
    model="moonshot:moonshot-v1-8k",
    tools=[],
    name="writer_agent",
)

supervisor = create_agent(
    model="moonshot:moonshot-v1-8k",
    tools=[handoff_to_research, handoff_to_writer],
    name="supervisor",
)
```

**优点：**
- 直接用户交互：子 Agent 可直接回复用户
- 状态持久：Agent 间保持对话上下文
- 重复请求高效：跳过传递步骤

---

### Skills：按需加载知识

**单个 Agent 动态加载专业 Prompt：**

```python
from langchain.tools import tool

@tool
def load_python_skill() -> str:
    """加载 Python 专业知识"""
    return """
    你是 Python 专家。以下是你需要知道的：
    - Python 3.11+ 的新特性
    - 最佳实践指南
    - 常见错误和解决方案
    """

@tool
def load_js_skill() -> str:
    """加载 JavaScript 专业知识"""
    return """
    你是 JavaScript 专家...
    """

agent = create_agent(
    model="moonshot:moonshot-v1-8k",
    tools=[load_python_skill, load_js_skill],
)
```

**优点：**
- 按需加载：只加载相关知识
- 单 Agent 控制：保持一致性
- 重复请求高效：知识已加载

---

### Router：路由分发

**路由步骤分类输入，分发给专业 Agent：**

```python
from langchain.agents import create_agent

python_agent = create_agent(
    model="moonshot:moonshot-v1-8k",
    tools=[python_tools],
    name="python_agent",
)

js_agent = create_agent(
    model="moonshot:moonshot-v1-8k",
    tools=[js_tools],
    name="js_agent",
)

def route_query(query: str) -> str:
    """路由查询"""
    if "Python" in query:
        return python_agent.invoke({"messages": [{"role": "user", "content": query}]})
    elif "JavaScript" in query:
        return js_agent.invoke({"messages": [{"role": "user", "content": query}]})
    return "无法识别"

router_agent = create_agent(
    model="moonshot:moonshot-v1-8k",
    tools=[route_query],
)
```

**优点：**
- 并行执行：可同时调用多个 Agent
- 结果合成：综合多个专业 Agent 输出

---

### 性能对比

**单次请求：**

| 模式 | 模型调用次数 |
|------|------------|
| Subagents | 4 |
| Handoffs | 3 |
| Skills | 3 |
| Router | 3 |

**重复请求（相同任务）：**

| 模式 | 第2次调用 | 总计 |
|------|----------|------|
| Subagents | 4 | 8 |
| Handoffs | 2 | 5 |
| Skills | 2 | 5 |
| Router | 3 | 6 |

**多领域任务：**

| 模式 | 调用次数 | Token 使用 |
|------|----------|-----------|
| Subagents | 5 | ~9K |
| Handoffs | 7+ | ~14K+ |
| Skills | 3 | ~15K |
| Router | 5 | ~9K |

---

### 选择模式

| 优化目标 | Subagents | Handoffs | Skills | Router |
|----------|-----------|---------|--------|--------|
| 单次请求 | | ✅ | ✅ | ✅ |
| 重复请求 | | ✅ | ✅ | |
| 并行执行 | ✅ | | | ✅ |
| 大上下文领域 | ✅ | | | ✅ |
| 简单任务 | | | ✅ | |

---

### Custom Workflow：自定义工作流

**使用 LangGraph 构建自定义流程：**

```python
from typing import Literal, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command

class State(TypedDict):
    task: str
    result: str

def supervisor(state: State) -> Command[Literal["search_agent", "calc_agent", END]]:
    if "搜索" in state["task"]:
        return Command(goto="search_agent")
    elif "计算" in state["task"]:
        return Command(goto="calc_agent")
    return Command(goto=END)

def search_agent(state: State) -> dict:
    return {"result": "搜索结果"}

def calc_agent(state: State) -> dict:
    return {"result": "计算结果"}

builder = StateGraph(State)
builder.add_node("supervisor", supervisor)
builder.add_node("search_agent", search_agent)
builder.add_node("calc_agent", calc_agent)

builder.add_edge(START, "supervisor")
builder.add_edge("search_agent", END)
builder.add_edge("calc_agent", END)

graph = builder.compile()
```

---

### 模式组合

**可以混合使用多种模式：**

```python
# Subagents 可调用 Router 作为工具
# Router 可使用 Skills 加载上下文
# Handoffs 可嵌入 Custom Workflow
```

---

### 子图流式输出

**识别子 Agent 输出来源：**

```python
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "..."}]},
    stream_mode=["messages", "updates"],
    subgraphs=True,
    version="v2",
):
    if chunk["type"] == "messages":
        token, metadata = chunk["data"]
        if agent_name := metadata.get("lc_agent_name"):
            print(f"🤖 {agent_name}: {token.text}")
```

---

### 多 Agent 总结

| 要点 | 说明 |
|------|------|
| Subagents | 子 Agent 作为工具，上下文隔离 |
| Handoffs | Agent 间传递控制，直接交互 |
| Skills | 按需加载专业知识 |
| Router | 路由分发，并行执行 |
| 选择依据 | 考虑并行性、上下文大小、交互方式 |