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
    model="openai:gpt-4o-mini",
    tools=[add, multiply],
)

# 流式追踪执行
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "计算 (3 + 5) * 2"}]},
    stream_mode="updates",
):
    for step, data in chunk.items():
        print(f"步骤: {step}")
        if "messages" in data:
            msg = data["messages"][-1]
            if hasattr(msg, "tool_calls"):
                print(f"  工具调用: {msg.tool_calls}")
            else:
                print(f"  内容: {msg.content[:50]}...")
```

---

### 状态流转

Agent 执行过程中的状态变化：

```python
# 查看完整状态
result = agent.invoke({
    "messages": [{"role": "user", "content": "北京天气？"}]
})

print("=== 执行历史 ===")
for msg in result["messages"]:
    role = msg.__class__.__name__.replace("Message", "")
    print(f"{role}: {msg.content[:50]}...")
    if hasattr(msg, "tool_calls"):
        print(f"  工具调用: {msg.tool_calls}")
```

---

### 控制循环次数

防止 Agent 无限循环：

```python
agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[get_weather],
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "复杂问题"}]},
    config={"recursion_limit": 5}  # 最多 5 次循环
)
```