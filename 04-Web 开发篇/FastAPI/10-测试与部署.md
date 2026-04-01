# FastAPI 测试与部署

掌握 FastAPI 应用测试和部署。

---

## 1. 测试基础

### 1.1 安装测试依赖

```bash
pip install pytest httpx
```

### 1.2 基本测试

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello"}

def test_create_item():
    response = client.post("/items", json={"name": "Test", "price": 10})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test"
```

---

## 2. 异步测试

### 2.1 async 测试

```python
import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_async():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
```

---

## 3. 单元测试

### 3.1 测试依赖

```python
from fastapi import Depends
from unittest.mock import Mock

def get_mock_db():
    return Mock()

@app.get("/items")
def get_items(db = Depends(get_mock_db)):
    return db.query.return_value.all()

# 测试
def test_get_items():
    mock_db = Mock()
    mock_db.query.return_value.all.return_value = [{"id": 1}]
    
    # 使用 mock
    response = client.get("/items")
    assert response.status_code == 200
```

---

## 4. 部署

### 4.1 Uvicorn

```bash
pip install uvicorn

# 运行
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 4.2 Gunicorn

```bash
pip install gunicorn

# 运行
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

---

## 5. Docker 部署

### 5.1 Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 5.2 docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/app
    depends_on:
      - db

  db:
    image: postgres:15

  redis:
    image: redis:7
```

---

## 6. 完整示例

### 6.1 应用代码

```python
# main.py
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# 模型
class Item(BaseModel):
    id: Optional[int] = None
    name: str
    price: float

# 模拟数据库
items_db = []

# 路由
@app.get("/")
def root():
    return {"message": "Hello API"}

@app.get("/items", response_model=List[Item])
def get_items():
    return items_db

@app.post("/items", response_model=Item, status_code=201)
def create_item(item: Item):
    item.id = len(items_db) + 1
    items_db.append(item)
    return item

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    for item in items_db:
        if item.id == item_id:
            return item
    from fastapi import HTTPException
    raise HTTPException(status_code=404, detail="Item not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 6.2 测试代码

```python
# test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello API"}

def test_create_item():
    response = client.post("/items", json={"name": "Test", "price": 10})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test"
    assert data["price"] == 10
    assert data["id"] == 1

def test_get_items():
    client.post("/items", json={"name": "Item 1", "price": 5})
    response = client.get("/items")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_get_item_not_found():
    response = client.get("/items/999")
    assert response.status_code == 404
```

### 6.3 运行测试

```bash
pytest test_main.py -v
```

---

## 总结

| 知识点 | 说明 |
|---------|------|
| TestClient | 同步测试 |
| AsyncClient | 异步测试 |
| Mock | 模拟依赖 |
| Uvicorn | ASGI 服务器 |
| Gunicorn | WSGI 服务器 |
| Docker | 容器化部署 |

---

[← 上一章](./09-FastAPI后台任务.md) | [返回目录](../README.md)