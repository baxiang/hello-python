# 09.03.03 - ReAct 循环

**ReAct：** Reasoning + Acting，Agent 的核心执行机制。

```
ReAct 循环：
┌──────────────────────────────────────┐
│  用户问题                             │
│    ↓                                  │
│  Thought: 思考需要什么工具             │
│    ↓                                  │
│  Action: 选择并调用工具                │
│    ↓                                  │
│  Observation: 工具返回结果             │
│    ↓                                  │
│  循环直到得出答案                      │
│    ↓                                  │
│  Final Answer: 最终回答               │
└──────────────────────────────────────┘
```

---

### 为什么理解 ReAct？

理解 ReAct 有助于：
- 调试 Agent 行为
- 优化工具选择
- 控制执行流程

---

### ReAct 执行流程

LangChain Agent 底层是 LangGraph，ReAct 循环通过图节点实现：

```
LangGraph 实现：
┌──────────────────────────────────────┐
│  START                                │
│    ↓                                  │
│  agent_node (LLM决策)                 │
│    ↓                                  │
│  should_continue? (判断是否调用工具)  │
│    ↓ (yes)                            │
│  tools_node (执行工具)                 │
│    ↓                                  │
│  agent_node (LLM继续)                 │
│    ↓ (no)                             │
│  END                                  │
└──────────────────────────────────────┘
```

**执行原理：**

| 步骤 | 说明 |
|------|------|
| agent_node | LLM 接收消息，决定是否调用工具 |
| should_continue | 检查是否有 tool_calls |
| tools_node | 执行所有工具调用，返回 ToolMessage |
| 循环 | 直到 LLM 不再调用工具 |

---

### 示例：追踪执行过程

```python
from langchain.agents import create_agent
from langchain.tools import tool

@tool
def add(a: int, b: int) -> int:
    """加法运算"""
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    """乘法运算"""
    return a * b

agent = create_agent(
    model="moonshot:moonshot-v1-8k",
    tools=[add, multiply],
)

for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "计算 (3 + 5) * 2"}]},
    stream_mode="updates",
):
    for step, data in chunk.items():
        print(f"步骤: {step}")
        if "messages" in data:
            msg = data["messages"][-1]
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                print(f"  工具调用: {msg.tool_calls}")
            else:
                content = msg.content[:50] if msg.content else ""
                print(f"  内容: {content}...")
```

---

### ReAct 循环详解

**完整示例：搜索耳机库存**

```
用户: Find the most popular wireless headphones and check stock

================================== Ai Message ==================================
Tool Calls:
  search_products (call_abc123)
  Args: query: wireless headphones

================================ Tool Message =================================
Found 5 products. Top result: WH-1000XM5

================================== Ai Message ==================================
Tool Calls:
  check_inventory (call_def456)
  Args: product_id: WH-1000XM5

================================ Tool Message =================================
Product WH-1000XM5: 10 units in stock

================================== Ai Message ==================================
I found wireless headphones (model WH-1000XM5) with 10 units in stock...
```

**循环过程：**

| 阶段 | 行为 | 说明 |
|------|------|------|
| Thought | 分析任务 | "需要先搜索热门产品" |
| Action | 调用工具 | `search_products("wireless headphones")` |
| Observation | 工具返回 | "WH-1000XM5" |
| Thought | 分析结果 | "需要确认库存" |
| Action | 调用工具 | `check_inventory("WH-1000XM5")` |
| Observation | 工具返回 | "10 units in stock" |
| Final Answer | 输出答案 | 完整回复 |

---

### 状态流转

Agent 执行过程中的状态变化：

```python
result = agent.invoke({
    "messages": [{"role": "user", "content": "北京天气？"}]
})

print("=== 执行历史 ===")
for msg in result["messages"]:
    role = msg.__class__.__name__.replace("Message", "")
    content = msg.content[:50] if msg.content else ""
    print(f"{role}: {content}...")
    if hasattr(msg, "tool_calls") and msg.tool_calls:
        print(f"  工具调用: {msg.tool_calls}")
```

---

### 流式追踪 ReAct

```python
from langchain.messages import AIMessage, HumanMessage

for chunk in agent.stream({
    "messages": [{"role": "user", "content": "搜索 AI 新闻并总结"}]
}, stream_mode="values"):
    latest_message = chunk["messages"][-1]
    if latest_message.content:
        if isinstance(latest_message, HumanMessage):
            print(f"用户: {latest_message.content}")
        elif isinstance(latest_message, AIMessage):
            print(f"Agent: {latest_message.content}")
    elif latest_message.tool_calls:
        print(f"调用工具: {[tc['name'] for tc in latest_message.tool_calls]}")
```

---

### 控制循环次数

**Recursion Limit：** 防止 Agent 无限循环。

```python
agent = create_agent(
    model="moonshot:moonshot-v1-8k",
    tools=[get_weather],
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "复杂问题"}]},
    config={"recursion_limit": 5},
)
```

**默认限制：** 1000 步。超过限制抛出 `GraphRecursionError`。

---

### 并行工具调用

Agent 支持一次调用多个工具：

```python
@tool
def get_weather(location: str) -> str:
    """获取天气"""
    return f"{location}: sunny"

agent = create_agent(
    model="moonshot:moonshot-v1-8k",
    tools=[get_weather],
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "北京和上海的天气"}]
})

# 可能产生两个并行工具调用：
# get_weather("北京")
# get_weather("上海")
```

---

### 工具错误处理

**自定义错误处理：**

```python
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage

@wrap_tool_call
def handle_tool_errors(request, handler):
    try:
        return handler(request)
    except Exception as e:
        return ToolMessage(
            content=f"工具错误: 请检查输入后重试。({str(e)})",
            tool_call_id=request.tool_call["id"],
        )

agent = create_agent(
    model="moonshot:moonshot-v1-8k",
    tools=[search, get_weather],
    middleware=[handle_tool_errors],
)
```

---

### 中断循环

**何时停止：**

| 条件 | 说明 |
|------|------|
| 无 tool_calls | LLM 返回最终答案 |
| recursion_limit | 达到最大步数 |
| interrupt | 人工审核中断 |

---

### ReAct vs 直接调用

| 方式 | 优点 | 适用场景 |
|------|------|----------|
| 直接调用 LLM | 简单快速 | 单次问答 |
| ReAct Agent | 多步推理 | 需要工具的任务 |

```python
# 直接调用 - 无工具循环
model.invoke("什么是 Python？")

# ReAct Agent - 循环调用工具
agent.invoke({"messages": [{"role": "user", "content": "搜索最新新闻"}]})
```

---

### ReAct 总结

| 要点 | 说明 |
|------|------|
| 核心机制 | Thought → Action → Observation 循环 |
| 底层实现 | LangGraph 图节点 + 条件边 |
| 流式追踪 | stream() 实时监控执行步骤 |
| 循环控制 | recursion_limit 防止无限循环 |
| 并行执行 | 多个工具可同时调用 |
| 错误处理 | middleware 自定义错误响应 |