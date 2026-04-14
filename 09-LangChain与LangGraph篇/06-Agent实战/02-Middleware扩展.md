# 09.06.02 - Middleware 扩展

**Middleware：** 拦截和增强 Agent 行为的机制。

```
Middleware：
┌──────────────────────────────────────┐
│  @wrap_model_call → 包装模型调用      │
│  @wrap_tool_call  → 包装工具调用      │
│                                       │
│  Guardrails → 输入/输出验证           │
│  HumanInTheLoop → 人工审核            │
└──────────────────────────────────────┘
```

### Guardrails：安全护栏

验证输入和输出：

```python
from langchain.agents.middleware import before_agent

@before_agent
def input_guardrail(state, runtime):
    user_input = state["messages"][-1].content
    
    if "敏感词" in user_input:
        return {"messages": ["输入包含敏感内容"]}
    
    return None  # 继续
```

---

### HumanInTheLoopMiddleware

自动审核工具调用：

```python
from langchain.agents.middleware import HumanInTheLoopMiddleware

agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[send_email, delete_file],
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={"send_email": True, "delete_file": True}
        ),
    ],
    checkpointer=checkpointer,
)
```

---

### @wrap_model_call

包装模型调用：

```python
from langchain.agents.middleware import wrap_model_call

@wrap_model_call
def log_model_call(state, runtime, call):
    print(f"模型调用: {state['messages'][-1].content}")
    result = call()
    print(f"模型响应: {result.content[:50]}...")
    return result
```

---

### @wrap_tool_call

包装工具调用：

```python
from langchain.agents.middleware import wrap_tool_call

@wrap_tool_call
def log_tool_call(state, runtime, tool_name, tool_input, call):
    print(f"工具调用: {tool_name}({tool_input})")
    result = call()
    print(f"工具结果: {result}")
    return result
```