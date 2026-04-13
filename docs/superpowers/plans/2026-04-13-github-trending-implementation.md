# GitHub Trending 项目实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 创建 GitHub Trending CLI 工具，爬取热门项目数据并支持多种输出格式。

**Architecture:** 模块化设计，分四个核心模块（fetcher/parser/storage/main），使用 dataclass 定义数据模型，TDD 开发。

**Tech Stack:** requests, beautifulsoup4, argparse, pytest

---

## 文件结构

| 文件 | 职责 |
|------|------|
| `app/__init__.py` | 包初始化 |
| `app/models.py` | TrendingRepo 数据模型 |
| `app/fetcher.py` | HTTP 请求获取页面 |
| `app/parser.py` | HTML 解析提取数据 |
| `app/storage.py` | JSON/CSV 文件存储 |
| `app/main.py` | CLI 入口，argparse 参数 |
| `tests/__init__.py` | 测试包初始化 |
| `tests/test_fetcher.py` | fetcher 模块测试 |
| `tests/test_parser.py` | parser 模块测试 |
| `tests/test_storage.py` | storage 模块测试 |
| `tests/fixtures/sample.html` | 测试用 HTML 样本 |
| `pyproject.toml` | 项目配置 |
| `README.md` | 项目说明 |

---

### Task 1: 创建项目结构和配置

**Files:**
- Create: `07-项目实战篇/Level-1-入门级/GitHub热榜追踪/github_trending/pyproject.toml`
- Create: `07-项目实战篇/Level-1-入门级/GitHub热榜追踪/github_trending/app/__init__.py`
- Create: `07-项目实战篇/Level-1-入门级/GitHub热榜追踪/github_trending/tests/__init__.py`

- [ ] **Step 1: 创建目录结构**

```bash
mkdir -p "07-项目实战篇/Level-1-入门级/GitHub热榜追踪/github_trending/app"
mkdir -p "07-项目实战篇/Level-1-入门级/GitHub热榜追踪/github_trending/tests/fixtures"
```

- [ ] **Step 2: 创建 pyproject.toml**

```toml
[project]
name = "github-trending"
version = "0.1.0"
description = "GitHub Trending 热榜追踪工具"
requires-python = ">=3.11"
dependencies = [
    "requests>=2.31.0",
    "beautifulsoup4>=4.12.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "ruff>=0.1.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["app"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_classes = "Test*"
python_functions = "test_*"
addopts = "-v --tb=short"

[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP", "B", "SIM"]
ignore = ["E501"]
```

- [ ] **Step 3: 创建 app/__init__.py**

```python
"""GitHub Trending 热榜追踪工具"""

__version__ = "0.1.0"
```

- [ ] **Step 4: 创建 tests/__init__.py**

```python
"""GitHub Trending 测试包"""
```

- [ ] **Step 5: 提交**

```bash
git add "07-项目实战篇/Level-1-入门级/GitHub热榜追踪/"
git commit -m "feat: init github trending project structure"
```

---

### Task 2: 创建数据模型

**Files:**
- Create: `app/models.py`
- Test: `tests/test_models.py`

- [ ] **Step 1: 写失败测试**

```python
import pytest
from app.models import TrendingRepo


def test_trending_repo_creation():
    repo = TrendingRepo(
        name="microsoft/vscode",
        description="Visual Studio Code",
        language="TypeScript",
        stars=150000,
        forks=22000,
        stars_today=50,
        url="https://github.com/microsoft/vscode",
    )
    assert repo.name == "microsoft/vscode"
    assert repo.stars == 150000


def test_trending_repo_defaults():
    repo = TrendingRepo(
        name="test/repo",
        description="",
        language="",
        stars=0,
        forks=0,
        stars_today=0,
        url="https://github.com/test/repo",
    )
    assert repo.name == "test/repo"


def test_trending_repo_to_dict():
    repo = TrendingRepo(
        name="python/cpython",
        description="Python interpreter",
        language="Python",
        stars=60000,
        forks=15000,
        stars_today=100,
        url="https://github.com/python/cpython",
    )
    result = repo.to_dict()
    assert result["name"] == "python/cpython"
    assert result["stars"] == 60000
```

- [ ] **Step 2: 运行测试确认失败**

```bash
cd "07-项目实战篇/Level-1-入门级/GitHub热榜追踪/github_trending"
uv sync
uv run pytest tests/test_models.py -v
```

Expected: FAIL - `ModuleNotFoundError: No module named 'app.models'`

- [ ] **Step 3: 实现数据模型**

```python
from dataclasses import dataclass, asdict


@dataclass
class TrendingRepo:
    """GitHub Trending 项目数据模型"""
    name: str
    description: str
    language: str
    stars: int
    forks: int
    stars_today: int
    url: str

    def to_dict(self) -> dict:
        """转换为字典格式"""
        return asdict(self)
```

- [ ] **Step 4: 运行测试确认通过**

```bash
cd "07-项目实战篇/Level-1-入门级/GitHub热榜追踪/github_trending"
uv run pytest tests/test_models.py -v
```

Expected: PASS

- [ ] **Step 5: 提交**

```bash
git add "07-项目实战篇/Level-1-入门级/GitHub热榜追踪/github_trending/"
git commit -m "feat: add TrendingRepo data model"
```

---

### Task 3: 创建 fetcher 模块

**Files:**
- Create: `app/fetcher.py`
- Test: `tests/test_fetcher.py`
- Create: `tests/fixtures/sample.html`

- [ ] **Step 1: 创建测试 HTML 样本文件**

从 GitHub Trending 页面获取结构，创建简化版本用于测试：

```html
<!DOCTYPE html>
<html>
<body>
<article class="Box-row">
  <h2 class="h3 lh-condensed">
    <a href="/microsoft/vscode">
      <span class="text-normal">microsoft /</span>
      vscode
    </a>
  </h2>
  <p class="col-9 d-inline-block Color-fg-muted m-0 pr-4">
    Visual Studio Code - Open Source editor
  </p>
  <span class="d-inline-block ml-0 mr-3">
    <span class="repo-language-color" style="background-color: #3178c6;"></span>
    <span itemprop="programmingLanguage">TypeScript</span>
  </span>
  <a href="/microsoft/vscode/stargazers" class="Link Link--muted d-inline-block mr-3">
    <svg class="octicon octicon-star mr-1" viewBox="0 0 16 16"></svg>
    150,000
  </a>
  <a href="/microsoft/vscode/forks" class="Link Link--muted d-inline-block mr-3">
    <svg class="octicon octicon-repo-forked mr-1"></svg>
    22,000
  </a>
  <span class="float-sm-right">
    <svg class="octicon octicon-star" viewBox="0 0 16 16"></svg>
    1,234 stars today
  </span>
</article>
</body>
</html>
```

- [ ] **Step 2: 写失败测试**

