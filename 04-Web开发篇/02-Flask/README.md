# Flask

学习 Flask Web 框架，从入门到实战。

---

## 本篇学习路径

```
知识依赖图：
┌─────────────────────────────────────────────────────────────┐
│                    Flask 学习路径                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   前置：01-Web基础（HTTP 协议、RESTful 设计）                 │
│                                                             │
│   第1章 简介 → 第2章 路由 → 第3章 模板                     │
│       │                  │                 │                │
│       ▼                  ▼                 ▼                │
│   第12章 配置       第15章 命令行      第13章 错误/日志      │
│                                                             │
│   第4章 数据库 → 第5章 表单 → 第6章 文件                   │
│       │                                                      │
│       ▼                                                      │
│   第7章 蓝图 → 第8章 认证 → 第9章 RESTful API              │
│       │                  │                                   │
│       ▼                  ▼                                   │
│   第17章 类视图/信号   第14章 安全专题                        │
│                                                             │
│   第10章 缓存/异步 → 第18章 Flask异步 → 第11章 测试/部署     │
│                                                             │
│   第16章 消息闪现/Session深入（可随时穿插学习）               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**学习建议：**
- **完整学习**：按 1→2→3→12→15→13→4→5→6→7→8→9→17→14→10→18→11→16 顺序
- **快速上手**：1→2→3→4→7→11（最小可用路径）
- **API 开发**：1→2→9→12→13→17→14→11
- **复习者**：直接跳到新增章节（12~18）

---

## 章节导航

### 基础篇

| 章节 | 文件 | 主题 |
|------|------|------|
| 01 | [01-Flask简介与安装.md](./01-Flask简介与安装.md) | Flask 入门、开发服务器 |
| 02 | [02-路由与请求处理.md](./02-路由与请求处理.md) | 路径参数、HTTP方法、请求响应、url_for、session |
| 03 | [03-Jinja2模板引擎.md](./03-Jinja2模板引擎.md) | 模板语法、继承、过滤器 |

### 核心篇

| 章节 | 文件 | 主题 |
|------|------|------|
| 04 | [04-数据库集成.md](./04-数据库集成.md) | SQLAlchemy、CRUD、关系映射 |
| 05 | [05-表单处理.md](./05-表单处理.md) | Flask-WTF、表单验证 |
| 06 | [06-文件上传下载.md](./06-文件上传下载.md) | 文件处理、安全上传 |
| 07 | [07-蓝图Blueprint.md](./07-蓝图Blueprint.md) | 模块化、蓝图组织 |

### 进阶篇

| 章节 | 文件 | 主题 |
|------|------|------|
| 08 | [08-认证授权.md](./08-认证授权.md) | Flask-Login、JWT、权限 |
| 09 | [09-RESTful-API.md](./09-RESTful-API.md) | Flask-RESTful、资源类 |
| 10 | [10-缓存与异步任务.md](./10-缓存与异步任务.md) | Flask-Caching、Celery |
| 11 | [11-测试与部署.md](./11-测试与部署.md) | pytest、Gunicorn、Docker |

### 新增专题篇（对照官方文档补充）

| 章节 | 文件 | 主题 |
|------|------|------|
| 12 | [12-配置管理.md](./12-配置管理.md) | app.config、dotenv、多环境配置、instance folders |
| 13 | [13-错误处理与日志.md](./13-错误处理与日志.md) | errorhandler、JSON API 错误、app.logger、邮件告警 |
| 14 | [14-Flask安全专题.md](./14-Flask安全专题.md) | XSS、CSRF、Security Headers、OWASP Top 10 |
| 15 | [15-Flask命令行.md](./15-Flask命令行.md) | flask run/shell、自定义命令、dotenv |
| 16 | [16-消息闪现与Session深入.md](./16-消息闪现与Session深入.md) | flash()、Flask-Session、服务端 Session |
| 17 | [17-类视图与信号.md](./17-类视图与信号.md) | MethodView、RESTful 类视图、Blinker 信号 |
| 18 | [18-Flask异步支持.md](./18-Flask异步支持.md) | async def 视图、WSGI vs ASGI、gevent |

---

## 示例项目

[flask_demo/](./flask_demo/) - Flask 实践项目

---

## 配套资源

- [Flask 官方文档](https://flask.palletsprojects.com/)
- [Flask Tutorial](https://flask.palletsprojects.com/en/stable/tutorial/)
- [SQLAlchemy 文档](https://docs.sqlalchemy.org/)
- [WTForms 文档](https://wtforms.readthedocs.io/)
- [Werkzeug 文档](https://werkzeug.palletsprojects.com/)
- [Jinja 文档](https://jinja.palletsprojects.com/)
