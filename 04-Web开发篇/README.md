# Web 开发篇

学习 Python Web 开发技能，从基础的 Flask 到现代的 FastAPI。

---

## 学习路径

```
Flask 基础 (同步、简单)
    ↓  适合初学者，快速上手
FastAPI 进阶 (异步、类型安全、自动文档)
    ↓  产业级选择，生产就绪
```

---

## 第一阶段：Flask 基础

Flask 是轻量级 Web 框架，适合初学者快速理解 Web 开发核心概念。

| 章节 | 文件 | 主题 | 难度 |
|------|------|------|------|
| 01 | [Flask/01-Flask简介与安装.md](./Flask/01-Flask简介与安装.md) | Flask 入门、开发服务器 | ⭐ |
| 02 | [Flask/02-路由与请求处理.md](./Flask/02-路由与请求处理.md) | 路由、请求对象、响应构建 | ⭐ |
| 03 | [Flask/03-Jinja2模板引擎.md](./Flask/03-Jinja2模板引擎.md) | 模板渲染、变量、控制结构 | ⭐ |
| 04 | [Flask/04-数据库集成.md](./Flask/04-数据库集成.md) | SQLAlchemy、CRUD、迁移 | ⭐⭐ |
| 05 | [Flask/05-表单处理.md](./Flask/05-表单处理.md) | Flask-WTF、表单验证 | ⭐⭐ |
| 06 | [Flask/06-文件上传下载.md](./Flask/06-文件上传下载.md) | 文件上传、下载 | ⭐⭐ |
| 07 | [Flask/07-蓝图Blueprint.md](./Flask/07-蓝图Blueprint.md) | 蓝图、应用工厂模式 | ⭐⭐ |
| 08 | [Flask/08-认证授权.md](./Flask/08-认证授权.md) | Flask-Login、JWT、权限控制 | ⭐⭐⭐ |
| 09 | [Flask/09-RESTful-API.md](./Flask/09-RESTful-API.md) | Flask-RESTful、资源类 | ⭐⭐⭐ |
| 10 | [Flask/10-缓存与异步任务.md](./Flask/10-缓存与异步任务.md) | Flask-Caching、Celery | ⭐⭐⭐ |
| 11 | [Flask/11-测试与部署.md](./Flask/11-测试与部署.md) | pytest、Gunicorn、Docker | ⭐⭐⭐ |

**Flask 适用场景：**
- 快速原型开发
- 小型Web应用
- 学习Web开发基础

---

## 第二阶段：FastAPI 进阶

FastAPI 是现代高性能 Web 框架，支持异步、自动文档、类型检查，是产业级首选。

| 章节 | 文件 | 主题 | 难度 |
|------|------|------|------|
| 01 | [FastAPI/01-FastAPI入门.md](./FastAPI/01-FastAPI入门.md) | FastAPI 入门、路径操作、参数 | ⭐⭐ |
| 02 | [FastAPI/02-Pydantic模型.md](./FastAPI/02-Pydantic模型.md) | 请求体模型、字段验证器 | ⭐⭐ |
| 03 | [FastAPI/03-依赖注入.md](./FastAPI/03-依赖注入.md) | Depends、认证依赖 | ⭐⭐⭐ |
| 04 | [FastAPI/04-数据库集成.md](./FastAPI/04-数据库集成.md) | SQLAlchemy 异步、CRUD | ⭐⭐⭐ |
| 05 | [FastAPI/05-认证授权.md](./FastAPI/05-认证授权.md) | OAuth2、JWT Token | ⭐⭐⭐ |
| 06 | [FastAPI/06-中间件.md](./FastAPI/06-中间件.md) | 中间件、CORS | ⭐⭐ |
| 07 | [FastAPI/07-错误处理.md](./FastAPI/07-错误处理.md) | 异常处理、自定义错误 | ⭐⭐ |
| 08 | [FastAPI/08-WebSocket.md](./FastAPI/08-WebSocket.md) | WebSocket 端点、连接管理 | ⭐⭐⭐ |
| 09 | [FastAPI/09-后台任务.md](./FastAPI/09-后台任务.md) | BackgroundTasks、异步任务 | ⭐⭐⭐ |
| 10 | [FastAPI/10-测试与部署.md](./FastAPI/10-测试与部署.md) | pytest、Docker、部署 | ⭐⭐⭐ |

**FastAPI 适用场景：**
- 生产环境 Web API
- 微服务架构
- 高并发异步应用
- 机器学习服务部署

---

## Flask vs FastAPI 对比

| 特性 | Flask | FastAPI |
|------|-------|---------|
| **性能** | 同步，中等 | 异步，高性能 ⚡ |
| **类型检查** | 无 | 自动类型检查 ✅ |
| **API文档** | 需手动编写 | 自动生成（OpenAPI）✅ |
| **学习曲线** | 平缓 ✅ | 中等 |
| **异步支持** | 需要 extension | 原生支持 ✅ |
| **生产就绪** | 需要 extension | 开箱即用 ✅ |
| **数据验证** | 需手动 | Pydantic自动 ✅ |
| **依赖注入** | 无 | 内置 ✅ |

---

## 学习建议

### 初学者路径
1. **先学 Flask** - 理解 Web 开发基础概念（路由、请求、响应、模板）
2. **完成一个小项目** - 如博客系统、待办事项管理
3. **学习 FastAPI** - 升级到现代工具链

### 有经验者路径
1. **直接学 FastAPI** - 如果已有其他Web框架经验
2. **对比学习** - 理解 Flask 的简洁 vs FastAPI 的强大
3. **项目驱动** - 用 FastAPI 完成一个完整项目

### 项目实战建议
- Flask 项目：适合快速原型、小型应用
- FastAPI 项目：适合生产环境、微服务、高性能API

---

## 技术栈对比

### Flask 技术栈
```python
# requirements.txt
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.0.5
Flask-Login==0.6.3
Flask-WTF==1.2.1
```

### FastAPI 技术栈
```python
# pyproject.toml
[project]
dependencies = [
    "fastapi>=0.109.0",
    "uvicorn>=0.27.0",
    "sqlalchemy>=2.0.0",
    "pydantic>=2.0.0",
]
```

---

## 常见问题

### Q: 应该先学哪个？
**A:** 初学者先学Flask，有经验者直接学FastAPI。

### Q: FastAPI 完全替代 Flask 吗？
**A:** 不是。Flask适合小型项目和快速原型，FastAPI适合生产环境API。

### Q: 可以在项目中混用吗？
**A:** 不建议。选择一个框架深入使用。

### Q: 性能差距大吗？
**A:** FastAPI异步性能明显更高，适合高并发场景。

---

## 下一步

1. **选择学习路径**（Flask优先或FastAPI直接）
2. **按章节学习**（不要跳章）
3. **完成项目实战**（07-项目实战篇有相关项目）

推荐起始：**Flask/01-Flask简介与安装.md** 或 **FastAPI/01-FastAPI入门.md**