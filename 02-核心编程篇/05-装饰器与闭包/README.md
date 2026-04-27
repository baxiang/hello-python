# 装饰器与闭包

本章讲解 Python 装饰器与闭包的完整知识体系，从函数是一等公民到生产环境装饰器最佳实践。

---

## 快速开始

```bash
# 进入示例项目
cd decorators_demo

# 安装依赖
uv sync

# 启动 Web 服务（ch03-ch06 章节演示）
uv run uvicorn app.main:app --reload
# → 访问 http://localhost:8000/docs 查看交互式 API 文档

# 运行测试（所有章节验证）
uv run pytest -v
```

---

## 知识地图

```
函数是一等公民 ──→ 闭包与作用域 ──→ 装饰器核心原理 ──→ 带参数装饰器
      ↓                   ↓                  ↓                    ↓
  函数传递能力       LEGB + nonlocal    @语法 + wraps      三层嵌套 + 工厂
  Callable 类型      闭包内存模型       定义时 vs 调用时    装饰器兼容性
        │                   │                  │                    │
        └───────────────────┴──────────────────┴────────────────────┘
                                 ↓
                     functools 标准装饰器 ──→ 装饰器高级用法 ──→ 边界情况与调试
                                 ↓                        ↓                  ↓
                             lru_cache / cache         ParamSpec         叠加顺序问题
                             cached_property           async 装饰器      闭包陷阱排查
                             singledispatch            wrapt 库          调试工具函数
                             partial                   调试技巧          生产排查清单
```

---

## 章节导航

| 章节 | 文件 | 主题 | 验证方式 |
|------|------|------|---------|
| 01 | [函数是一等公民](./01-函数是一等公民.md) | 函数传递 + Callable | `pytest tests/test_ch01.py` |
| 02 | [闭包与作用域链](./02-闭包与作用域链.md) | LEGB + nonlocal + 闭包原理 | `pytest tests/test_ch02.py` |
| 03 | [装饰器核心原理](./03-装饰器核心原理.md) | @语法 + wraps + 执行时序 | `curl localhost:8000/api/v1/demo` |
| 04 | [带参数装饰器](./04-带参数装饰器与装饰器工厂.md) | 三层嵌套 + 工厂模式 | `curl localhost:8000/api/v1/auth` |
| 05 | [functools 标准装饰器](./05-functools 标准装饰器.md) | lru_cache/cached_property | `curl localhost:8000/api/v1/cache` |
| 06 | [装饰器高级用法](./06-装饰器高级用法与最佳实践.md) | async + 类型精化 + wrapt | `curl localhost:8000/api/v1/async` |
| 07 | [边界情况与调试实战](./07-装饰器边界情况与调试实战.md) | 叠加顺序 + 闭包陷阱 + 调试工具 | `curl localhost:8000/api/v1/debug` |

---

## API 端点一览

启动服务后，以下端点可用：

| 端点 | 章节 | 说明 |
|------|------|------|
| `GET /api/v1/demo/hello` | ch03 | 日志 + 计时装饰器演示 |
| `GET /api/v1/demo/wraps-comparison` | ch03 | @wraps 对比 |
| `GET /api/v1/auth/profile` | ch04 | 权限验证（user 角色） |
| `DELETE /api/v1/auth/users/:id` | ch04 | 权限验证（admin 角色） |
| `POST /api/v1/retry/fetch` | ch04 | 重试机制演示 |
| `GET /api/v1/cache/fibonacci/:n` | ch05 | lru_cache 性能对比 |
| `GET /api/v1/cache/config/:key` | ch05 | 缓存命中率监控 |
| `GET /api/v1/async/call/{delay}` | ch06 | 异步装饰器 |
| `GET /api/v1/async/sync/:delay` | ch06 | 同步操作对比 |
| `GET /api/v1/async/count-calls` | ch06 | 类装饰器计数 |
| `GET /api/v1/debug/order-conflict` | ch07 | 装饰器叠加顺序 |
| `GET /api/v1/debug/closure-trap` | ch07 | 循环变量陷阱 |
| `GET /api/v1/debug/async-await-missing` | ch07 | async await 遗漏 |
| `GET /api/v1/debug/signature-lost` | ch07 | 函数签名丢失 |
| `GET /api/v1/debug/stack-swallowed` | ch07 | 异常栈被吞掉 |

---

## 装饰器最佳实践清单

1. **始终使用 @wraps** — 保留原函数元信息
2. **一个装饰器只做一件事** — 保持简单和可组合
3. **用 ParamSpec 保留类型签名** — 让 IDE 提供更好的提示
4. **async 装饰器记得 await** — 否则返回 coroutine 而非结果
5. **优先用 functools 标准装饰器** — lru_cache, singledispatch 等
6. **装饰器在定义时执行** — 不是调用时
