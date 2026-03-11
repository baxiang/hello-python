# 第 1 章：Web 基础入门

掌握 Web 开发的核心概念、HTTP 协议和 Web 架构。

---

## 本章目标

- 理解 Web 工作原理
- 掌握 HTTP 协议
- 了解 URL 和请求方法
- 认识 Web 架构模式

---

## 1.1 Web 工作原理

### 什么是 Web？

Web（World Wide Web）是一个由超文本组成的全球信息系统，通过互联网访问。

### 请求-响应模型

```
┌──────────┐         ┌──────────┐         ┌──────────┐
│  浏览器   │ ──────▶ │  服务器   │ ◀────── │  数据库   │
│ (Client) │  请求   │ (Server)  │  响应   │ (Database)│
└──────────┘         └──────────┘         └──────────┘
```

1. 用户在浏览器中输入 URL
2. 浏览器向服务器发送 HTTP 请求
3. 服务器处理请求，从数据库获取数据
4. 服务器返回 HTTP 响应（包含 HTML/CSS/JS）
5. 浏览器渲染页面

### URL 详解

```
https://www.example.com:443/path/to/page?id=123#section
│       │              │    │            │       │
│       │              │    │            │       └── 锚点
│       │              │    │            └────────── 路径
│       │              │    └───────────────────── 查询参数
│       │              │    端口号
│       │              └── 域名
│       └────────────────── 协议 (https)
└─────────────────────────── 主机名
```

---

## 1.2 HTTP 协议

### 什么是 HTTP？

HTTP（HyperText Transfer Protocol）是 Web 通信的基础协议，用于客户端和服务器之间的通信。

### HTTP 请求方法

| 方法 | 说明 | 幂等性 |
|------|------|--------|
| GET | 获取资源 | ✓ |
| POST | 创建资源 | ✗ |
| PUT | 更新资源（完整） | ✓ |
| PATCH | 更新资源（部分） | ✗ |
| DELETE | 删除资源 | ✓ |
| HEAD | 获取头部信息 | ✓ |
| OPTIONS | 获取支持的选项 | ✓ |

### HTTP 状态码

| 状态码 | 含义 | 说明 |
|--------|------|------|
| 200 | OK | 请求成功 |
| 201 | Created | 资源创建成功 |
| 204 | No Content | 请求成功，无返回内容 |
| 301 | Moved Permanently | 永久重定向 |
| 302 | Found | 临时重定向 |
| 400 | Bad Request | 请求语法错误 |
| 401 | Unauthorized | 未认证 |
| 403 | Forbidden | 无权限 |
| 404 | Not Found | 资源不存在 |
| 500 | Internal Server Error | 服务器错误 |
| 502 | Bad Gateway | 网关错误 |
| 503 | Service Unavailable | 服务不可用 |

### HTTP 请求结构

```http
GET /api/users HTTP/1.1
Host: www.example.com
Accept: application/json
Authorization: Bearer token123
User-Agent: Mozilla/5.0
```

### HTTP 响应结构

```http
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 123
Date: Mon, 01 Jan 2024 00:00:00 GMT

{
  "status": "success",
  "data": [...]
}
```

---

## 1.3 HTTP Header 详解

### 请求头

| 头部 | 说明 |
|------|------|
| Host | 服务器域名 |
| User-Agent | 客户端信息 |
| Accept | 可接受的响应类型 |
| Accept-Language | 可接受的语言 |
| Accept-Encoding | 可接受的编码 |
| Authorization | 认证信息 |
| Cookie | Cookie 数据 |
| Content-Type | 请求体类型 |

### 响应头

| 头部 | 说明 |
|------|------|
| Content-Type | 响应体类型 |
| Content-Length | 响应体长度 |
| Set-Cookie | 设置 Cookie |
| Cache-Control | 缓存控制 |
| Location | 重定向地址 |
| ETag | 资源版本标识 |

---

## 1.4 Web 架构模式

### 客户端-服务器架构

```
┌─────────────────────────────────────────────────────────┐
│                        客户端                            │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  │
│  │  浏览器  │  │  移动端  │  │ 桌面应用 │  │  API调用 │  │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘  │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                        服务器                            │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  │
│  │  Web服务器│  │  应用服务 │  │  缓存服务 │  │  任务队列 │  │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘  │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                        数据层                            │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐               │
│  │  主数据库 │  │  读写分离 │  │  搜索引擎 │               │
│  └─────────┘  └─────────┘  └─────────┘               │
└─────────────────────────────────────────────────────────┘
```

