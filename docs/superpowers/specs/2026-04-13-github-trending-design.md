# GitHub Trending 项目设计文档

## 项目概述

**Level-1 入门级项目**：GitHub 热榜追踪 CLI 工具，适合初学者，预计 1-2 天完成。

爬取 `https://github.com/trending` 页面，获取热门项目数据并保存为文件。

## 核心功能

### 输入参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `--language` | 按语言过滤 | `python`, `javascript`, `go`, `all` |
| `--range` | 按时间范围 | `daily`, `weekly`, `monthly` |
| `--output` | 输出格式 | `json`, `csv`, `terminal` |
| `--limit` | 显示数量限制 | `10`, `25`, `50` |

### 输出数据

每个项目包含：
- 项目名称（如 `microsoft/vscode`）
- 项目描述
- 主要语言
- 新增星标数（如 `+1,234 stars today`）
- 总星标数
- Fork 数
- 项目链接

## 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| `requests` | 2.31+ | HTTP 请求获取页面 |
| `beautifulsoup4` | 4.12+ | HTML 解析提取数据 |
| `argparse` | 内置 | 命令行参数解析 |
| `json` | 内置 | JSON 文件存储 |
| `csv` | 内置 | CSV 文件存储 |

## 数据来源

爬取 GitHub Trending 页面：
- `/trending` - 今日热门（默认）
- `/trending/python` - Python 语言筛选
- `/trending?since=weekly` - 本周热门
- `/trending?since=monthly` - 本月热门

## 章节结构

| 章节 | 文件名 | 内容 | 学习目标 |
|------|--------|------|----------|
| 01 | `01-页面请求与分析.md` | HTTP 请求、页面结构分析 | 掌握 requests 发送请求、分析 HTML 结构 |
| 02 | `02-数据解析.md` | BeautifulSoup 解析数据 | 学会 CSS 选择器、提取文本和属性 |
| 03 | `03-命令行参数.md` | argparse 参数设计 | 理解 CLI 参数解析、用户体验设计 |
| 04 | `04-数据存储.md` | JSON/CSV 文件存储 | 掌握文件写入、数据格式化 |
| 05 | `05-完整工具.md` | 整合完整 CLI 工具 | 模块化设计、代码组织 |

## 项目目录结构

```
07-项目实战篇/Level-1-入门级/GitHub热榜追踪/
├── README.md                    # 项目说明
├── 01-页面请求与分析.md          # 第1章文档
├── 02-数据解析.md                # 第2章文档
├── 03-命令行参数.md              # 第3章文档
├── 04-数据存储.md                # 第4章文档
├── 05-完整工具.md                # 第5章文档
└── github_trending/             # 示例代码项目
    ├── pyproject.toml           # 项目配置
    ├── README.md                # 代码说明
    ├── app/
    │   ├── __init__.py
    │   ├── main.py              # CLI 入口（argparse）
    │   ├── fetcher.py           # 页面获取（requests）
    │   ├── parser.py            # 数据解析（BeautifulSoup）
    │   └── storage.py           # 文件存储（json/csv）
    │   └── models.py            # 数据模型（dataclass）
    └── tests/
        ├── __init__.py
        ├── test_fetcher.py      # 测试请求模块
        ├── test_parser.py       # 测试解析模块
        └── test_storage.py      # 测试存储模块
```

## 代码架构

### 数据模型

```python
from dataclasses import dataclass

@dataclass
class TrendingRepo:
    name: str              # owner/repo
    description: str
    language: str
    stars: int             # 总星标数
    forks: int
    stars_today: int       # 今日新增
    url: str               # 项目链接
```

### 模块职责

| 模块 | 职责 | 依赖 |
|------|------|------|
| `fetcher.py` | 发送 HTTP 请求，返回 HTML | requests |
| `parser.py` | 解析 HTML，返回 TrendingRepo 列表 | BeautifulSoup, models |
| `storage.py` | 保存数据到文件 | json, csv, models |
| `main.py` | CLI 入口，参数解析，调用各模块 | argparse, fetcher, parser, storage |

### CLI 使用示例

```bash
# 今日热门，默认显示 25 个
uv run python -m app.main

# Python 语言，本周热门，JSON 输出
uv run python -m app.main --language python --range weekly --output json

# 限制显示 10 个，保存为 CSV
uv run python -m app.main --limit 10 --output csv --file trending.csv

# 显示帮助
uv run python -m app.main --help
```

## 错误处理

| 错误场景 | 处理方式 |
|----------|----------|
| 网络请求失败 | 捕获 `requests.RequestException`，显示错误信息 |
| 页面结构变化 | 解析失败时记录警告，返回空列表 |
| 文件写入失败 | 捕获 `IOError`，显示错误信息 |
| 无效参数 | argparse 自动处理，显示帮助信息 |

## 测试策略

| 模块 | 测试内容 |
|------|----------|
| `test_fetcher.py` | 请求成功、请求失败、User-Agent 设置 |
| `test_parser.py` | HTML 解析、空页面处理、数据提取 |
| `test_storage.py` | JSON 写入、CSV 写入、文件路径处理 |

使用 pytest + mock 避免真实网络请求。

## 学习目标

完成本项目后，学习者将掌握：
1. 使用 requests 发送 HTTP 请求
2. 使用 BeautifulSoup 解析 HTML
3. 设计 CLI 参数提升用户体验
4. 实现数据持久化存储
5. 模块化代码组织

## 法律合规

项目文档需包含：
- 爬虫伦理声明
- robots.txt 重要性说明
- 请求频率限制建议（添加延迟、User-Agent）
- 数据用途限制说明

## 前置知识

- 第 01 章：Python 简介
- 第 05 章：字符串
- 第 08 章：字典
- 正则表达式基础（可选）