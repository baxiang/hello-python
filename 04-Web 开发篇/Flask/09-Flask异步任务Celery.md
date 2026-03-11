# Flask 异步任务 Celery

掌握 Celery 实现异步任务处理。

---

## 1. Celery 基础

### 1.1 安装

```bash
pip install celery redis
```

### 1.2 配置

```python
# celery_config.py
from celery import Celery

celery_app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1'
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Shanghai',
    enable_utc=True,
)
```

---

## 2. 定义任务

### 2.1 基本任务

```python
# tasks.py
from celery_config import celery_app
import time

@celery_app.task
def send_email(to, subject, body):
    """发送邮件任务"""
    time.sleep(2)  # 模拟发送
    print(f'Email sent to {to}')
    return {'status': 'sent', 'to': to}

@celery_app.task
def process_data(data):
    """处理数据任务"""
    result = sum(data)
    return {'result': result, 'count': len(data)}
```

### 2.2 定时任务

```python
from celery.schedules import crontab

celery_app.conf.beat_schedule = {
    'daily-cleanup': {
        'task': 'tasks.cleanup',
        'schedule': crontab(hour=2, minute=0),
    },
}
```

---

## 3. Flask 集成

### 3.1 应用配置

```python
# app.py
from flask import Flask, request, jsonify
from celery import Celery

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_RESULT_BACKEND']
    )
    celery.conf.update(app.config)
    
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    
    celery.Task = ContextTask
    return celery

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/1'

celery = make_celery(app)

# 任务
@celery.task
def long_task():
    import time
    time.sleep(10)
    return 'Done'

# 路由
@app.route('/start-task')
def start_task():
    task = long_task.delay()
    return jsonify({'task_id': task.id})

@app.route('/task-status/<task_id>')
def task_status(task_id):
    task = celery.AsyncResult(task_id)
    return jsonify({
        'task_id': task.id,
        'status': task.state,
        'result': task.result if task.ready() else None
    })

if __name__ == '__main__':
    app.run(debug=True)
```

---

## 4. 运行

### 4.1 启动 Worker

```bash
celery -A app.celery worker --loglevel=info
```

### 4.2 启动 Beat

```bash
celery -A app.celery beat --loglevel=info
```

---

## 总结

| 知识点 | 说明 |
|---------|------|
| Celery | 异步任务队列 |
| broker | 消息代理 |
| task | 任务定义 |
| delay | 异步调用 |

---

[← 上一章](./Flask/08-Flask缓存.md) | [下一章](./Flask/10-Flask部署.md)