# Web 聊天界面

使用 FastAPI + WebSocket 实现 Web 端的 AI 聊天界面。

---

## 1. 项目结构

```
ai-chat-web/
├── main.py              # FastAPI 主程序
├── chat.py              # 聊天核心逻辑
├── static/
│   └── index.html       # 前端页面
├── .env                 # 配置
└── requirements.txt
```

---

## 2. 后端实现

### 2.1 FastAPI 主程序 (main.py)

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()

app = FastAPI(title="AI Chat")

# 静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")

# OpenAI 客户端
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("BASE_URL")
)

MODEL = os.getenv("MODEL", "gpt-4o-mini")


class ConnectionManager:
    """WebSocket 连接管理器"""
    
    def __init__(self):
        self.active_connections: list[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)


manager = ConnectionManager()


@app.get("/", response_class=HTMLResponse)
async def get():
    """返回聊天页面"""
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """WebSocket 聊天端点"""
    await manager.connect(websocket)
    
    # 对话历史
    messages = [
        {"role": "system", "content": "你是一个友好的助手"}
    ]
    
    try:
        while True:
            # 接收用户消息
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            user_message = message_data.get("content", "")
            if not user_message:
                continue
            
            # 添加到历史
            messages.append({"role": "user", "content": user_message})
            
            # 发送开始标记
            await websocket.send_text(json.dumps({
                "type": "start",
                "role": "assistant"
            }))
            
            # 流式调用 API
            stream = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                stream=True
            )
            
            full_response = ""
            
            for chunk in stream:
                delta = chunk.choices[0].delta
                if delta.content:
                    full_response += delta.content
                    # 发送内容块
                    await websocket.send_text(json.dumps({
                        "type": "chunk",
                        "content": delta.content
                    }))
            
            # 保存回复到历史
            messages.append({"role": "assistant", "content": full_response})
            
            # 发送结束标记
            await websocket.send_text(json.dumps({
                "type": "end"
            }))
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## 3. 前端实现