```python
import pytest
from unittest.mock import patch, Mock
from app.fetcher import fetch_trending_page


def test_fetch_trending_page_success():
    with patch("app.fetcher.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<html><body>test</body></html>"
        mock_get.return_value = mock_response
        
        result = fetch_trending_page()
        assert result == "<html><body>test</body></html>"
        mock_get.assert_called_once()


def test_fetch_trending_page_with_language():
    with patch("app.fetcher.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<html>python</html>"
        mock_get.return_value = mock_response
        
        result = fetch_trending_page(language="python")
        assert result == "<html>python</html>"
        
        call_args = mock_get.call_args
        assert "python" in call_args[0][0]


def test_fetch_trending_page_with_range():
    with patch("app.fetcher.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<html>weekly</html>"
        mock_get.return_value = mock_response
        
        result = fetch_trending_page(time_range="weekly")
        assert result == "<html>weekly</html>"
        
        call_args = mock_get.call_args
        assert "weekly" in call_args[0][0]


def test_fetch_trending_page_failure():
    with patch("app.fetcher.requests.get") as mock_get:
        mock_get.side_effect = Exception("Network error")
        
        with pytest.raises(Exception):
            fetch_trending_page()


def test_fetch_trending_page_headers():
    with patch("app.fetcher.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<html></html>"
        mock_get.return_value = mock_response
        
        fetch_trending_page()
        
        call_kwargs = mock_get.call_args[1]
        assert "headers" in call_kwargs
        assert "User-Agent" in call_kwargs["headers"]
```

- [ ] **Step 3: 运行测试确认失败**

```bash
cd "07-项目实战篇/Level-1-入门级/GitHub热榜追踪/github_trending"
uv run pytest tests/test_fetcher.py -v
```

Expected: FAIL - `ModuleNotFoundError: No module named 'app.fetcher'`

- [ ] **Step 4: 实现 fetcher 模块**

```python
import requests

BASE_URL = "https://github.com/trending"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}


def fetch_trending_page(
    language: str | None = None,
    time_range: str = "daily",
) -> str:
    """
    获取 GitHub Trending 页面 HTML
    
    Args:
        language: 编程语言过滤（如 python, javascript）
        time_range: 时间范围（daily, weekly, monthly）
    
    Returns:
        页面 HTML 内容
    
    Raises:
        requests.RequestException: 网络请求失败
    """
    url = BASE_URL
    
    if language:
        url = f"{BASE_URL}/{language}"
    
    params = {}
    if time_range != "daily":
        params["since"] = time_range
    
    response = requests.get(url, headers=HEADERS, params=params, timeout=30)
    response.raise_for_status()
    
    return response.text
```

- [ ] **Step 5: 运行测试确认通过**

```bash
cd "07-项目实战篇/Level-1-入门级/GitHub热榜追踪/github_trending"
uv run pytest tests/test_fetcher.py -v
```

Expected: PASS

- [ ] **Step 6: 提交**

```bash
git add "07-项目实战篇/Level-1-入门级/GitHub热榜追踪/github_trending/"
git commit -m "feat: add fetcher module for HTTP requests"
```

---

### Task 4: 创建 parser 模块

**Files:**
- Create: `app/parser.py`
- Test: `tests/test_parser.py`
- Modify: `tests/fixtures/sample.html`

- [ ] **Step 1: 更新测试 HTML 样本，包含多个项目**

```html
<!DOCTYPE html>
<html>
<body>
<article class="Box-row">
  <h2 class="h3 lh-condensed">
    <a href="/microsoft/vscode">
      <span class="text-normal">microsoft /</span>
      vscode
    </a>
  </h2>
  <p class="col-9 d-inline-block Color-fg-muted m-0 pr-4">
    Visual Studio Code - Open Source editor
  </p>
  <span class="d-inline-block ml-0 mr-3">
    <span itemprop="programmingLanguage">TypeScript</span>
  </span>
  <a href="/microsoft/vscode/stargazers" class="Link Link--muted d-inline-block mr-3">
    150,000
  </a>
  <a href="/microsoft/vscode/network/members" class="Link Link--muted d-inline-block mr-3">
    22,000
  </a>
  <span class="float-sm-right">
    1,234 stars today
  </span>
</article>
<article class="Box-row">
  <h2 class="h3 lh-condensed">
    <a href="/python/cpython">
      <span class="text-normal">python /</span>
      cpython
    </a>
  </h2>
  <p class="col-9 d-inline-block Color-fg-muted m-0 pr-4">
    The Python programming language
  </p>
  <span class="d-inline-block ml-0 mr-3">
    <span itemprop="programmingLanguage">Python</span>
  </span>
  <a href="/python/cpython/stargazers" class="Link Link--muted d-inline-block mr-3">
    60,000
  </a>
  <a href="/python/cpython/network/members" class="Link Link--muted d-inline-block mr-3">
    15,000
  </a>
  <span class="float-sm-right">
    500 stars today
  </span>
</article>
</body>
</html>
```

- [ ] **Step 2: 写失败测试**

```python
import pytest
from pathlib import Path
from app.parser import parse_trending_page
from app.models import TrendingRepo


@pytest.fixture
def sample_html():
    return Path("tests/fixtures/sample.html").read_text()


def test_parse_trending_page_returns_list(sample_html):
    result = parse_trending_page(sample_html)
    assert isinstance(result, list)


def test_parse_trending_page_extract_repos(sample_html):
    result = parse_trending_page(sample_html)
    assert len(result) == 2


def test_parse_trending_page_repo_data(sample_html):
    result = parse_trending_page(sample_html)
    repo = result[0]
    
    assert isinstance(repo, TrendingRepo)
    assert repo.name == "microsoft/vscode"
    assert "Visual Studio Code" in repo.description
    assert repo.language == "TypeScript"


def test_parse_trending_page_stars(sample_html):
    result = parse_trending_page(sample_html)
    repo = result[0]
    
    assert repo.stars == 150000
    assert repo.stars_today == 1234


def test_parse_trending_page_url(sample_html):
    result = parse_trending_page(sample_html)
    repo = result[0]
    
    assert repo.url == "https://github.com/microsoft/vscode"


def test_parse_empty_page():
    result = parse_trending_page("<html><body></body></html>")
    assert result == []


def test_parse_limit(sample_html):
    result = parse_trending_page(sample_html, limit=1)
    assert len(result) == 1
```

- [ ] **Step 3: 运行测试确认失败**

```bash
cd "07-项目实战篇/Level-1-入门级/GitHub热榜追踪/github_trending"
uv run pytest tests/test_parser.py -v
```

Expected: FAIL - `ModuleNotFoundError: No module named 'app.parser'`

- [ ] **Step 4: 实现 parser 模块**

