# GitHub Trending 热榜追踪工具

命令行工具，爬取 GitHub Trending 页面，获取热门项目数据。

## 功能

- 获取 GitHub 热门项目列表
- 按编程语言过滤（python, javascript, go 等）
- 按时间范围筛选（今日、本周、本月）
- 支持多种输出格式（终端、JSON、CSV）

## 安装

```bash
uv sync
```

## 使用

```bash
# 今日热门（默认）
uv run python -m app.main

# Python 语言，本周热门
uv run python -m app.main --language python --range weekly

# 输出 JSON 文件
uv run python -m app.main --output json --file trending.json

# 输出 CSV 文件，限制 10 个
uv run python -m app.main --output csv --limit 10

# 显示帮助
uv run python -m app.main --help
```

## 测试

```bash
uv run pytest -v
uv run pytest --cov=app
```

## ⚠️ 爬虫伦理

本项目仅用于学习目的，使用时请注意：

- 遵守 GitHub robots.txt 协议
- 添加请求延迟，避免高频访问
- 不用于商业数据采集
- 尊重网站服务器资源

## 技术栈

- requests - HTTP 请求
- beautifulsoup4 - HTML 解析
- argparse - 命令行参数