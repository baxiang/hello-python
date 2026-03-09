# 第七篇 - 服务端编程篇

通过 6 章内容，系统学习 Python Web 服务端开发，从 HTTP 协议基础到 Flask、FastAPI 两大主流框架，最后通过 3 个完整项目实战综合运用。

---

## 篇章导航

| 章节 | 文件 | 主题 | 核心内容 |
|------|------|------|---------|
| 第 24 章 | [24-Web 基础.md](./24-Web 基础.md) | Web 基础 | HTTP 协议、URL 路由、Cookie/Session、RESTful API 设计 |
| 第 25 章 | [25-Flask 快速上手.md](./25-Flask 快速上手.md) | Flask 入门 | 第一个 Flask 应用、路由、请求/响应处理 |
| 第 26 章 | [26-Flask 进阶.md](./26-Flask 进阶.md) | Flask 进阶 | Jinja2 模板、蓝图、数据库、用户认证 |
| 第 27 章 | [27-Flask 高级.md](./27-Flask 高级.md) | Flask 高级 | RESTful API、JWT、缓存、异步任务、部署 |
| 第 28 章 | [28-FastAPI.md](./28-FastAPI.md) | FastAPI 详解 | Pydantic 验证、依赖注入、异步、WebSocket |
| 第 29 章 | [29-服务端项目实战.md](./29-服务端项目实战.md) | 项目实战 | 博客 API、待办 API、聊天室 |

---

## 学习路线

```
┌─────────────────────────────────────────────────────────────────┐
│              第七篇：服务端编程篇 学习路线                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  基础理论 → Flask 框架 (同步) → FastAPI 框架 (异步) → 实战项目   │
│                                                                 │
│  第 24 章      第 25-27 章       第 28 章        第 29 章         │
│  Web 基础     Flask 全三章     FastAPI 详解    3 个完整项目      │
│                                                                 │
│  ┌─────────┐  ┌──────────┐  ┌──────────┐  ┌─────────────────┐ │
│  │ HTTP    │  │ Flask    │  │ FastAPI  │  │ 博客 API        │ │
│  │ RESTful │→ │ Jinja2   │→ │ Pydantic │→ │ 待办 API        │ │
│  │ JWT     │  │ 蓝图     │  │ 依赖注入 │  │ 聊天室          │ │
│  │         │  │ SQLAlchemy│  │ WebSocket│  │                 │ │
│  └─────────┘  └──────────┘  └──────────┘  └─────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 技术对比：Flask vs FastAPI

| 特性 | Flask | FastAPI |
|------|-------|---------|
| 类型 | 同步框架 | 异步框架 (async/await) |
| 性能 | 中等 | 高 (Starlette 基础) |
| 模板 | Jinja2 (强大) | 支持较弱 (专注 API) |
| 数据验证 | 手动 | Pydantic 自动验证 |
| API 文档 | 需手动配置 | 自动生成 Swagger/ReDoc |
| 类型检查 | 无 | 基于类型提示 |
| WebSocket | 需扩展 | 原生支持 |
| 学习曲线 | 平缓 | 需要理解异步 |
| 适用场景 | 传统网站、SSR 应用 | REST API、微服务 |

**选择建议：**
- 传统网站、需要模板渲染 → Flask
- REST API、微服务、高性能需求 → FastAPI
- 团队熟悉 Flask、项目稳定 → Flask
- 新项目、AI 服务集成 → FastAPI

---

## 环境准备

开始前请确保已安装以下依赖：

```bash
# 创建项目
uv init web-learning
cd web-learning

# Flask 相关（第 25-27 章）
uv add flask flask-sqlalchemy flask-login flask-wtf flask-migrate
uv add flask-caching celery redis
uv add pyjwt python-dotenv

# FastAPI 相关（第 28 章）
uv add fastapi uvicorn[standard]
uv add sqlalchemy[asyncio] aiosqlite
uv add python-jose[cryptography] passlib[bcrypt]
uv add python-multipart

# 测试工具
uv add pytest pytest-flask pytest-asyncio httpx
```

---

## 各章前置依赖

```
第 24 章 (Web 基础)
└── 无依赖，可直接学习

第 25 章 (Flask 快速上手)
└── 第 24 章 (Web 基础)
    └── 建议先了解 HTTP 基础

第 26 章 (Flask 进阶)
└── 第 25 章 (Flask 快速上手)
    ├── Jinja2 模板
    ├── SQLAlchemy ORM (第 12 章文件操作)
    └── 表单处理

第 27 章 (Flask 高级)
└── 第 26 章 (Flask 进阶)
    ├── REST API 设计
    ├── JWT 认证
    ├── Celery 异步任务
    └── 部署配置

第 28 章 (FastAPI)
├── 第 24 章 (Web 基础)
├── 第 21 章 (类型提示) ← 重要！
└── 第 23 章 (asyncio 高级编程) ← 建议先学

第 29 章 (项目实战)
├── 第 27 章 (Flask 高级)
└── 第 28 章 (FastAPI)
```

---

## 学完本篇你能做什么？

完成本篇章学习后，你将能够：

✅ **理解 Web 开发核心原理**
   - HTTP 协议、请求/响应 cycle、状态码
   - RESTful API 设计规范
   - 认证授权机制 (Session/JWT/OAuth2)

✅ **使用 Flask 开发 Web 应用**
   - 搭建完整的网站 (模板 + 路由 + 数据库)
   - 用户注册/登录系统
   - 文件上传、缓存优化
   - 使用 Celery 处理异步任务

✅ **使用 FastAPI 构建高性能 API**
   - 自动数据验证 (Pydantic)
   - 自动生成 API 文档
   - 异步数据库操作
   - WebSocket 实时通信

✅ **独立开发服务端项目**
   - 博客系统 API
   - 待办事项管理 API
   - 实时聊天室

---

[← 上一篇：第 23 章 asyncio 高级编程](../23-asyncio 高级编程.md) |
[→ 下一篇：第 30 章 机器学习基础](../08-机器学习篇/30-机器学习基础.md)