```python
import re
from bs4 import BeautifulSoup
from app.models import TrendingRepo


def parse_trending_page(html: str, limit: int | None = None) -> list[TrendingRepo]:
    """
    解析 GitHub Trending 页面 HTML
    
    Args:
        html: 页面 HTML 内容
        limit: 返回项目数量限制
    
    Returns:
        TrendingRepo 列表
    """
    soup = BeautifulSoup(html, "html.parser")
    articles = soup.select("article.Box-row")
    
    repos = []
    for article in articles[:limit] if limit else articles:
        repo = _parse_repo_article(article)
        if repo:
            repos.append(repo)
    
    return repos


def _parse_repo_article(article) -> TrendingRepo | None:
    """解析单个项目 article 元素"""
    try:
        name = _extract_name(article)
        description = _extract_description(article)
        language = _extract_language(article)
        stars = _extract_stars(article)
        forks = _extract_forks(article)
        stars_today = _extract_stars_today(article)
        url = _extract_url(article)
        
        return TrendingRepo(
            name=name,
            description=description,
            language=language,
            stars=stars,
            forks=forks,
            stars_today=stars_today,
            url=url,
        )
    except Exception:
        return None


def _extract_name(article) -> str:
    """提取项目名称"""
    h2 = article.select_one("h2.h3.lh-condensed")
    if not h2:
        return ""
    
    link = h2.select_one("a")
    if not link:
        return ""
    
    href = link.get("href", "")
    return href.strip("/")


def _extract_description(article) -> str:
    """提取项目描述"""
    p = article.select_one("p.col-9")
    if not p:
        return ""
    return p.get_text(strip=True)


def _extract_language(article) -> str:
    """提取编程语言"""
    span = article.select_one("span[itemprop='programmingLanguage']")
    if not span:
        return ""
    return span.get_text(strip=True)


def _extract_stars(article) -> int:
    """提取总星标数"""
    link = article.select_one("a.Link--muted[href*='stargazers']")
    if not link:
        return 0
    text = link.get_text(strip=True)
    return _parse_number(text)


def _extract_forks(article) -> int:
    """提取 Fork 数"""
    link = article.select_one("a.Link--muted[href*='network']")
    if not link:
        return 0
    text = link.get_text(strip=True)
    return _parse_number(text)


def _extract_stars_today(article) -> int:
    """提取今日新增星标数"""
    span = article.select_one("span.float-sm-right")
    if not span:
        return 0
    text = span.get_text(strip=True)
    match = re.search(r"(\d+(?:,\d+)?)\s*stars", text)
    if match:
        return _parse_number(match.group(1))
    return 0


def _extract_url(article) -> str:
    """提取项目链接"""
    h2 = article.select_one("h2.h3.lh-condensed")
    if not h2:
        return ""
    
    link = h2.select_one("a")
    if not link:
        return ""
    
    href = link.get("href", "")
    return f"https://github.com{href}"


def _parse_number(text: str) -> int:
    """解析数字字符串（如 '1,234' -> 1234）"""
    text = text.replace(",", "").strip()
    try:
        return int(text)
    except ValueError:
        return 0
```

- [ ] **Step 5: 运行测试确认通过**

```bash
cd "07-项目实战篇/Level-1-入门级/GitHub热榜追踪/github_trending"
uv run pytest tests/test_parser.py -v
```

Expected: PASS

- [ ] **Step 6: 提交**

```bash
git add "07-项目实战篇/Level-1-入门级/GitHub热榜追踪/github_trending/"
git commit -m "feat: add parser module for HTML parsing"
```

---

### Task 5: 创建 storage 模块

**Files:**
- Create: `app/storage.py`
- Test: `tests/test_storage.py`

- [ ] **Step 1: 写失败测试**

```python
import pytest
import json
import csv
from pathlib import Path
from tempfile import TemporaryDirectory
from app.models import TrendingRepo
from app.storage import save_json, save_csv, format_terminal


@pytest.fixture
def sample_repos():
    return [
        TrendingRepo(
            name="microsoft/vscode",
            description="Visual Studio Code",
            language="TypeScript",
            stars=150000,
            forks=22000,
            stars_today=1234,
            url="https://github.com/microsoft/vscode",
        ),
        TrendingRepo(
            name="python/cpython",
            description="Python interpreter",
            language="Python",
            stars=60000,
            forks=15000,
            stars_today=500,
            url="https://github.com/python/cpython",
        ),
    ]


def test_save_json(sample_repos):
    with TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "trending.json"
        save_json(sample_repos, filepath)
        
        assert filepath.exists()
        
        with open(filepath) as f:
            data = json.load(f)
        
        assert len(data) == 2
        assert data[0]["name"] == "microsoft/vscode"


def test_save_csv(sample_repos):
    with TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "trending.csv"
        save_csv(sample_repos, filepath)
        
        assert filepath.exists()
        
        with open(filepath, newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        assert len(rows) == 2
        assert rows[0]["name"] == "microsoft/vscode"
        assert rows[0]["stars"] == "150000"


def test_format_terminal(sample_repos):
    output = format_terminal(sample_repos)
    
    assert "microsoft/vscode" in output
    assert "python/cpython" in output
    assert "150000" in output or "150,000" in output


def test_format_terminal_empty():
    output = format_terminal([])
    assert output == "暂无热门项目数据"


def test_save_json_empty():
    with TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "empty.json"
        save_json([], filepath)
        
        with open(filepath) as f:
            data = json.load(f)
        
        assert data == []
```

- [ ] **Step 2: 运行测试确认失败**

```bash
cd "07-项目实战篇/Level-1-入门级/GitHub热榜追踪/github_trending"
uv run pytest tests/test_storage.py -v
```

Expected: FAIL - `ModuleNotFoundError: No module named 'app.storage'`

- [ ] **Step 3: 实现 storage 模块**

```python
import json
import csv
from pathlib import Path
from app.models import TrendingRepo


def save_json(repos: list[TrendingRepo], filepath: Path) -> None:
    """
    保存为 JSON 文件
    
    Args:
        repos: TrendingRepo 列表
        filepath: 输出文件路径
    """
    data = [repo.to_dict() for repo in repos]
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_csv(repos: list[TrendingRepo], filepath: Path) -> None:
    """
    保存为 CSV 文件
    
    Args:
        repos: TrendingRepo 列表
        filepath: 输出文件路径
    """
    if not repos:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("")
        return
    
    fieldnames = ["name", "description", "language", "stars", "forks", "stars_today", "url"]
    
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for repo in repos:
            writer.writerow(repo.to_dict())


def format_terminal(repos: list[TrendingRepo]) -> str:
    """
    格式化为终端输出
    
    Args:
        repos: TrendingRepo 列表
    
    Returns:
        格式化的文本字符串
    """
    if not repos:
        return "暂无热门项目数据"
    
    lines = []
    for i, repo in enumerate(repos, 1):
        stars_formatted = _format_number(repo.stars)
        stars_today_formatted = _format_number(repo.stars_today)
        
        line = f"{i}. {repo.name}"
        if repo.language:
            line += f" ({repo.language})"
        line += f" - ⭐ {stars_formatted}"
        if repo.stars_today > 0:
            line += f" (+{stars_today_formatted} today)"
        lines.append(line)
        
        if repo.description:
            lines.append(f"   {repo.description}")
        lines.append(f"   {repo.url}")
        lines.append("")
    
    return "\n".join(lines)


def _format_number(n: int) -> str:
    """格式化数字，添加千位分隔符"""
    return f"{n:,}"
```

