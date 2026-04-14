# 09.06.02 - Middleware 扩展

**Middleware：** 拦截和增强 Agent 执行的机制，在每个步骤前后提供钩子。

```
Middleware：
┌──────────────────────────────────────┐
│  before_agent  → Agent 执行前         │
│  after_agent   → Agent 执行后         │
│                                       │
│  wrap_model_call → 包装模型调用       │
│  wrap_tool_call  → 包装工具调用       │
│                                       │
│  Guardrails → 输入/输出验证           │
│  HumanInTheLoop → 人工审核            │
│  Summarization → 自动摘要             │
└──────────────────────────────────────┘
```

### Middleware 用途

- 日志追踪、分析、调试
- Prompt 转换、工具选择、输出格式化
- 重试、降级、提前终止
- 速率限制、护栏、PII 检测

---

### Agent 执行流程

```
Agent Loop：
┌──────────────────────────────────────┐
│  before_agent                         │
│    ↓                                  │
│  wrap_model_call                      │
│    ↓                                  │
│  model.invoke() → 工具调用？          │
│    ↓                                  │
│  wrap_tool_call                       │
│    ↓                                  │
│  tool.invoke()                        │
│    ↓                                  │
│  循环直到无工具调用                    │
│    ↓                                  │
│  after_agent                          │
└──────────────────────────────────────┘
```

---

### 添加 Middleware

```python
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware, HumanInTheLoopMiddleware

agent = create_agent(
    model="moonshot:moonshot-v1-8k",
    tools=[...],
    middleware=[
        SummarizationMiddleware(...),
        HumanInTheLoopMiddleware(...),
    ],
)
```

---

### @wrap_model_call

**包装模型调用：**

```python
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse

@wrap_model_call
def log_model(request: ModelRequest, handler) -> ModelResponse:
    print(f"模型调用: {request.state['messages'][-1].content}")
    result = handler(request)
    print(f"模型响应: {result.response.content[:50]}...")
    return result
```

**ModelRequest 字段：**

| 字段 | 说明 |
|------|------|
| state | 当前图状态 |
| tools | 可用工具列表 |
| runtime | Runtime 对象 |
| model | 当前模型 |

**动态模型选择：**

```python
from langchain_openai import ChatOpenAI

basic_model = ChatOpenAI(
    model="moonshot-v1-8k",
    openai_api_base="https://api.moonshot.cn/v1",
)
advanced_model = ChatOpenAI(
    model="moonshot-v1-32k",
    openai_api_base="https://api.moonshot.cn/v1",
)

@wrap_model_call
def dynamic_model(request: ModelRequest, handler) -> ModelResponse:
    message_count = len(request.state["messages"])
    
    if message_count > 10:
        model = advanced_model
    else:
        model = basic_model
    
    return handler(request.override(model=model))
```

---

### @wrap_tool_call

**包装工具调用：**

```python
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
```

**动态工具过滤：**

```python
@wrap_model_call
def filter_tools(request: ModelRequest, handler) -> ModelResponse:
    is_authenticated = request.state.get("authenticated", False)
    
    if not is_authenticated:
        tools = [t for t in request.tools if t.name.startswith("public_")]
        return handler(request.override(tools=tools))
    
    return handler(request)
```

---

### @before_agent

**Agent 执行前拦截：**

```python
from langchain.agents.middleware import before_agent

@before_agent
def input_guardrail(state, runtime):
    user_input = state["messages"][-1].content
    
    if "敏感词" in user_input:
        return {"messages": ["输入包含敏感内容，请重新输入"]}
    
    return None  # 继续执行
```

---

### @after_agent

**Agent 执行后拦截：**

```python
from langchain.agents.middleware import after_agent

@after_agent(can_jump_to=["end"])
def output_guardrail(state, runtime):
    last_message = state["messages"][-1]
    
    if "敏感内容" in last_message.content:
        last_message.content = "无法提供该回复，请重新提问"
    
    return None
```

---

### HumanInTheLoopMiddleware

**预置人工审核中间件：**

