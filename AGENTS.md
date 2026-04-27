# AGENTS.md

## Repository Overview

Python tutorial repo with Chinese markdown docs + 49 sample projects across 9 sections.

## Architecture

**Multi-project monorepo**: No root-level config. Each project has its own `pyproject.toml`.

```
<章节目录>/<项目>/
├── pyproject.toml
├── app/                     # Source (43/49 projects use app/)
├── tests/                   # pytest suite (38/49 projects, ~2200 test files)
└── uv.lock                  # If deps installed (32/49 projects)
```

- **Build**: hatchling (all projects)
- **Package names**: `app/` (43), `processor/` (1), `analyzer/` (1), 4 projects have no explicit package
- **Ruff config**: 26/49 projects have `[tool.ruff]`; others have no lint setup
- **PyPI mirror**: Many projects use Tsinghua mirror (`pypi.tuna.tsinghua.edu.cn`)
- **Dev deps**: 13 projects use `[dependency-groups]`, 6 use `[project.optional-dependencies]`

## Commands

**Must cd into project directory first — no root-level commands:**

```bash
cd <project_directory>
uv run pytest                   # Run tests (if tests/ exists)
uv run pytest tests/test_x.py   # Single test file
uv run pytest -k "test_name"    # Run specific test
uv run ruff check .             # Lint (if [tool.ruff] exists)
uv run ruff check --fix .       # Auto-fix
uv run ruff format .            # Format
uv run uvicorn app.main:app --reload  # FastAPI apps
uv add <package>                # Add dependency
```

**Dev deps**: Use `[dependency-groups]` (preferred) or `[project.optional-dependencies]` — both work with `uv sync --group dev`.

**Async tests**: Some projects use `pytest-asyncio` with `asyncio_mode = "auto"` in pyproject.toml.

## Sections

| Dir | Topics |
|-----|--------|
| 01-基础入门篇 | Python入门、变量、运算符、字符串、数据结构 |
| 02-核心编程篇 | 函数、OOP、异常、迭代器、装饰器、类型提示 |
| 03-高级语法篇 | 模块与包、标准库、并发与异步 |
| 04-Web开发篇 | Flask、FastAPI |
| 05-机器学习篇 | 基础概念、数据预处理、监督/无监督学习 |
| 06-神经网络与深度学习篇 | PyTorch、CNN、RNN |
| 07-项目实战篇 | Level 1-4 项目（入门→专业级） |
| 08-工程实践篇 | 代码质量、项目管理、运维监控 |
| 09-LangChain与LangGraph篇 | LangChain/LangGraph、Agent实战 |

## Toolchain

- **Python**: 3.11+
- **Package manager**: uv (not pip)
- **Test**: pytest
- **Lint/Format**: ruff (line-length 88 default, py311, rules: E,F,I,N,W,UP,B,SIM)