- [ ] **Step 4: 运行测试确认通过**

```bash
cd "07-项目实战篇/Level-1-入门级/GitHub热榜追踪/github_trending"
uv run pytest tests/test_storage.py -v
```

Expected: PASS

- [ ] **Step 5: 提交**

```bash
git add "07-项目实战篇/Level-1-入门级/GitHub热榜追踪/github_trending/"
git commit -m "feat: add storage module for file output"
```

---

### Task 6: 创建 main CLI 入口

**Files:**
- Create: `app/main.py`

- [ ] **Step 1: 写失败测试**

```python
import pytest
from unittest.mock import patch, Mock
from pathlib import Path
from tempfile import TemporaryDirectory
from app.main import main, parse_args


def test_parse_args_defaults():
    args = parse_args([])
    assert args.language is None
    assert args.range == "daily"
    assert args.output == "terminal"
    assert args.limit == 25


def test_parse_args_with_options():
    args = parse_args(["--language", "python", "--range", "weekly", "--output", "json"])
    assert args.language == "python"
    assert args.range == "weekly"
    assert args.output == "json"


def test_parse_args_limit():
    args = parse_args(["--limit", "10"])
    assert args.limit == 10


def test_main_terminal_output():
    with patch("app.main.fetch_trending_page") as mock_fetch:
        with patch("app.main.parse_trending_page") as mock_parse:
            mock_fetch.return_value = "<html></html>"
            mock_parse.return_value = []
            
            result = main(["--output", "terminal"])
            assert "暂无热门项目数据" in result


def test_main_json_output():
    with TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "output.json"
        
        with patch("app.main.fetch_trending_page") as mock_fetch:
            with patch("app.main.parse_trending_page") as mock_parse:
                from app.models import TrendingRepo
                mock_fetch.return_value = "<html></html>"
                mock_parse.return_value = [
                    TrendingRepo(
                        name="test/repo",
                        description="Test",
                        language="Python",
                        stars=1000,
                        forks=100,
                        stars_today=50,
                        url="https://github.com/test/repo",
                    )
                ]
                
                result = main(["--output", "json", "--file", str(filepath)])
                assert filepath.exists()
```

- [ ] **Step 2: 运行测试确认失败**

```bash
cd "07-项目实战篇/Level-1-入门级/GitHub热榜追踪/github_trending"
uv run pytest tests/test_main.py -v
```

Expected: FAIL - `ModuleNotFoundError: No module named 'app.main'`

- [ ] **Step 3: 实现 main 模块**

```python
import argparse
from pathlib import Path
from app.fetcher import fetch_trending_page
from app.parser import parse_trending_page
from app.storage import save_json, save_csv, format_terminal


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    """
    解析命令行参数
    
    Args:
        args: 参数列表（None 时从 sys.argv 读取）
    
    Returns:
        解析后的参数对象
    """
    parser = argparse.ArgumentParser(
        description="GitHub Trending 热榜追踪工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument(
        "--language",
        type=str,
        default=None,
        help="按编程语言过滤（如 python, javascript, go）",
    )
    
    parser.add_argument(
        "--range",
        type=str,
        choices=["daily", "weekly", "monthly"],
        default="daily",
        help="时间范围：daily（今日）、weekly（本周）、monthly（本月）",
    )
    
    parser.add_argument(
        "--output",
        type=str,
        choices=["terminal", "json", "csv"],
        default="terminal",
        help="输出格式：terminal（终端）、json、csv",
    )
    
    parser.add_argument(
        "--file",
        type=str,
        default=None,
        help="输出文件路径（json/csv 格式时使用）",
    )
    
    parser.add_argument(
        "--limit",
        type=int,
        default=25,
        help="显示项目数量限制",
    )
    
    return parser.parse_args(args)


def main(args: list[str] | None = None) -> str:
    """
    主函数
    
    Args:
        args: 命令行参数
    
    Returns:
        输出内容（terminal 格式）或文件路径
    """
    parsed = parse_args(args)
    
    try:
        html = fetch_trending_page(language=parsed.language, time_range=parsed.range)
        repos = parse_trending_page(html, limit=parsed.limit)
        
        if parsed.output == "terminal":
            output = format_terminal(repos)
            print(output)
            return output
        
        elif parsed.output == "json":
            filepath = Path(parsed.file) if parsed.file else Path("trending.json")
            save_json(repos, filepath)
            print(f"已保存到: {filepath}")
            return str(filepath)
        
        elif parsed.output == "csv":
            filepath = Path(parsed.file) if parsed.file else Path("trending.csv")
            save_csv(repos, filepath)
            print(f"已保存到: {filepath}")
            return str(filepath)
    
    except Exception as e:
        print(f"错误: {e}")
        raise


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: 运行测试确认通过**

```bash
cd "07-项目实战篇/Level-1-入门级/GitHub热榜追踪/github_trending"
uv run pytest tests/test_main.py -v
```

Expected: PASS

- [ ] **Step 5: 提交**

```bash
git add "07-项目实战篇/Level-1-入门级/GitHub热榜追踪/github_trending/"
git commit -m "feat: add CLI main module with argparse"
```

---

### Task 7: 运行完整测试并验证功能

**Files:**
- All test files

- [ ] **Step 1: 运行全部测试**

```bash
cd "07-项目实战篇/Level-1-入门级/GitHub热榜追踪/github_trending"
uv run pytest -v --cov=app
```

Expected: 所有测试 PASS，覆盖率 > 80%

- [ ] **Step 2: 运行 lint 检查**

```bash
cd "07-项目实战篇/Level-1-入门级/GitHub热榜追踪/github_trending"
uv run ruff check .
uv run ruff format --check .
```

Expected: 无 lint 错误

- [ ] **Step 3: 实际运行 CLI（可选，测试网络）**

```bash
cd "07-项目实战篇/Level-1-入门级/GitHub热榜追踪/github_trending"
uv run python -m app.main --limit 5
```

Expected: 输出 5 个热门项目

- [ ] **Step 4: 提交**

```bash
git add "07-项目实战篇/Level-1-入门级/GitHub热榜追踪/github_trending/"
git commit -m "test: verify all tests pass and CLI works"
```

---

### Task 8: 创建项目 README

**Files:**
- Create: `07-项目实战篇/Level-1-入门级/GitHub热榜追踪/github_trending/README.md`

- [ ] **Step 1: 写 README**

```markdown
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
```

- [ ] **Step 2: 提交**

```bash
git add "07-项目实战篇/Level-1-入门级/GitHub热榜追踪/github_trending/README.md"
git commit -m "docs: add project README"
```

---

### Task 9: 创建项目总览 README

**Files:**
- Create: `07-项目实战篇/Level-1-入门级/GitHub热榜追踪/README.md`

- [ ] **Step 1: 写项目总览 README**

```markdown
# GitHub 热榜追踪项目

