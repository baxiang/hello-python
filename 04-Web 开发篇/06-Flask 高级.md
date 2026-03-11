# 第 6 章：Flask 高级

深入学习 Flask 认证、缓存、异步任务和部署。

---

## 本章目标

- 实现 JWT 用户认证
- 掌握 Flask 缓存
- 理解 Celery 异步任务
- 学会错误处理
- 了解部署选项

---

## 6.1 用户认证

### 安装依赖

```bash
pip install flask-jwt-extended flask-login flask-bcrypt
```

### 用户认证实现

```python
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
from flask_bcrypt import Bcrypt
from datetime import timedelta

app = Flask(__name__)

# 配置
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# 用户模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

# 注册
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': '用户名已存在'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': '邮箱已被注册'}), 400
    
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': '注册成功'}), 201

# 登录
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': '用户名或密码错误'}), 401
    
    # 创建 Token
    access_token = create_access_token(
        identity=user.id,
        expires_delta=timedelta(hours=1)
    )
    refresh_token = create_refresh_token(
        identity=user.id,
        expires_delta=timedelta(days=7)
    )
    
    return jsonify({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user': {'id': user.id, 'username': user.username}
    })

# 受保护的路由
@app.route('/profile')
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email
    })

# 刷新 Token
@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)
    return jsonify({'access_token': access_token})

# 错误处理
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({'error': 'Token 已过期'}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({'error': '无效的 Token'}), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({'error': '缺少 Token'}), 401
```

---

## 6.2 缓存

### 安装和使用

```bash
pip install flask-caching
```

```python
from flask import Flask
from flask_caching import Cache

app = Flask(__name__)
app.config['CACHE_TYPE'] = 'simple'  # 简单缓存
# app.config['CACHE_TYPE'] = 'redis'
# app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'

cache = Cache(app)

# 缓存视图
@app.route('/api/data')
@cache.cached(timeout=60, query_string=True)
def get_data():
    # 模拟耗时操作
    import time
    time.sleep(2)
    return {'data': 'some data'}

# 缓存函数结果
@cache.memoize(timeout=300)
def expensive_function(x):
    import time
    time.sleep(2)
    return x * 2

# 手动缓存操作
@app.route('/cache/set')
def set_cache():
    cache.set('key', 'value', timeout=60)
    return '缓存已设置'

@app.route('/cache/get')
def get_cache():
    value = cache.get('key')
    return f'缓存值: {value}'

@app.route('/cache/delete')
def delete_cache():
    cache.delete('key')
    return '缓存已删除'

# 清除所有缓存
@app.route('/cache/clear')
def clear_cache():
    cache.clear()
    return '所有缓存已清除'
```

---

## 6.3 异步任务

### 安装 Celery

```bash
pip install celery
```

### Celery 配置

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

# 定义任务
@celery_app.task
def send_email(to, subject, body):
    """发送邮件任务"""
    import time
    time.sleep(2)  # 模拟发送
    print(f'邮件已发送到: {to}')
    return {'status': 'sent', 'to': to}

@celery_app.task
def process_data(data):
    """处理数据任务"""
    import time
    time.sleep(5)  # 模拟处理
    result = sum(data)
    return {'result': result, 'count': len(data)}
```

### Flask 中使用 Celery

```python
# app.py
from flask import Flask, request, jsonify
from celery import Celery
from celery_config import celery_app, send_email, process_data

app = Flask(__name__)

# 启动 Celery worker
# celery -A app.celery_app worker --loglevel=info

# 触发异步任务
@app.route('/send-email', methods=['POST'])
def send_email_task():
    data = request.get_json()
    
    # 异步执行
    task = send_email.delay(data['to'], data['subject'], data['body'])
    
    return jsonify({
        'task_id': task.id,
        'status': '任务已提交'
    })

# 检查任务状态
@app.route('/task/<task_id>')
def task_status(task_id):
    task = celery_app.AsyncResult(task_id)
    
    return jsonify({
        'task_id': task.id,
        'status': task.state,
        'result': task.result if task.ready() else None
    })

# 批量处理
@app.route('/process', methods=['POST'])
def process_task():
    data = request.get_json().get('numbers', [])
    
    task = process_data.delay(data)
    
    return jsonify({
        'task_id': task.id,
        'status': '任务已提交'
    })

if __name__ == '__main__':
    app.run(debug=True)
```

---

## 6.4 错误处理

### 自定义错误页面

```python
from flask import render_template

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', code=404, message='页面未找到'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', code=500, message='服务器内部错误'), 500

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('error.html', code=403, message='禁止访问'), 403
```

### API 错误响应

```python
from flask import jsonify

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not Found',
        'message': '请求的资源不存在',
        'status': 404
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal Server Error',
        'message': '服务器内部错误',
        'status': 500
    }), 500

# 自定义 API 异常
class APIException(Exception):
    def __init__(self, message, status_code=400):
        super().__init__()
        self.message = message
        self.status_code = status_code

@app.errorhandler(APIException)
def handle_api_exception(error):
    return jsonify({
        'error': error.message
    }), error.status_code
```

---

## 6.5 日志记录

```python
import logging
from flask import Flask

app = Flask(__name__)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

@app.route('/')
def index():
    logger.info('首页被访问')
    return 'Hello'

@app.route('/error')
def error_route():
    logger.error('发生错误')
    raise Exception('测试错误')
```

---

## 6.6 部署选项

### 使用 Gunicorn

```bash
pip install gunicorn

# 运行
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 使用 Docker

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
    restart: always
```

---

## 本章总结

### 学到的技能

| 技能 | 说明 |
|------|------|
| JWT 认证 | Token 身份验证 |
| Flask-Caching | 页面和数据缓存 |
| Celery | 异步任务队列 |
| 错误处理 | 自定义错误页面 |
| 日志 | 应用日志记录 |
| 部署 | Gunicorn、Docker |

### 下一步

在 [第 7 章](./07-FastAPI 入门.md) 中，我们将学习 FastAPI 框架。

---

[← 上一章](./05-Flask 进阶.md) | [下一章 →](./07-FastAPI 入门.md)