# AGENTS.md

## Repository Overview

Python tutorial repo with Chinese markdown docs + 49 sample Python projects across 9 sections (基础→核心→高级→Web→ML→DL→项目→工程实践→LangChain/LangGraph).

## Architecture

**Multi-project monorepo**: No root-level config. 49 independent projects, each with its own `pyproject.toml`.

```
<chapter_dir>/<project>/
├── pyproject.toml
├── app/ or <custom_pkg>/     # Source (most use app/)
│   ├── core/                 # Core logic (optional)
│   └── utils/                # Helpers (optional)
├── tests/                    # pytest suite (optional)
└── uv.lock                   # If deps installed
```

- **Build system**: hatchling (all projects)
- **Source package**: `app/` in most projects; a few use custom names (e.g., `processor/`)
- **Ruff/pytest config**: Only present in ~14 of 49 projects; absent projects have no lint/test setup
- **No CI/CD**, no pre-commit hooks

## Commands

**Must cd into project directory first — no root-level commands:**

```bash
cd <project_directory>
uv run pytest                   # Run tests (if tests/ exists)
uv run pytest tests/test_x.py   # Single test file
uv run pytest -k "test_name"    # Run specific test by name
uv run ruff check .             # Lint (if [tool.ruff] exists)
uv run ruff check --fix .       # Auto-fix
uv run ruff format .            # Format
uv run uvicorn app.main:app --reload  # FastAPI apps
uv add <package>                # Add dependency
uv remove <package>             # Remove dependency
```

**Dev dependencies**: Projects use either `[project.optional-dependencies]` (dev) or `[[dependency-groups]]` (dev) — both work with `uv sync --group dev`.

## Sections

| Dir | Topics |
|-----|--------|
| 01-基础入门篇 | Python入门、变量、运算符、字符串、数据结构 |
| 02-核心编程篇 | 函数、OOP、异常、迭代器、装饰器、类型提示 |
| 03-高级语法篇 | 模块与包、标准库、并发与异步 |
| 04-Web开发篇 | Flask、FastAPI |
| 05-机器学习篇 | 基础概念、数据预处理、监督/无监督学习、模型优化 |
| 06-神经网络与深度学习篇 | PyTorch、CNN、RNN、实战项目 |
| 07-项目实战篇 | Level 1-4 项目（入门→专业级） |
| 08-工程实践篇 | 代码质量、项目管理、运维监控、开发技巧 |
| 09-LangChain与LangGraph篇 | LangChain/LangGraph入门与进阶、Agent实战 |

## Toolchain

- **Python**: 3.11+
- **Package manager**: uv (not pip)
- **Test**: pytest
- **Lint/Format**: ruff (line-length 88, py311, rules: E,F,I,N,W,UP,B,SIM)