Level-1 入门级项目，学习爬虫和 CLI 工具开发。

## 项目概述

爬取 GitHub Trending 页面，获取热门项目数据并保存为文件。

```
┌─────────────────────────────────────────────────────────────┐
│                   GitHub Trending CLI                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   输入参数:                                                  │
│   • --language: 按语言过滤 (python/javascript/go)            │
│   • --range: 按时间范围 (daily/weekly/monthly)               │
│   • --output: 输出格式 (json/csv/terminal)                   │
│                                                             │
│   输出数据:                                                  │
│   • 项目名称、描述、主要语言                                  │
│   • 星标数、Fork 数                                          │
│   • 今日新增星标数                                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 目录

| 章节 | 文件 | 主题 |
|------|------|------|
| 01 | [01-页面请求与分析.md](./01-页面请求与分析.md) | HTTP 请求、页面结构 |
| 02 | [02-数据解析.md](./02-数据解析.md) | BeautifulSoup 解析 |
| 03 | [03-命令行参数.md](./03-命令行参数.md) | argparse 参数设计 |
| 04 | [04-数据存储.md](./04-数据存储.md) | JSON/CSV 存储 |
| 05 | [05-完整工具.md](./05-完整工具.md) | CLI 工具整合 |

## 技术栈

- **HTTP 请求**: requests
- **HTML 解析**: beautifulsoup4
- **命令行**: argparse
- **数据存储**: json, csv

## 学习目标

1. 掌握 requests 发送 HTTP 请求
2. 学会 BeautifulSoup 解析 HTML
3. 设计 CLI 参数提升用户体验
4. 实现数据持久化存储

## 前置知识

- Python 基础语法
- 字符串处理
- 字典和列表

## ⚠️ 法律声明

本项目仅供学习，使用时需遵守：

- GitHub robots.txt 协议
- 不对服务器造成过大压力
- 不爬取个人隐私数据
- 遵守相关法律法规
```

- [ ] **Step 2: 提交**

```bash
git add "07-项目实战篇/Level-1-入门级/GitHub热榜追踪/README.md"
git commit -m "docs: add project overview README"
```

---

### Task 10: 创建第1章文档 - 页面请求与分析

**Files:**
- Create: `07-项目实战篇/Level-1-入门级/GitHub热榜追踪/01-页面请求与分析.md`

- [ ] **Step 1: 写第1章文档**

```markdown
# 第 1 章 - 页面请求与分析

本章学习如何发送 HTTP 请求获取网页内容。

---

## 1.1 HTTP 请求基础

### 概念说明

HTTP（HyperText Transfer Protocol）是浏览器和服务器之间通信的协议。

```
┌─────────────────────────────────────────────────────────────┐
│                    HTTP 请求流程                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   客户端（浏览器/Python）                                     │
│       │                                                     │
│       │  发送请求（GET/POST）                                 │
│       ▼                                                     │
│   服务器                                                    │
│       │                                                     │
│       │  返回响应（HTML/JSON）                                │
│       ▼                                                     │
│   客户端接收数据                                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**请求类型：**
- **GET**：获取数据（最常用）
- **POST**：提交数据

---

### 示例代码

使用 requests 库发送 GET 请求：

```python
import requests

url = "https://github.com/trending"
response = requests.get(url)

print(f"状态码: {response.status_code}")
print(f"内容长度: {len(response.text)}")
```

---

## 1.2 设置请求头

### 概念说明

User-Agent 是请求头中的重要字段，告诉服务器你是谁。

```
┌─────────────────────────────────────────────────────────────┐
│                    为什么需要 User-Agent                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   没有 User-Agent:                                          │
│   • 服务器可能拒绝请求                                        │
│   • 被识别为爬虫，返回 403                                    │
│                                                             │
│   有 User-Agent:                                            │
│   • 模拟浏览器行为                                            │
│   • 请求成功率更高                                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### 示例代码

```python
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml",
}

url = "https://github.com/trending"
response = requests.get(url, headers=headers)

print(response.status_code)
```

---

## 1.3 GitHub Trending 页面结构

### 概念说明

访问 `https://github.com/trending` 可以看到热门项目列表。

**页面 URL 规则：**
- 今日热门：`https://github.com/trending`
- 本周热门：`https://github.com/trending?since=weekly`
- 本月热门：`https://github.com/trending?since=monthly`
- Python 项目：`https://github.com/trending/python`

---

### 示例代码

```python
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
}

# 今日热门
url = "https://github.com/trending"
response = requests.get(url, headers=headers)
print(f"今日热门: {response.status_code}")

# 本周热门
url = "https://github.com/trending?since=weekly"
response = requests.get(url, headers=headers)
print(f"本周热门: {response.status_code}")

# Python 项目
url = "https://github.com/trending/python"
response = requests.get(url, headers=headers)
print(f"Python 项目: {response.status_code}")
```

---

## 1.4 处理请求错误

### 概念说明

网络请求可能失败，需要处理错误情况。

**常见错误：**
- 网络超时
- 服务器返回错误（403、404、500）
- DNS 解析失败

---

### 示例代码

```python
import requests
from requests.exceptions import RequestException, Timeout

url = "https://github.com/trending"
headers = {"User-Agent": "Mozilla/5.0"}

try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    print("请求成功")
except Timeout:
    print("请求超时")
except RequestException as e:
    print(f"请求失败: {e}")
```

---

## 常见错误

### 1. 未设置 User-Agent

```python
# 错误示例
response = requests.get("https://github.com/trending")
# 可能返回 403 Forbidden
```

**解决方法：** 添加 User-Agent 头。

### 2. 未处理超时

```python
# 错误示例
response = requests.get(url)  # 可能永久等待
```

**解决方法：** 设置 timeout 参数。

---

## 练习题

1. 使用 requests 获取 GitHub Trending 页面，打印状态码
2. 添加 User-Agent 头，对比请求结果
3. 设置 timeout=5，处理超时异常
4. 分别请求今日、本周、本月热门页面

---

[下一章 → 数据解析](./02-数据解析.md)
```

- [ ] **Step 2: 提交**

```bash
git add "07-项目实战篇/Level-1-入门级/GitHub热榜追踪/01-页面请求与分析.md"
git commit -m "docs: add chapter 01 - HTTP requests and page analysis"
```

---

### Task 11: 创建第2章文档 - 数据解析

**Files:**
- Create: `07-项目实战篇/Level-1-入门级/GitHub热榜追踪/02-数据解析.md`

- [ ] **Step 1: 写第2章文档**

```markdown
# 第 2 章 - 数据解析

