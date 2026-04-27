# Web 开发篇

学习 Python Web 开发技能，掌握 Flask 和 FastAPI 框架。

---

## 本篇学习路径

```
知识依赖图：
┌─────────────────────────────────────────────────────────────┐
│                    Web 开发篇学习路径                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   前置：02-核心编程篇（函数、类、异常）                        │
│         03-高级语法篇（模块与包）                             │
│                                                             │
│   第0章 Web 基础（HTTP 协议、RESTful 设计）                   │
│   ├── 前置：无 ← 本章起点                                    │
│   └── 输出：理解 HTTP 请求/响应、状态码、RESTful 原则        │
│           │                                                 │
│           ↓                                                 │
│   Flask 路径（传统 Web 开发）                                 │
│   ├── 第1章 Flask 简介 → 第2章 路由 → 第3章 模板            │
│   ├── 第4章 数据库 → 第5章 表单 → 第6章 文件                │
│   ├── 第7章 蓝图 → 第8章 认证 → 第9章 RESTful API           │
│   └── 第10章 缓存/异步 → 第11章 测试/部署                   │
│                                                             │
│   FastAPI 路径（现代 API 开发）                               │
│   ├── 第1章 入门 → 第2章 Pydantic → 第3章 依赖注入          │
│   ├── 第4章 数据库 → 第5章 认证 → 第6章 中间件              │
│   └── 第7章 错误处理 → 第8章 WebSocket → 第9章 后台任务     │
│                                                             │
│   Flask 路径 与 FastAPI 路径 可并行学习                      │
│                                                             │
│   关键路径：HTTP基础 → Flask 完整链路 → FastAPI 完整链路     │
│   只学 API 开发：HTTP基础 → FastAPI 路径                     │
│   只学 Web 全栈：HTTP基础 → Flask 路径                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**学习建议：**
- **完整学习**：Web 基础 → Flask 全 11 章 → FastAPI 全 12 章 → 安全专题
- **只学 API 开发**：Web 基础 → FastAPI 路径 → 分页与过滤 → API 文档生成
- **只学 Web 全栈**：Web 基础 → Flask 路径 → 再学 FastAPI
- **复习者**：直接跳到实战项目章节，查漏补缺
- **安全审计**：完成基础学习后，阅读安全专题查漏补缺

---

## Flask 模块

| 章节 | 文件 | 主题 |
|------|------|------|
| 01 | [01-Flask/01-Flask简介与安装.md](./01-Flask/01-Flask简介与安装.md) | Flask 入门、开发服务器 |
| 02 | [01-Flask/02-路由与请求处理.md](./01-Flask/02-路由与请求处理.md) | 路由、请求对象、响应构建 |
| 03 | [01-Flask/03-Jinja2模板引擎.md](./01-Flask/03-Jinja2模板引擎.md) | 模板渲染、变量、控制结构 |
| 04 | [01-Flask/04-数据库集成.md](./01-Flask/04-数据库集成.md) | SQLAlchemy、CRUD、迁移 |
| 05 | [01-Flask/05-表单处理.md](./01-Flask/05-表单处理.md) | Flask-WTF、表单验证 |
| 06 | [01-Flask/06-文件上传下载.md](./01-Flask/06-文件上传下载.md) | 文件上传、下载 |
| 07 | [01-Flask/07-蓝图Blueprint.md](./01-Flask/07-蓝图Blueprint.md) | 蓝图、应用工厂模式 |
| 08 | [01-Flask/08-认证授权.md](./01-Flask/08-认证授权.md) | Flask-Login、JWT、权限控制 |
| 09 | [01-Flask/09-RESTful-API.md](./01-Flask/09-RESTful-API.md) | Flask-RESTful、资源类 |
| 10 | [01-Flask/10-缓存与异步任务.md](./01-Flask/10-缓存与异步任务.md) | Flask-Caching、Celery |
| 11 | [01-Flask/11-测试与部署.md](./01-Flask/11-测试与部署.md) | pytest、Gunicorn、Docker |

---

## Web 基础

| 章节 | 文件 | 主题 |
|------|------|------|
| 00 | [00-Web基础.md](./00-Web基础.md) | HTTP 协议、状态码、RESTful 设计原则 |

---

## 专题

| 章节 | 文件 | 主题 |
|------|------|------|
| 安全 | [安全专题.md](./安全专题.md) | XSS、CSRF、SQL 注入、HTTP 安全 Headers |

---

## FastAPI 模块

| 章节 | 文件 | 主题 |
|------|------|------|
| 01 | [02-FastAPI/01-FastAPI入门.md](./02-FastAPI/01-FastAPI入门.md) | FastAPI 入门、路径操作、参数 |
| 02 | [02-FastAPI/02-Pydantic模型.md](./02-FastAPI/02-Pydantic模型.md) | 请求体模型、字段验证器 |
| 03 | [02-FastAPI/03-依赖注入.md](./02-FastAPI/03-依赖注入.md) | Depends、认证依赖 |
| 04 | [02-FastAPI/04-数据库集成.md](./02-FastAPI/04-数据库集成.md) | SQLAlchemy 异步、CRUD |
| 05 | [02-FastAPI/05-认证授权.md](./02-FastAPI/05-认证授权.md) | OAuth2、JWT Token |
| 06 | [02-FastAPI/06-中间件.md](./02-FastAPI/06-中间件.md) | 中间件、CORS |
| 07 | [02-FastAPI/07-错误处理.md](./02-FastAPI/07-错误处理.md) | 异常处理、自定义错误 |
| 08 | [02-FastAPI/08-WebSocket.md](./02-FastAPI/08-WebSocket.md) | WebSocket 端点、连接管理 |
| 09 | [02-FastAPI/09-后台任务.md](./02-FastAPI/09-后台任务.md) | BackgroundTasks、异步任务 |
| 10 | [02-FastAPI/10-测试与部署.md](./02-FastAPI/10-测试与部署.md) | pytest、Docker、部署 |
| 11 | [02-FastAPI/11-分页与过滤.md](./02-FastAPI/11-分页与过滤.md) | 偏移/游标分页、查询过滤、排序 |
| 12 | [02-FastAPI/12-API文档生成.md](./02-FastAPI/12-API文档生成.md) | OpenAPI、Swagger、ReDoc |