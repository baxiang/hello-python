# Python 标准库示例项目 - 日志分析器

完整的日志分析器项目，覆盖 Python 标准库 8 章知识点。

## 覆盖的知识点

| 章节 | 模块 | 核心功能 |
|-----|-----|---------|
| ch01 | math | sqrt, ceil, floor, pow, log |
| ch02 | random | sample, choice, choices, shuffle |
| ch03 | datetime | strptime, strftime, timedelta, weekday |
| ch04 | pathlib | iterdir, glob, rglob, Path属性 |
| ch05 | json | dump, dumps, load, loads, ensure_ascii |
| ch06 | 文件操作 | read_text, write_text, Path.open |
| ch07 | re | match, search, findall, sub |
| ch08 | pickle | dump, load, 序列化/反序列化 |

## 项目结构

```
toolbox/
├── app/
│   ├── core/
│   │   ├── log_entry.py      # ch03: datetime日志条目
│   │   ├── log_parser.py     # ch06/ch07: 文件解析+正则
│   │   ├── log_filter.py     # ch03/ch04: 时间+路径过滤
│   │   ├── log_stats.py      # ch01/ch02: math+random统计
│   │   ├── log_report.py     # ch05: JSON报告
│   │   ├── log_cache.py      # ch08: pickle缓存
│   │   └── log_scanner.py    # ch04: 目录扫描
│   └── utils/
│       ├── patterns.py       # ch07: 正则模式
│       ├── validators.py     # ch07: 验证器
│       └── helpers.py        # 辅助函数
├── tests/                    # pytest测试套件
├── sample_logs/              # 示例日志文件
└── pyproject.toml
```

## 安装

```bash
uv sync
```

## 使用示例

```python
from app.core import (
    LogEntry, parse_timestamp,
    LogScanner, find_log_files,
    LogParser, parse_log_file,
    LogFilter, filter_by_level,
    LogStats, calculate_mean,
    LogReport, generate_report,
    LogCache, save_cache,
)

# 解析日志文件
parser = LogParser()
entries = parser.parse_file("sample_logs/app.log")

# 按级别过滤
errors = filter_by_level(entries, ["ERROR", "CRITICAL"])

# 生成统计报告
stats = LogStats([e.timestamp.timestamp() for e in entries])
print(f"平均时间: {stats.mean()}")
print(f"标准差: {stats.std_dev()}")

# 生成JSON报告
report = generate_report(entries)
print(report)

# 缓存解析结果
cache = LogCache("cache.pkl")
cache.save(entries)
```

## 运行测试

```bash
uv run pytest tests/ -v
```

## 代码检查

```bash
uv run ruff check .
uv run ruff format .
```

## 模块详情

### LogEntry (datetime)
- 解析多种时间格式
- 格式化输出
- 时间差计算
- 工作日判断

### LogScanner (pathlib)
- 目录遍历
- glob模式匹配
- 递归扫描
- 文件信息获取

### LogStats (math + random)
- 统计计算: mean, std_dev, percentile
- 数学运算: sqrt, ceil, floor
- 随机采样: sample, choice

### LogParser (re + 文件操作)
- 正则匹配日志格式
- 提取IP/邮箱/错误码
- 敏感信息屏蔽

### LogFilter
- 时间范围过滤
- 级别过滤
- 工作日过滤
- 正则模式过滤

### LogReport (json)
- JSON序列化
- 中文支持
- 格式化输出

### LogCache (pickle)
- 序列化缓存
- 安全警告
- 缓存管理