本章学习使用 BeautifulSoup 解析 HTML 提取数据。

---

## 2.1 HTML 结构基础

### 概念说明

HTML 由标签组成，每个标签可能有属性和内容。

```
┌─────────────────────────────────────────────────────────────┐
│                    HTML 结构示例                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   <article class="Box-row">                                 │
│       <h2 class="h3">                                       │
│           <a href="/microsoft/vscode">                      │
│               <span class="text-normal">microsoft /</span>  │
│               vscode                                        │
│           </a>                                              │
│       </h2>                                                 │
│       <p class="col-9">项目描述</p>                          │
│       <span itemprop="programmingLanguage">Python</span>    │
│   </article>                                                │
│                                                             │
│   • article: 容器标签                                       │
│   • h2/a: 标题和链接                                        │
│   • class/href: 属性                                        │
│   • 文本: 标签内容                                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 2.2 BeautifulSoup 基础

### 概念说明

BeautifulSoup 是 Python 的 HTML 解析库，可以：
- 根据标签名查找元素
- 根据 CSS 选择器查找
- 提取文本和属性

---

### 示例代码

```python
from bs4 import BeautifulSoup

html = """
<article class="Box-row">
    <h2 class="h3 lh-condensed">
        <a href="/microsoft/vscode">vscode</a>
    </h2>
</article>
"""

soup = BeautifulSoup(html, "html.parser")

# 查找所有 article
articles = soup.find_all("article")
print(f"找到 {len(articles)} 个项目")

# 查找第一个 h2
h2 = soup.find("h2")
print(h2.text)

# CSS 选择器
link = soup.select_one("h2 a")
print(link.get("href"))
```

---

## 2.3 CSS 选择器

### 概念说明

CSS 选择器可以精确定位元素。

**常用选择器：**
| 选择器 | 含义 | 示例 |
|--------|------|------|
| `.class` | 按类名 | `.Box-row` |
| `#id` | 按 ID | `#main` |
| `tag` | 按标签 | `article` |
| `tag.class` | 组合 | `article.Box-row` |
| `parent > child` | 子元素 | `h2 > a` |
| `[attr]` | 按属性 | `[href]` |

---

### 示例代码

```python
from bs4 import BeautifulSoup

html = """
<article class="Box-row">
    <h2 class="h3 lh-condensed">
        <a href="/microsoft/vscode">
            <span class="text-normal">microsoft /</span>
            vscode
        </a>
    </h2>
    <p class="col-9">Visual Studio Code</p>
    <span itemprop="programmingLanguage">TypeScript</span>
</article>
"""

soup = BeautifulSoup(html, "html.parser")

# CSS 选择器查找
article = soup.select_one("article.Box-row")
h2 = article.select_one("h2.h3")
link = h2.select_one("a")

# 提取文本
name = link.text.strip()
print(f"项目名: {name}")

# 提取属性
href = link.get("href")
print(f"链接: {href}")
```

---

## 2.4 解析 GitHub Trending 项目

### 概念说明

GitHub Trending 页面的每个项目在 `<article class="Box-row">` 标签中。

---

### 示例代码

```python
from bs4 import BeautifulSoup
import requests

headers = {"User-Agent": "Mozilla/5.0"}
url = "https://github.com/trending"

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# 查找所有项目
articles = soup.select("article.Box-row")

for article in articles[:3]:  # 只显示前 3 个
    # 提取项目名
    h2 = article.select_one("h2.h3")
    link = h2.select_one("a")
    name = link.get("href").strip("/")
    
    # 提取描述
    p = article.select_one("p.col-9")
    desc = p.text.strip() if p else ""
    
    # 提取语言
    lang_span = article.select_one("span[itemprop='programmingLanguage']")
    lang = lang_span.text.strip() if lang_span else ""
    
    print(f"{name} ({lang}): {desc[:50]}...")
```

---

## 2.5 提取数字数据

### 概念说明

星标数、Fork 数是文本，需要转换为数字。

---

### 示例代码

```python
def parse_number(text: str) -> int:
    """解析数字字符串（如 '1,234' -> 1234）"""
    text = text.replace(",", "").strip()
    try:
        return int(text)
    except ValueError:
        return 0

# 示例
print(parse_number("1,234"))    # 1234
print(parse_number("150,000"))  # 150000
print(parse_number("abc"))      # 0
```

---

## 常见错误

### 1. 选择器写错

```python
# 错误示例
article = soup.select_one("article.box-row")  # 小写，可能找不到
```

**解决方法：** 检查 HTML 实际结构，确认类名大小写。

### 2. 未处理空元素

```python
# 错误示例
p = article.select_one("p")
desc = p.text  # 如果 p 为 None，报错
```

**解决方法：** 使用条件判断。

```python
p = article.select_one("p")
desc = p.text.strip() if p else ""
```

---

## 练习题

1. 使用 BeautifulSoup 解析一个简单 HTML
2. 用 CSS 选择器查找 GitHub Trending 项目名
3. 提取项目描述、语言、星标数
4. 将星标数文本转换为整数

---

[下一章 → 命令行参数](./03-命令行参数.md)
```

- [ ] **Step 2: 提交**

```bash
git add "07-项目实战篇/Level-1-入门级/GitHub热榜追踪/02-数据解析.md"
git commit -m "docs: add chapter 02 - HTML parsing with BeautifulSoup"
```

---

### Task 12: 创建第3章文档 - 命令行参数

**Files:**
- Create: `07-项目实战篇/Level-1-入门级/GitHub热榜追踪/03-命令行参数.md`

- [ ] **Step 1: 写第3章文档**

```markdown
# 第 3 章 - 命令行参数

本章学习使用 argparse 设计 CLI 参数。

---

## 3.1 argparse 基础

### 概念说明

argparse 是 Python 内置的命令行参数解析库。

```
┌─────────────────────────────────────────────────────────────┐
│                    CLI 参数示例                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   基本用法:                                                  │
│   python main.py                                            │
│                                                             │
│   带参数:                                                    │
│   python main.py --language python                          │
│   python main.py --range weekly                             │
│   python main.py --limit 10                                 │
│                                                             │
│   组合使用:                                                  │
│   python main.py --language python --range weekly --limit 5│
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### 示例代码

```python
import argparse

parser = argparse.ArgumentParser(description="GitHub Trending 工具")

# 添加参数
parser.add_argument("--language", type=str, help="编程语言")
parser.add_argument("--limit", type=int, default=25, help="数量限制")

# 解析参数
args = parser.parse_args()

