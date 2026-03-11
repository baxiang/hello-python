# FastAPI 中间件

掌握 FastAPI 中间件的使用和自定义。

---

## 1. 内置中间件

### 1.1 CORS 中间件

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 1.2 GZip 中间件

```python
from fastapi.middleware.gzip import GZipMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)
```

---

## 2. 自定义中间件

### 2.1 基础中间件

```python
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
import time

app = FastAPI()

@app.middleware("http")
async def add_process_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

### 2.2 请求日志中间件

```python
@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    print(f"Response: {response.status_code}")
    return response
```

---

## 3. 中间件进阶

### 3.1 认证中间件

```python
from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 公开路径
        public_paths = ["/docs", "/openapi.json", "/token"]
        
        if request.url.path in public_paths:
            return await call_next(request)
        
        # 检查认证
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        return await call_next(request)

app.add_middleware(AuthMiddleware)
```

### 3.2 缓存中间件

```python
from starlette.middleware.base import BaseHTTPMiddleware

class CacheMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, cache):
        super().__init__(app)
        self.cache = cache
    
    async def dispatch(self, request: Request, call_next):
        if request.method != "GET":
            return await call_next(request)
        
        cache_key = str(request.url)
        if cache_key in self.cache:
            from starlette.responses import Response
            return Response(content=self.cache[cache_key], media_type="application/json")
        
        response = await call_next(request)
        
        if response.status_code == 200:
            # 缓存响应
            pass
        
        return response
```

---

## 4. 完整示例

```python
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import time

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GZip
app.add_middleware(GZipMiddleware, minimum_size=500)

# 自定义中间件
@app.middleware("http")
async def timing_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    process_time = time.time() - start
    response.headers["X-Process-Time"] = f"{process_time:.4f}"
    return response

@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response

@app.get("/")
async def root():
    return {"message": "Hello"}

@app.get("/slow")
async def slow():
    time.sleep(2)
    return {"message": "Done"}
```

---

## 总结

| 知识点 | 说明 |
|---------|------|
| CORSMiddleware | 跨域请求 |
| GZipMiddleware | 压缩 |
| BaseHTTPMiddleware | 自定义中间件 |
| 请求/响应处理 | 中间件钩子 |

---

[← 上一章](./05-FastAPI认证授权.md) | [下一章](./07-FastAPI错误处理.md)