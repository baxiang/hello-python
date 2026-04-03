# LLM API 基础

学习如何调用大语言模型 API，包括 OpenAI 和本地模型。

---

## 1. OpenAI API 调用

### 1.1 安装依赖

```bash
# 使用 uv 安装
uv add openai

# 或使用 pip
pip install openai
```

### 1.2 基本调用

```python
from openai import OpenAI

# 初始化客户端
client = OpenAI(api_key="your-api-key")

# 发送请求
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "你好，介绍一下 Python"}
    ]
)

# 获取响应
print(response.choices[0].message.content)
```

### 1.3 使用环境变量

**推荐方式：将 API Key 存储在环境变量中**

```python
# .env 文件
OPENAI_API_KEY=sk-your-api-key

# 代码中自动读取
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # 加载 .env 文件
client = OpenAI()  # 自动读取 OPENAI_API_KEY
```

---

## 2. 消息格式

### 2.1 角色类型

```
┌─────────────────────────────────────────────────────────────┐
│                    消息角色说明                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   role      说明                                            │
│   ─────────────────────────────────────────────────────     │
│   system    设定 AI 的行为和角色                            │
│   user      用户输入的问题                                  │
│   assistant AI 的回复                                       │
│                                                             │
│   对话顺序：system → user → assistant → user → ...          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 完整对话示例

```python
messages = [
    {"role": "system", "content": "你是一个 Python 编程助手"},
    {"role": "user", "content": "如何读取 JSON 文件？"},
    {"role": "assistant", "content": "可以使用 json.load()..."},
    {"role": "user", "content": "能举个例子吗？"}
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages
)
```

---

## 3. 常用参数

```python
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    
    # 控制输出
    temperature=0.7,      # 0-2，越高越随机
    max_tokens=1000,      # 最大输出长度
    top_p=0.9,            # 采样范围
    
    # 停止条件
    stop=["\n", "END"],   # 遇到这些停止
    
    # 流式输出
    stream=True,          # 启用流式响应
)
```

**参数说明：**

| 参数 | 说明 | 建议值 |
|------|------|--------|
| temperature | 创造性程度 | 代码：0.2，创意：0.8 |
| max_tokens | 输出长度限制 | 根据需求设置 |
| stream | 流式输出 | 长回复时启用 |

---

## 4. 国内模型 API

### 4.1 通义千问（阿里云）

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-dashscope-api-key",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

response = client.chat.completions.create(
    model="qwen-plus",
    messages=[{"role": "user", "content": "你好"}]
)
```

### 4.2 DeepSeek

```python
client = OpenAI(
    api_key="your-deepseek-api-key",
    base_url="https://api.deepseek.com/v1"
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "你好"}]
)
```

### 4.3 本地模型（Ollama）

```bash
# 安装 Ollama
# macOS: brew install ollama
# Linux: curl -fsSL https://ollama.com/install.sh | sh

# 下载模型
ollama pull qwen2.5:7b

# 启动服务
ollama serve
```

```python
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # Ollama 不需要真实 key
)

response = client.chat.completions.create(
    model="qwen2.5:7b",
    messages=[{"role": "user", "content": "你好"}]
)
```

---

## 5. 错误处理

```python
from openai import OpenAI, APIError, RateLimitError

client = OpenAI()

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "你好"}]
    )
except RateLimitError:
    print("API 调用频率超限，请稍后重试")
except APIError as e:
    print(f"API 错误: {e}")
except Exception as e:
    print(f"其他错误: {e}")
```

---

## 本章小结

```
┌─────────────────────────────────────────────────────────────┐
│                    LLM API 知识要点                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   API 调用：                                                 │
│   ✓ OpenAI SDK（推荐）                                      │
│   ✓ 国内模型：通义千问、DeepSeek                            │
│   ✓ 本地模型：Ollama                                        │
│                                                             │
│   消息格式：                                                 │
│   ✓ system/user/assistant 角色                             │
│   ✓ messages 列表管理                                       │
│                                                             │
│   参数控制：                                                 │
│   ✓ temperature 控制创造性                                  │
│   ✓ max_tokens 限制长度                                     │
│   ✓ stream 流式输出                                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

[← 返回目录](./README.md) | [下一章：对话管理 →](./02-对话管理.md)