print(f"语言: {args.language}")
print(f"限制: {args.limit}")
```

---

## 3.2 参数类型

### 概念说明

argparse 支持多种参数类型和验证方式。

| 参数类型 | 说明 | 示例 |
|----------|------|------|
| `type=str` | 字符串 | `--language python` |
| `type=int` | 整数 | `--limit 10` |
| `choices` | 限定选项 | `choices=["daily", "weekly"]` |
| `default` | 默认值 | `default=25` |
| `required` | 必填 | `required=True` |

---

### 示例代码

```python
import argparse

parser = argparse.ArgumentParser(description="GitHub Trending 工具")

# 字符串参数
parser.add_argument(
    "--language",
    type=str,
    default=None,
    help="按编程语言过滤",
)

# 限定选项参数
parser.add_argument(
    "--range",
    type=str,
    choices=["daily", "weekly", "monthly"],
    default="daily",
    help="时间范围",
)

# 整数参数
parser.add_argument(
    "--limit",
    type=int,
    default=25,
    help="显示数量",
)

args = parser.parse_args()

# 使用参数
language = args.language
time_range = args.range
limit = args.limit

print(f"语言: {language}, 范围: {time_range}, 限制: {limit}")
```

---

## 3.3 设计友好帮助

### 概念说明

好的 CLI 工具应该有清晰的 --help 输出。

---

### 示例代码

```python
import argparse

parser = argparse.ArgumentParser(
    description="GitHub Trending 热榜追踪工具",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="""
示例用法:
  %(prog)s                     今日热门（默认）
  %(prog)s --language python   Python 项目
  %(prog)s --range weekly      本周热门
  %(prog)s --output json       输出 JSON
""",
)

parser.add_argument(
    "--language",
    help="编程语言过滤（python, javascript, go）",
)
parser.add_argument(
    "--range",
    choices=["daily", "weekly", "monthly"],
    default="daily",
    help="时间范围：daily(今日)/weekly(本周)/monthly(本月)",
)

args = parser.parse_args()
```

运行 `python main.py --help` 会显示友好的帮助信息。

---

## 3.4 完整参数设计

### 示例代码

```python
import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description="GitHub Trending 热榜追踪工具",
    )
    
    parser.add_argument(
        "--language",
        type=str,
        default=None,
        help="按编程语言过滤（python, javascript, go）",
    )
    
    parser.add_argument(
        "--range",
        type=str,
        choices=["daily", "weekly", "monthly"],
        default="daily",
        help="时间范围",
    )
    
    parser.add_argument(
        "--output",
        type=str,
        choices=["terminal", "json", "csv"],
        default="terminal",
        help="输出格式",
    )
    
    parser.add_argument(
        "--file",
        type=str,
        default=None,
        help="输出文件路径",
    )
    
    parser.add_argument(
        "--limit",
        type=int,
        default=25,
        help="显示项目数量",
    )
    
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    print(args)
```

---

## 常见错误

### 1. 参数类型错误

```bash
# 错误示例
python main.py --limit abc  # abc 不是整数
```

**结果：** argparse 自动报错并退出。

### 2. 无效选项

```bash
# 错误示例
python main.py --range hourly  # hourly 不在 choices 中
```

**结果：** argparse 报错 "invalid choice"。

---

## 练习题

1. 创建一个简单的 argparse 程序，接收 --name 参数
2. 添加 --count 参数，类型为整数，默认值 10
3. 使用 choices 限制 --mode 参数只能是 "fast" 或 "slow"
4. 运行 --help 查看生成的帮助信息

---

[下一章 → 数据存储](./04-数据存储.md)
```

- [ ] **Step 2: 提交**

```bash
git add "07-项目实战篇/Level-1-入门级/GitHub热榜追踪/03-命令行参数.md"
git commit -m "docs: add chapter 03 - CLI argument design"
```

---

### Task 13: 创建第4章文档 - 数据存储

**Files:**
- Create: `07-项目实战篇/Level-1-入门级/GitHub热榜追踪/04-数据存储.md`

- [ ] **Step 1: 写第4章文档**

```markdown
# 第 4 章 - 数据存储

本章学习将数据保存为 JSON 和 CSV 文件。

---

## 4.1 JSON 文件存储

### 概念说明

JSON（JavaScript Object Notation）是常用的数据格式。

```
┌─────────────────────────────────────────────────────────────┐
│                    JSON 结构示例                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   [                                                         │
│     {                                                       │
│       "name": "microsoft/vscode",                           │
│       "description": "Visual Studio Code",                  │
│       "language": "TypeScript",                             │
│       "stars": 150000                                       │
│     },                                                      │
│     {                                                       │
│       "name": "python/cpython",                             │
│       "language": "Python"                                  │
│     }                                                       │
│   ]                                                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### 示例代码

```python
import json

data = [
    {
        "name": "microsoft/vscode",
        "description": "Visual Studio Code",
        "language": "TypeScript",
        "stars": 150000,
    },
    {
        "name": "python/cpython",
        "description": "Python interpreter",
        "language": "Python",
        "stars": 60000,
    },
]

# 写入 JSON 文件
with open("trending.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("已保存到 trending.json")
```

---

## 4.2 CSV 文件存储

### 概念说明

CSV（Comma-Separated Values）是表格数据格式。

```
┌─────────────────────────────────────────────────────────────┐
│                    CSV 结构示例                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   name,description,language,stars                           │
│   microsoft/vscode,Visual Studio Code,TypeScript,150000     │
│   python/cpython,Python interpreter,Python,60000            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### 示例代码

```python
import csv

data = [
    {"name": "microsoft/vscode", "language": "TypeScript", "stars": 150000},
    {"name": "python/cpython", "language": "Python", "stars": 60000},
]

fieldnames = ["name", "language", "stars"]

