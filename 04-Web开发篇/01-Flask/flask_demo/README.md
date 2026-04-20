# cms-api - Flask CMS RESTful API示例项目

前后分离架构的Flask RESTful API示例，覆盖Flask全部知识点。

## 章节知识点覆盖

| 章节 | 模块 | API | 知识点 |
|------|------|-----|--------|
| ch01 | Flask简介 | app/__init__.py | 应用工厂 |
| ch02 | 路由与请求 | api/*.py | HTTP方法 |
| ch03 | Jinja2模板 | templates/optional/ | **传统可选** |
| ch04 | 数据库集成 | models/*.py | SQLAlchemy |
| ch05 | 表单处理 | schemas/*.py | Marshmallow |
| ch06 | 文件上传 | api/files.py | upload/download |
| ch07 | Blueprint | api/__init__.py | 模块化组织 |
| ch08 | 认证授权 | api/auth.py | JWT |
| ch09 | RESTful API | api/articles.py | CRUD |
| ch10 | 缓存异步 | config.py | 缓存配置 |
| ch11 | 测试部署 | tests/*.py | pytest |

## 安装

```bash
cd "04-Web开发篇/01-Flask/flask_demo"
uv sync
```

## 运行

```bash
uv run flask run
```

## 测试

```bash
uv run pytest tests/ -v
```

## API列表

### 认证 (/api/auth)

- POST /register - 用户注册
- POST /login - 用户登录
- POST /refresh - Token刷新

### 用户 (/api/users)

- GET / - 用户列表
- GET /<id> - 用户详情
- GET /me - 当前用户

### 文章 (/api/articles)

- GET / - 文章列表
- GET /<id> - 文章详情
- POST / - 创建文章 (JWT)
- PUT /<id> - 更新文章 (JWT)
- DELETE /<id> - 删除文章 (JWT)

### 文件 (/api/files)

- POST /upload - 上传文件 (JWT)
- GET /<filename> - 下载文件

## 关于Jinja2模板

2026年主流前后分离，模板仅作历史参考。
详见 `app/templates/optional/README.md`