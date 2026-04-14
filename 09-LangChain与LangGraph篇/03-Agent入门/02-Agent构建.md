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

---

## create_agent：Agent 工厂

LangChain 提供生产级 Agent 实现：

```python
from langchain.agents import create_agent

agent = create_agent(
    model="openai:gpt-4o-mini",
    tools=[get_weather, search],
)
```

---

### 核心组件

| 参数 | 说明 |
|------|------|
| `model` | 语言模型（静态或动态） |
| `tools` | 工具列表（静态或动态） |
| `system_prompt` | 系统提示词 |
| `name` | Agent 名称（用于多 Agent） |
| `response_format` | 结构化输出 |
| `context_schema` | 运行时上下文 |
| `store` | 长期记忆 |
| `middleware` | 中间件 |

---

## Model：模型配置

### 静态模型

最常用的方式，配置后不变：

```python
# 方式1：字符串标识符
agent = create_agent("openai:gpt-4o-mini", tools=tools)

# 方式2：模型实例（更多控制）
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.1,
    max_tokens=1000,
    timeout=30,
)
agent = create_agent(model, tools=tools)
```

**字符串标识符自动推断：**
- `"gpt-4"` → `"openai:gpt-4"`
- `"claude-3"` → `"anthropic:claude-3"`

### 动态模型

运行时根据状态选择模型：

```python
from langchain_openai import ChatOpenAI
from langchain.agents.middleware import wrap_model_call

basic_model = ChatOpenAI(model="gpt-4o-mini")
advanced_model = ChatOpenAI(model="gpt-4o")

@wrap_model_call
def dynamic_model_selection(request, handler):
    message_count = len(request.state["messages"])
    
    if message_count > 10:
        model = advanced_model
    else:
        model = basic_model
    
    return handler(request.override(model=model))

agent = create_agent(
    model=basic_model,
    tools=tools,
    middleware=[dynamic_model_selection],
)
```

---

## Tools：工具配置

### 静态工具

定义时固定：

```python
from langchain.tools import tool

@tool
def search(query: str) -> str:
    """搜索信息"""
    return f"结果: {query}"

@tool
def get_weather(location: str) -> str:
    """获取天气"""
    return f"{location} 天气晴朗"

agent = create_agent(model, tools=[search, get_weather])
```

### 动态工具

运行时过滤或添加：

**基于状态过滤：**

```python
from langchain.agents.middleware import wrap_model_call

@wrap_model_call
def state_based_tools(request, handler):
    state = request.state
    is_authenticated = state.get("authenticated", False)
    
    if not is_authenticated:
        # 只暴露公开工具
        tools = [t for t in request.tools if t.name.startswith("public_")]
        request = request.override(tools=tools)
    
    return handler(request)
```

**基于上下文过滤：**

```python
from dataclasses import dataclass

@dataclass
class Context:
    user_role: str

@wrap_model_call
def context_based_tools(request, handler):
    user_role = request.runtime.context.user_role
    
    if user_role == "admin":
        pass  # 所有工具
    elif user_role == "editor":
        tools = [t for t in request.tools if t.name != "delete"]
        request = request.override(tools=tools)
    else:
        tools = [t for t in request.tools if t.name.startswith("read_")]
        request = request.override(tools=tools)
    
    return handler(request)

agent = create_agent(
    model="gpt-4o-mini",
    tools=[read_data, write_data, delete_data],
    middleware=[context_based_tools],
    context_schema=Context,
)
```

---

## System Prompt：系统提示词

### 静态提示词

```python
agent = create_agent(
    model,
    tools,
    system_prompt="你是一个有帮助的助手。简洁准确。",
)
```

### 使用 SystemMessage

```python
from langchain.messages import SystemMessage

agent = create_agent(
    model="anthropic:claude-3",
    system_prompt=SystemMessage(
        content=[
            {"type": "text", "text": "你是一个文学分析助手。"},
            {"type": "text", "text": "<小说全文>", "cache_control": {"type": "ephemeral"}},
        ]
    )
)
```

`cache_control` 让 Anthropic 缓存内容块，降低成本。

### 动态提示词

```python
from langchain.agents.middleware import dynamic_prompt

@dynamic_prompt
def user_role_prompt(request) -> str:
    user_role = request.runtime.context.get("user_role", "user")
    base = "你是一个有帮助的助手。"
    
    if user_role == "expert":
        return f"{base} 提供详细技术回答。"
    elif user_role == "beginner":
        return f"{base} 简单解释，避免术语。"
    
    return base

agent = create_agent(
    model="gpt-4o-mini",
    tools=[search],
    middleware=[user_role_prompt],
)
```

---

## 调用 Agent

### invoke：单次调用

```python
result = agent.invoke({
    "messages": [{"role": "user", "content": "北京天气怎么样？"}]
})

print(result["messages"][-1].content)
```

### stream：流式输出

```python
from langchain.messages import AIMessage, HumanMessage

for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "搜索AI新闻"}]},
    stream_mode="values",
):
    latest = chunk["messages"][-1]
    if isinstance(latest, HumanMessage):
        print(f"用户: {latest.content}")
    elif isinstance(latest, AIMessage):
        if latest.content:
            print(f"Agent: {latest.content}")
        elif latest.tool_calls:
            print(f"调用工具: {[tc['name'] for tc in latest.tool_calls]}")
```

---

## Structured Output：结构化输出

### ToolStrategy

通过工具调用实现，适用于所有支持工具的模型：

```python
from pydantic import BaseModel
from langchain.agents.structured_output import ToolStrategy

class ContactInfo(BaseModel):
    name: str
    email: str
    phone: str

agent = create_agent(
    model="gpt-4o-mini",
    response_format=ToolStrategy(ContactInfo),
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "提取联系方式：张三，zhang@example.com，13800138000"}]
})

print(result["structured_response"])
# ContactInfo(name='张三', email='zhang@example.com', phone='13800138000')
```

### ProviderStrategy

使用提供商原生结构化输出（更可靠）：

```python
from langchain.agents.structured_output import ProviderStrategy

agent = create_agent(
    model="gpt-4o",
    response_format=ProviderStrategy(ContactInfo),
)
```

**自动选择：** 传入 schema（如 `response_format=ContactInfo`）时自动使用 ProviderStrategy（如果支持）。

---

## Name：Agent 名称

用于多 Agent 系统的节点标识：

```python
agent = create_agent(
    model,
    tools,
    name="research_assistant",
)
```

**命名建议：** 使用 `snake_case`，避免空格和特殊字符。

---

## 错误处理

### 工具错误中间件

```python
from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage

@wrap_tool_call
def handle_tool_errors(request, handler):
    try:
        return handler(request)
    except Exception as e:
        return ToolMessage(
            content=f"工具错误: 请检查输入。({str(e)})",
            tool_call_id=request.tool_call["id"]
        )

agent = create_agent(
    model="gpt-4o-mini",
    tools=[search],
    middleware=[handle_tool_errors],
)
```

---

## 为什么用它？

```python
# 没有 Agent：手动管理
model.invoke("搜索天气")
# 手动解析工具调用
# 手动执行工具
# 手动传回模型

# 有 Agent：自动循环
agent.invoke("搜索北京天气")
# Agent 自动：决策 → 执行 → 循环 → 完成
```