with open("trending.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for row in data:
        writer.writerow(row)

print("已保存到 trending.csv")
```

---

## 4.3 格式化终端输出

### 概念说明

直接在终端显示数据，需要格式化处理。

---

### 示例代码

```python
def format_number(n: int) -> str:
    """添加千位分隔符"""
    return f"{n:,}"

repos = [
    {"name": "microsoft/vscode", "stars": 150000, "stars_today": 1234},
    {"name": "python/cpython", "stars": 60000, "stars_today": 500},
]

for i, repo in enumerate(repos, 1):
    stars = format_number(repo["stars"])
    today = format_number(repo["stars_today"])
    print(f"{i}. {repo['name']} - ⭐ {stars} (+{today} today)")

# 输出:
# 1. microsoft/vscode - ⭐ 150,000 (+1,234 today)
# 2. python/cpython - ⭐ 60,000 (+500 today)
```

---

## 4.4 完整存储模块

### 示例代码

```python
import json
import csv
from pathlib import Path

def save_json(data: list, filepath: Path) -> None:
    """保存为 JSON"""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def save_csv(data: list, filepath: Path) -> None:
    """保存为 CSV"""
    if not data:
        return
    
    fieldnames = data[0].keys()
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def format_terminal(data: list) -> str:
    """格式化终端输出"""
    if not data:
        return "暂无数据"
    
    lines = []
    for i, repo in enumerate(data, 1):
        stars = f"{repo.get('stars', 0):,}"
        line = f"{i}. {repo['name']} - ⭐ {stars}"
        lines.append(line)
    
    return "\n".join(lines)
```

---

## 常见错误

### 1. 编码问题

```python
# 错误示例
with open("trending.json", "w") as f:  # 未指定 encoding
    json.dump(data, f)
# 中文可能乱码
```

**解决方法：** 指定 `encoding="utf-8"`。

### 2. CSV newline 问题

```python
# 错误示例
with open("trending.csv", "w") as f:  # Windows 会多出空行
    writer = csv.writer(f)
```

**解决方法：** 添加 `newline=""`。

---

## 练习题

1. 创建一个列表，写入 JSON 文件
2. 读取刚才的 JSON 文件，打印内容
3. 将同样的数据写入 CSV 文件
4. 实现一个格式化函数，添加千位分隔符

---

[下一章 → 完整工具](./05-完整工具.md)
```

- [ ] **Step 2: 提交**

```bash
git add "07-项目实战篇/Level-1-入门级/GitHub热榜追踪/04-数据存储.md"
git commit -m "docs: add chapter 04 - data storage with JSON and CSV"
```

---

### Task 14: 创建第5章文档 - 完整工具

**Files:**
- Create: `07-项目实战篇/Level-1-入门级/GitHub热榜追踪/05-完整工具.md`

- [ ] **Step 1: 写第5章文档**

```markdown
# 第 5 章 - 完整工具

本章整合所有模块，完成 CLI 工具。

---

## 5.1 模块整合

### 概念说明

将 fetcher、parser、storage、main 模块组合成完整工具。

```
┌─────────────────────────────────────────────────────────────┐
│                    工具架构                                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   main.py (CLI 入口)                                        │
│       │                                                     │
│       │  解析参数                                            │
│       ▼                                                     │
│   fetcher.py                                                │
│       │  发送请求                                            │
│       ▼                                                     │
│   parser.py                                                 │
│       │  解析 HTML                                           │
│       ▼                                                     │
│   storage.py                                                │
│       │  保存数据                                            │
│       ▼                                                     │
│   输出结果                                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 5.2 主函数实现

### 示例代码

```python
import argparse
from pathlib import Path
from fetcher import fetch_trending_page
from parser import parse_trending_page
from storage import save_json, save_csv, format_terminal

def main():
    args = parse_args()
    
    try:
        # 获取页面
        html = fetch_trending_page(
            language=args.language,
            time_range=args.range,
        )
        
        # 解析数据
        repos = parse_trending_page(html, limit=args.limit)
        
        # 输出结果
        if args.output == "terminal":
            print(format_terminal(repos))
        elif args.output == "json":
            filepath = Path(args.file) if args.file else Path("trending.json")
            save_json(repos, filepath)
            print(f"已保存到: {filepath}")
        elif args.output == "csv":
            filepath = Path(args.file) if args.file else Path("trending.csv")
            save_csv(repos, filepath)
            print(f"已保存到: {filepath}")
    
    except Exception as e:
        print(f"错误: {e}")
        raise

def parse_args():
    parser = argparse.ArgumentParser(description="GitHub Trending 工具")
    parser.add_argument("--language", help="编程语言")
    parser.add_argument("--range", choices=["daily", "weekly", "monthly"], default="daily")
    parser.add_argument("--output", choices=["terminal", "json", "csv"], default="terminal")
    parser.add_argument("--file", help="输出文件")
    parser.add_argument("--limit", type=int, default=25)
    return parser.parse_args()

if __name__ == "__main__":
    main()
```

---

## 5.3 运行示例

### 基本使用

```bash
# 今日热门
uv run python -m app.main

# 显示帮助
uv run python -m app.main --help
```

### 高级使用

```bash
# Python 项目，本周热门
uv run python -m app.main --language python --range weekly

# 输出 JSON
uv run python -m app.main --output json --file trending.json

# 输出 CSV，限制 10 个
uv run python -m app.main --output csv --limit 10
```

---

## 5.4 扩展建议

### 添加新功能

完成基础功能后，可以尝试：

1. **添加颜色输出**
```python
# 使用 rich 库美化终端输出
from rich.console import Console
console = Console()
console.print("[bold green]热门项目[/]")
```

2. **添加缓存机制**
```python
# 缓存请求结果，避免重复请求
import hashlib
cache_key = hashlib.md5(url.encode()).hexdigest()
```

3. **添加配置文件**
```python
# 从 config.yaml 读取默认参数
import yaml
config = yaml.safe_load(open("config.yaml"))
```

---

## 常见错误

### 1. 模块导入错误

```python
# 错误示例
from app.fetcher import fetch_trending_page  # 可能找不到模块
```

**解决方法：** 确保目录结构正确，使用 `python -m app.main` 运行。

### 2. 未处理异常

```python
# 错误示例
html = fetch_trending_page()  # 网络失败时崩溃
```

**解决方法：** 使用 try-except 包裹。

---

## 练习题

1. 运行完整工具，查看今日热门
2. 使用 --language python 查看 Python 项目
3. 保存结果为 JSON 文件
4. 尝试添加 --verbose 参数显示详细信息

---

## 项目完成检查

- [ ] fetcher.py 能成功获取页面
- [ ] parser.py 能解析项目数据
- [ ] storage.py 能保存文件
- [ ] main.py CLI 参数正常工作
- [ ] 测试全部通过
- [ ] 可以向他人演示

---

## 下一步

恭喜完成本项目！建议继续学习：

- [Level-2 数据采集爬虫](../Level-2-进阶级/数据采集爬虫/)
- [Level-2 文件管理系统](../Level-2-进阶级/文件管理系统/)
```

- [ ] **Step 2: 提交**

```bash
git add "07-项目实战篇/Level-1-入门级/GitHub热榜追踪/05-完整工具.md"
git commit -m "docs: add chapter 05 - complete CLI tool integration"
```

---

### Task 15: 更新项目实战篇 README

**Files:**
- Modify: `07-项目实战篇/README.md`

- [ ] **Step 1: 在 Level-1 表格中添加新项目**

在现有的 Level-1 入门级表格中添加：

```markdown
| [GitHub热榜追踪](./Level-1-入门级/GitHub热榜追踪/) | requests, BeautifulSoup | 1天 | HTTP、HTML解析 |
```

- [ ] **Step 2: 提交**

```bash
git add "07-项目实战篇/README.md"
git commit -m "docs: add GitHub Trending project to Level-1 list"
```

---

## 实施完成检查

- [ ] 所有测试通过 (`uv run pytest -v`)
- [ ] Lint 检查通过 (`uv run ruff check .`)
- [ ] CLI 工具可正常运行
- [ ] 5 章文档完整
- [ ] README 清晰
- [ ] Git 提交历史清晰