```python
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver

agent = create_agent(
    model="moonshot:moonshot-v1-8k",
    tools=[send_email, delete_file],
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={"send_email": True, "delete_file": True}
        ),
    ],
    checkpointer=InMemorySaver(),
)

# 第一次调用 - 中断
result = agent.invoke({"messages": [{"role": "user", "content": "发送邮件"}]}, config)

# 恢复执行
result = agent.invoke(Command(resume={"type": "approve"}), config)
```

---

### SummarizationMiddleware

**预置摘要中间件：**

```python
from langchain.agents.middleware import SummarizationMiddleware

agent = create_agent(
    model="moonshot:moonshot-v1-8k",
    tools=[...],
    middleware=[
        SummarizationMiddleware(
            model="moonshot:moonshot-v1-8k",
            token_limit=4000,  # 超过 4000 token 时摘要
        ),
    ],
)
```

---

### @dynamic_prompt

**动态系统提示：**

```python
from langchain.agents.middleware import dynamic_prompt, ModelRequest

@dynamic_prompt
def user_role_prompt(request: ModelRequest) -> str:
    user_role = request.runtime.context.get("user_role", "user")
    
    if user_role == "expert":
        return "你是专家助手，提供详细技术回答。"
    elif user_role == "beginner":
        return "你是助手，用简单语言解释概念。"
    
    return "你是一个友好的助手。"
```

---

### 自定义 Middleware 类

```python
from langchain.agents.middleware import AgentMiddleware

class CustomMiddleware(AgentMiddleware):
    state_schema = CustomState
    tools = [tool1, tool2]
    
    def wrap_model_call(self, request: ModelRequest, handler) -> ModelResponse:
        ...
    
    def wrap_tool_call(self, request: ToolCallRequest, handler):
        ...
    
    def before_agent(self, state, runtime):
        ...
    
    def after_agent(self, state, runtime):
        ...
```

---

### 动态工具注册

**运行时添加工具：**

```python
class DynamicToolMiddleware(AgentMiddleware):
    def wrap_model_call(self, request: ModelRequest, handler) -> ModelResponse:
        updated = request.override(tools=[*request.tools, new_tool])
        return handler(updated)
    
    def wrap_tool_call(self, request: ToolCallRequest, handler):
        if request.tool_call["name"] == "new_tool":
            return handler(request.override(tool=new_tool))
        return handler(request)
```

---

### Guardrails：安全护栏

**输入验证：**

```python
@before_agent
def input_guardrail(state, runtime):
    content = state["messages"][-1].content
    
    banned_words = ["密码", "信用卡"]
    for word in banned_words:
        if word in content:
            return {"messages": [AIMessage("请勿输入敏感信息")]}
    
    return None
```

**输出验证：**

```python
@after_agent
def output_guardrail(state, runtime):
    last = state["messages"][-1]
    
    if isinstance(last, AIMessage):
        if contains_pii(last.content):
            last.content = redact_pii(last.content)
    
    return None
```

---

### PII 检测

```python
import re

def contains_pii(text: str) -> bool:
    patterns = [
        r'\b\d{16}\b',  # 信用卡
        r'\b[A-Z]{2}\d{9}\b',  # 身份证
    ]
    return any(re.search(p, text) for p in patterns)

def redact_pii(text: str) -> str:
    return re.sub(r'\b\d{16}\b', '[CARD]', text)
```

---

### Middleware 总结

| 钩子 | 时机 | 用途 |
|------|------|------|
| before_agent | Agent 执行前 | 输入验证、日志 |
| after_agent | Agent 执行后 | 输出验证、日志 |
| wrap_model_call | 模型调用时 | 动态模型、工具过滤 |
| wrap_tool_call | 工具调用时 | 错误处理、日志 |
| dynamic_prompt | Prompt 生成时 | 动态系统提示 |

**预置 Middleware：**

| Middleware | 用途 |
|------------|------|
| HumanInTheLoopMiddleware | 工具审核 |
| SummarizationMiddleware | 自动摘要 |
| ModelFallbackMiddleware | 模型降级 |
| ToolRetryMiddleware | 工具重试 |