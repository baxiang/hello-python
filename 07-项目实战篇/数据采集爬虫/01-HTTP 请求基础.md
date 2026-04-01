# HTTP 请求基础

学习使用 requests 库发送 HTTP 请求获取网页内容。

---

## 1. requests 库

### 1.1 安装

```bash
uv add requests
```

### 1.2 基本请求

```python
import requests

# GET 请求
response = requests.get("https://httpbin.org/get")
print(response.status_code)  # 200
print(response.text)         # 响应内容

# POST 请求
response = requests.post(
    "https://httpbin.org/post",
    data={"key": "value"}
)
```

### 1.3 请求方法

```
┌─────────────────────────────────────────────────────────────┐
│                    HTTP 请求方法                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   方法      用途                  示例                       │
│   ─────────────────────────────────────────────────────     │
│   GET      获取资源            requests.get(url)            │
│   POST     提交数据            requests.post(url, data)     │
│   PUT      更新资源            requests.put(url, data)      │
│   DELETE   删除资源            requests.delete(url)         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. 请求参数

### 2.1 URL 参数

```python
# 查询参数
response = requests.get(
    "https://httpbin.org/get",
    params={
        "page": 1,
        "size": 20,
        "keyword": "python"
    }
)
# 实际 URL: https://httpbin.org/get?page=1&size=20&keyword=python
```

### 2.2 请求头

```python
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Referer": "https://example.com"
}

response = requests.get("https://httpbin.org/headers", headers=headers)
```

### 2.3 Cookie

```python
# 发送 Cookie
cookies = {"session": "abc123", "user": "alice"}
response = requests.get("https://httpbin.org/cookies", cookies=cookies)

# 从响应获取 Cookie
response = requests.get("https://httpbin.org/cookies/set?name=value")
print(response.cookies.get("name"))  # value
```

---

## 3. 响应处理

### 3.1 响应属性

```python
response = requests.get("https://httpbin.org/get")

# 状态码
print(response.status_code)    # 200
print(response.ok)             # True (状态码 200-399)

# 响应内容
print(response.text)           # 文本内容
print(response.content)        # 字节内容
print(response.json())         # JSON 解析

# 编码
print(response.encoding)       # utf-8
response.encoding = "gbk"      # 手动设置编码

# 响应头
print(response.headers["Content-Type"])
```

### 3.2 状态码处理

```python
response = requests.get("https://httpbin.org/status/404")

if response.status_code == 200:
    print("请求成功")
elif response.status_code == 404:
    print("页面不存在")
elif response.status_code == 500:
    print("服务器错误")
else:
    print(f"其他错误: {response.status_code}")

# 使用 raise_for_status
try:
    response = requests.get("https://httpbin.org/status/404")
    response.raise_for_status()  # 非 2xx 状态码抛出异常
except requests.HTTPError as e:
    print(f"HTTP 错误: {e}")
```

---

## 4. Session 会话

### 4.1 使用 Session

```python
# Session 自动管理 Cookie
session = requests.Session()

# 登录
session.post("https://example.com/login", data={
    "username": "alice",
    "password": "123456"
})

# 后续请求自动携带登录 Cookie
response = session.get("https://example.com/profile")
```

### 4.2 Session 配置

```python
session = requests.Session()

# 设置默认请求头
session.headers.update({
    "User-Agent": "MyCrawler/1.0"
})

# 设置默认超时
session.request = lambda *args, **kwargs: requests.Session.request(session, *args, timeout=10, **kwargs)
```

---

## 5. 超时和重试

### 5.1 超时设置

```python
# 连接超时 + 读取超时
response = requests.get(
    "https://httpbin.org/delay/2",
    timeout=(3, 10)  # 连接超时 3 秒，读取超时 10 秒
)

# 统一超时
response = requests.get(url, timeout=10)
```

### 5.2 重试机制

```python
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

session = requests.Session()

# 配置重试策略
retry = Retry(
    total=3,              # 总重试次数
    backoff_factor=1,     # 重试间隔倍数
    status_forcelist=[500, 502, 503, 504]  # 触发重试的状态码
)

adapter = HTTPAdapter(max_retries=retry)
session.mount("http://", adapter)
session.mount("https://", adapter)

# 使用 session 发送请求
response = session.get("https://httpbin.org/status/500")
```

---

## 6. 异步请求

### 6.1 使用 httpx

```bash
uv add httpx
```

```python
import httpx
import asyncio

async def fetch(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.text

async def fetch_multiple(urls: list):
    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        return [r.text for r in responses]

# 运行
urls = [
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/2",
    "https://httpbin.org/delay/3"
]
results = asyncio.run(fetch_multiple(urls))
```

---

## 本章小结

```
┌─────────────────────────────────────────────────────────────┐
│                    HTTP 请求知识要点                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   基本请求：                                                 │
│   ✓ requests.get/post/put/delete                           │
│   ✓ params 查询参数                                         │
│   ✓ headers 请求头                                          │
│                                                             │
│   响应处理：                                                 │
│   ✓ status_code 状态码                                      │
│   ✓ text/content/json 内容                                  │
│   ✓ raise_for_status 异常处理                               │
│                                                             │
│   高级功能：                                                 │
│   ✓ Session 会话管理                                        │
│   ✓ timeout 超时设置                                        │
│   ✓ Retry 重试机制                                          │
│   ✓ httpx 异步请求                                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

[← 返回目录](./README.md) | [下一章：HTML 解析 →](./02-HTML%20解析.md)