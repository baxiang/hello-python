# FastAPI Demo

FastAPI Web 框架示例项目，包含路由、模型、服务等内容。

## 安装

```bash
uv sync
```

## 运行

```bash
uv run python -c "from app import __version__; print(f'版本: {__version__}')"
```

## 启动服务

```bash
uv run uvicorn app.main:app --reload
```