### 3.1 HTML 页面 (static/index.html)

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Chat</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        .header {
            background: #2c3e50;
            color: white;
            padding: 16px;
            text-align: center;
        }
        
        .chat-container {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            max-width: 800px;
            margin: 0 auto;
            width: 100%;
        }
        
        .message {
            margin-bottom: 16px;
            display: flex;
            gap: 12px;
        }
        
        .message.user {
            flex-direction: row-reverse;
        }
        
        .avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            flex-shrink: 0;
        }
        
        .message.user .avatar {
            background: #3498db;
            color: white;
        }
        
        .message.assistant .avatar {
            background: #2ecc71;
            color: white;
        }
        
        .content {
            background: white;
            padding: 12px 16px;
            border-radius: 12px;
            max-width: 70%;
            line-height: 1.6;
            box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        }
        
        .message.user .content {
            background: #3498db;
            color: white;
        }
        
        .input-container {
            padding: 16px;
            background: white;
            border-top: 1px solid #eee;
        }
        
        .input-wrapper {
            max-width: 800px;
            margin: 0 auto;
            display: flex;
            gap: 12px;
        }
        
        #messageInput {
            flex: 1;
            padding: 12px 16px;
            border: 1px solid #ddd;
            border-radius: 24px;
            font-size: 16px;
            outline: none;
        }
        
        #messageInput:focus {
            border-color: #3498db;
        }
        
        #sendBtn {
            padding: 12px 24px;
            background: #3498db;
            color: white;
            border: none;
            border-radius: 24px;
            cursor: pointer;
            font-size: 16px;
        }
        
        #sendBtn:hover {
            background: #2980b9;
        }
        
        #sendBtn:disabled {
            background: #bdc3c7;
            cursor: not-allowed;
        }
        
        .typing {
            opacity: 0.7;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>AI Chat</h1>
    </div>
    
    <div class="chat-container" id="chatContainer">
        <!-- 消息会动态添加到这里 -->
    </div>
    
    <div class="input-container">
        <div class="input-wrapper">
            <input type="text" id="messageInput" placeholder="输入消息..." autocomplete="off">
            <button id="sendBtn">发送</button>
        </div>
    </div>

    <script>
        const chatContainer = document.getElementById('chatContainer');
        const messageInput = document.getElementById('messageInput');
        const sendBtn = document.getElementById('sendBtn');
        
        let ws = null;
        let currentAssistantMessage = null;
        
        // 连接 WebSocket
        function connect() {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            ws = new WebSocket(`${protocol}//${window.location.host}/ws/chat`);
            
            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                handleMessage(data);
            };
            
            ws.onclose = () => {
                console.log('WebSocket 已断开');
            };
        }
        
        // 处理消息
        function handleMessage(data) {
            switch (data.type) {
                case 'start':
                    // 创建新的助手消息
                    currentAssistantMessage = createMessage('assistant', '');
                    break;
                    
                case 'chunk':
                    // 追加内容
                    if (currentAssistantMessage) {
                        currentAssistantMessage.querySelector('.content').textContent += data.content;
                        scrollToBottom();
                    }
                    break;
                    
                case 'end':
                    // 消息完成
                    currentAssistantMessage = null;
                    sendBtn.disabled = false;
                    break;
            }
        }
        
        // 创建消息元素
        function createMessage(role, content) {
            const div = document.createElement('div');
            div.className = `message ${role}`;
            
            const avatar = document.createElement('div');
            avatar.className = 'avatar';
            avatar.textContent = role === 'user' ? '我' : 'AI';
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'content';
            contentDiv.textContent = content;
            
            div.appendChild(avatar);
            div.appendChild(contentDiv);
            chatContainer.appendChild(div);
            
            scrollToBottom();
            return div;
        }
        
        // 发送消息
        function sendMessage() {
            const content = messageInput.value.trim();
            if (!content) return;
            
            // 显示用户消息
            createMessage('user', content);
            
            // 发送到服务器
            ws.send(JSON.stringify({
                type: 'message',
                content: content
            }));
            
            // 清空输入框
            messageInput.value = '';
            sendBtn.disabled = true;
        }
        
        // 滚动到底部
        function scrollToBottom() {
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        
        // 事件绑定
        sendBtn.addEventListener('click', sendMessage);
        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
        
        // 初始化
        connect();
    </script>
</body>
</html>
```

---

## 4. 运行项目

### 4.1 安装依赖

```bash
uv init ai-chat-web
cd ai-chat-web
uv add fastapi uvicorn openai python-dotenv
```

### 4.2 配置

```bash
cat > .env << EOF
OPENAI_API_KEY=your-api-key
MODEL=gpt-4o-mini
EOF
```

### 4.3 启动服务

```bash
uv run python main.py
```

访问 http://localhost:8000 即可使用。

---

## 5. 功能扩展

### 5.1 添加会话管理

```python
# 在 main.py 中添加
from datetime import datetime
import uuid

sessions = {}  # session_id -> messages

@app.post("/api/session")
async def create_session():
    session_id = str(uuid.uuid4())
    sessions[session_id] = [
        {"role": "system", "content": "你是一个友好的助手"}
    ]
    return {"session_id": session_id}
```

### 5.2 添加 Markdown 渲染

```html
<!-- 在 HTML 中添加 marked.js -->
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>

<!-- 修改内容渲染 -->
contentDiv.innerHTML = marked.parse(content);
```

---

## 本章小结

```
┌─────────────────────────────────────────────────────────────┐
│                    Web 聊天界面知识要点                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   后端：                                                     │
│   ✓ FastAPI + WebSocket                                    │
│   ✓ 流式响应推送                                            │
│   ✓ 连接管理器                                              │
│                                                             │
│   前端：                                                     │
│   ✓ WebSocket 连接                                          │
│   ✓ 消息渲染                                                │
│   ✓ 实时更新                                                │
│                                                             │
│   扩展功能：                                                 │
│   ✓ 会话管理                                                │
│   ✓ Markdown 渲染                                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

[← 上一章：CLI 聊天工具](./04-CLI%20聊天工具.md) | [返回目录](./README.md)