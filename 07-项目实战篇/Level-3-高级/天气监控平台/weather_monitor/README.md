# 天气监控平台

天气数据采集与分析 API 服务。

## 功能

- 天气数据采集
- 城市管理
- 数据存储与查询
- 监控告警

## 安装

```bash
uv sync
```

## 运行

```bash
uv run uvicorn app.main:app --reload
```

## API 文档

启动后访问 http://localhost:8000/docs