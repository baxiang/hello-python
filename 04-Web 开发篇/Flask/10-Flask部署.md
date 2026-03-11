# Flask 部署

掌握 Flask 应用的生产环境部署。

---

## 1. 生产服务器

### 1.1 Gunicorn

```bash
pip install gunicorn

# 运行
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# 参数说明
# -w: worker 数量
# -b: 绑定地址
# app:app: 应用模块和实例
```

### 1.2 配置文件

```python
# gunicorn_config.py
bind = '0.0.0.0:5000'
workers = 4
worker_class = 'sync'
timeout = 120
keepalive = 5
accesslog = 'logs/access.log'
errorlog = 'logs/error.log'
loglevel = 'info'
```

运行：

```bash
gunicorn -c gunicorn_config.py app:app
```

---

## 2. Docker 部署

### 2.1 Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

### 2.2 docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=postgresql://user:pass@db:5432/app
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: app

  redis:
    image: redis:7
```

---

## 3. Nginx 配置

### 3.1 安装 Nginx

```bash
sudo apt install nginx
```

### 3.2 配置文件

```nginx
# /etc/nginx/sites-available/flask_app

upstream flask_app {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://flask_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /var/www/app/static;
    }
}
```

---

## 4. 完整部署

### 4.1 项目结构

```
project/
├── app/
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── nginx.conf
```

### 4.2 部署步骤

```bash
# 1. 构建镜像
docker-compose build

# 2. 启动服务
docker-compose up -d

# 3. 查看日志
docker-compose logs -f

# 4. 停止服务
docker-compose down
```

---

## 总结

| 知识点 | 说明 |
|---------|------|
| Gunicorn | WSGI 服务器 |
| Docker | 容器化 |
| Nginx | 反向代理 |
| docker-compose | 编排工具 |

---

[← 上一章](./Flask/09-Flask异步任务Celery.md) | [返回目录](../README.md)