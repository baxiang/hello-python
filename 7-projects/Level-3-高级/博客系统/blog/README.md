# 博客系统

基于 FastAPI 的博客 RESTful API。

## 功能

- 用户管理
- 文章 CRUD
- 评论系统
- 密码加密

## 安装

```bash
uv sync
```

## 运行

```bash
uv run uvicorn app.main:app --reload
```

## API

- `POST /api/users` - 创建用户
- `POST /api/posts` - 创建文章
- `GET /api/posts` - 获取文章列表
- `GET /api/posts/{id}` - 获取文章详情