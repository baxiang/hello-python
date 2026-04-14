# 09.03.02 - Agent 构建

**Agent：** 能自主调用工具的 LLM 应用，基于 ReAct 循环执行任务。

```
Agent 结构：
┌──────────────────────────────────────┐
│  create_agent                         │
│                                       │
│  输入: 用户问题                        │
│    ↓                                  │
│  LLM 决策 → 选择工具                   │
│    ↓                                  │
│  工具执行 → 返回结果                   │
│    ↓                                  │
│  LLM 生成 → 最终答案                   │
└──────────────────────────────────────┘
```

### 最简示例：创建 Agent

```python
from langchain.agents import create_agent
from langchain.tools import tool

@tool
def get_weather(city: str) -> str:
    """获取城市天气"""
    return f"{city} 天气晴朗，温度 25°C"

agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[get_weather],
)

result = agent.invoke({"messages": [{"role": "user", "content": "北京天气怎么样？"}]})
print(result["messages"][-1].content)
```

---

### 详细示例：多工具 Agent

```python
from langchain.agents import create_agent
from langchain.tools import tool
import datetime

@tool
def get_time() -> str:
    """获取当前时间"""
    return datetime.datetime.now().strftime("%H:%M")

@tool
def calculate(expr: str) -> str:
    """计算数学表达式"""
    return str(eval(expr))

@tool  
def search(query: str) -> str:
    """搜索信息"""
    return f"关于 {query} 的搜索结果..."

agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[get_time, calculate, search],
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "现在几点？10分钟后是什么时间？"}]
})
print(result["messages"][-1].content)
```

---

### 动态工具和模型

Agent 可以动态配置工具和模型：

```python
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

model = init_chat_model("anthropic:claude-3-sonnet")

agent = create_agent(
    model=model,
    tools=[get_weather, calculate],
    system_prompt="你是一个智能助手，善于使用工具解决问题。",
)
```

---

### 流式输出

Agent 支持流式输出：

```python
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "北京天气？"}]},
    stream_mode="updates",
):
    print(chunk)
```