### MVC 架构

```
┌─────────────────────────────────────────────────────────┐
│                        控制器 (Controller)               │
│  处理请求、调用模型、返回响应                            │
└─────────────────────────────────────────────────────────┘
          │                    │                    │
          ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────┐
│                        模型 (Model)                      │
│  业务逻辑、数据处理、数据库操作                          │
└─────────────────────────────────────────────────────────┘
          │                    │                    │
          ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────┐
│                        视图 (View)                       │
│  模板渲染、JSON 返回、页面展示                          │
└─────────────────────────────────────────────────────────┘
```

### RESTful 架构

- 资源：URI 表示资源
- 动作：HTTP 方法表示操作
- 表现：JSON/XML 表示数据

```
GET    /api/users        # 获取用户列表
GET    /api/users/1      # 获取单个用户
POST   /api/users        # 创建用户
PUT    /api/users/1      # 更新用户
DELETE /api/users/1      # 删除用户
```

---

## 1.5 Cookie 和 Session

### Cookie

Cookie 是存储在客户端的小型文本文件，用于跟踪用户状态。

```python
# 设置 Cookie
response.set_cookie(
    key="user_id",
    value="123",
    max_age=3600,  # 秒
    httponly=True,
    secure=True
)

# 读取 Cookie
user_id = request.cookies.get("user_id")
```

### Session

Session 是存储在服务器端的用户会话数据。

```python
from flask import session

# 设置 Session
session['user_id'] = 123
session['username'] = 'john'

# 读取 Session
user_id = session.get('user_id')
```

---

## 1.6 Web 安全基础

### XSS（跨站脚本攻击）

```python
# 错误示例 - 直接输出用户输入
html = f"<h1>{user_input}</h1>"

# 正确示例 - 转义输出
from markupsafe import escape
html = f"<h1>{escape(user_input)}</h1>"
```

### CSRF（跨站请求伪造）

```python
# Flask-WTF 防护
from flask_wtf import CSRFProtect
csrf = CSRFProtect(app)
```

### SQL 注入

```python
# 错误示例
query = f"SELECT * FROM users WHERE name = '{name}'"

# 正确示例 - 使用参数化查询
query = "SELECT * FROM users WHERE name = %s"
cursor.execute(query, (name,))
```

---

## 1.7 实战：使用 Python 发送 HTTP 请求

### 安装 requests

```bash
pip install requests
```

### 发送 GET 请求

```python
import requests

# 简单 GET 请求
response = requests.get('https://api.example.com/users')
print(response.status_code)
print(response.json())

# 带参数的 GET 请求
params = {'page': 1, 'limit': 10}
response = requests.get('https://api.example.com/users', params=params)

# 带请求头的 GET 请求
headers = {'Authorization': 'Bearer token123'}
response = requests.get('https://api.example.com/users', headers=headers)
```

### 发送 POST 请求

```python
import requests

# POST 请求
data = {'username': 'john', 'email': 'john@example.com'}
response = requests.post('https://api.example.com/users', json=data)

# 上传文件
files = {'file': open('document.pdf', 'rb')}
response = requests.post('https://api.example.com/upload', files=files)
```

### 处理响应

```python
response = requests.get('https://api.example.com/users')

# 状态码
print(response.status_code)

# 响应头
print(response.headers)

# 响应体（自动解码）
print(response.text)

# JSON 响应
print(response.json())

# 二进制响应（用于图片等）
print(response.content)
```

### 错误处理

```python
try:
    response = requests.get('https://api.example.com/users', timeout=5)
    response.raise_for_status()  # 检查 4xx/5xx 错误
    print(response.json())
except requests.exceptions.Timeout:
    print("请求超时")
except requests.exceptions.ConnectionError:
    print("连接错误")
except requests.exceptions.HTTPError as e:
    print(f"HTTP 错误: {e}")
```

---

## 本章总结

### 学到的技能

| 技能 | 说明 |
|------|------|
| Web 原理 | 请求-响应模型 |
| HTTP 协议 | 请求方法、状态码、Header |
| URL 结构 | 协议、域名、路径、参数 |
| 架构模式 | MVC、RESTful |
| 安全基础 | XSS、CSRF、SQL 注入 |
| requests 库 | HTTP 请求发送 |

### 下一步

在 [第 2 章](./02-HTML 与 CSS.md) 中，我们将学习前端技术基础。

---

[← 回到目录](./README.md) | [下一篇 →](./02-HTML 与 CSS.md)