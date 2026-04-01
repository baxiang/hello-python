# FastAPI 后台任务

掌握 FastAPI 后台任务处理。

---

## 1. BackgroundTasks

### 1.1 基本使用

```python
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

def write_log(message: str):
    with open("log.txt", "a") as f:
        f.write(f"{message}\n")

@app.post("/send-email/{email}")
async def send_email(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, f"Email sent to {email}")
    return {"message": "Email is being sent"}
```

### 1.2 带参数的任务

```python
def process_data(data: str, count: int):
    for i in range(count):
        print(f"Processing {data}: {i+1}/{count}")

@app.post("/process")
async def process(
    data: str,
    count: int = 5,
    background_tasks: BackgroundTasks = None
):
    background_tasks.add_task(process_data, data, count)
    return {"message": "Processing started"}
```

---

## 2. Celery 集成

### 2.1 安装

```bash
pip install celery redis
```

### 2.2 Celery 配置

```python
# celery_config.py
from celery import Celery

celery_app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1'
)

@celery_app.task
def send_email_task(to: str, subject: str, body: str):
    import time
    time.sleep(2)
    print(f"Email sent to {to}")
    return {"status": "sent", "to": to}

@celery_app.task
def process_data_task(data: list):
    result = sum(data)
    return {"result": result, "count": len(data)}
```

### 2.3 FastAPI 中使用

```python
from fastapi import FastAPI, BackgroundTasks
from celery import Celery
from celery_config import celery_app, send_email_task, process_data_task

app = FastAPI()

@app.post("/send-email")
async def send_email(email: str, subject: str, body: str):
    task = send_email_task.delay(email, subject, body)
    return {"task_id": task.id, "status": "queued"}

@app.post("/process")
async def process_data(numbers: list):
    task = process_data_task.delay(numbers)
    return {"task_id": task.id, "status": "queued"}

@app.get("/task/{task_id}")
async def get_task_status(task_id: str):
    task = celery_app.AsyncResult(task_id)
    return {
        "task_id": task.id,
        "status": task.state,
        "result": task.result if task.ready() else None
    }
```

---

## 3. 完整示例

```python
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from typing import List
import time

app = FastAPI()

# ==================== 任务函数 ====================
def write_notification(email: str, message: str):
    """写入通知日志"""
    with open("notifications.txt", "a") as f:
        f.write(f"Email: {email}, Message: {message}\n")

def send_email_async(email: str, subject: str, body: str):
    """模拟发送邮件"""
    time.sleep(2)  # 模拟耗时操作
    print(f"Email sent: {subject} to {email}")

def process_batch(items: List[dict]):
    """批量处理"""
    results = []
    for item in items:
        time.sleep(0.5)
        results.append({"processed": item})
    return results

# ==================== 路由 ====================
class EmailRequest(BaseModel):
    email: str
    subject: str
    body: str

class ProcessRequest(BaseModel):
    items: List[dict]

@app.post("/notify")
async def notify(email: str, message: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message)
    return {"message": "Notification queued"}

@app.post("/email")
async def send_email(request: EmailRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(
        send_email_async,
        request.email,
        request.subject,
        request.body
    )
    return {"message": "Email sending in background"}

@app.post("/batch")
async def process_batch_items(request: ProcessRequest, background_tasks: BackgroundTasks):
    task = background_tasks.add_task(
        process_batch,
        request.items
    )
    return {"message": "Batch processing started", "task_id": id(task)}
```

---

## 总结

| 知识点 | 说明 |
|---------|------|
| BackgroundTasks | 轻量后台任务 |
| add_task | 添加任务 |
| Celery | 生产级任务队列 |
| AsyncResult | 任务状态 |

---

[← 上一章](./08-FastAPI-WebSocket.md) | [下一章](./10-FastAPI测试与部署.md)