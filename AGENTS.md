# AGENTS.md

## Repository Overview

Python tutorial repo with Chinese markdown docs + 40+ sample Python projects across 8 sections (基础→核心→高级→Web→ML→DL→项目→工程实践).

## Architecture

**Multi-project monorepo**: No root-level config. Each project has its own `pyproject.toml`.

```
<chapter_dir>/<project>/
├── pyproject.toml
├── app/ or src/              # Source code (most use app/)
├── tests/                    # Test suite
└── uv.lock                   # If deps exist
```

## Commands

**Must cd into project directory first — no root-level commands:**

```bash
cd <project_directory>
uv run pytest                   # Run tests
uv run pytest tests/test_x.py   # Single test file
uv run ruff check .             # Lint
uv run ruff check --fix .       # Auto-fix
uv run ruff format .            # Format
uv run uvicorn app.main:app --reload  # FastAPI apps
uv add <package>                # Add dependency
```

## Toolchain

- **Python**: 3.11+
- **Package manager**: uv (not pip)
- **Test**: pytest
- **Lint/Format**: ruff (line-length 88, py311, rules: E,F,I,N,W,UP,B,SIM)

## Writing Conventions

- **Language**: Simplified Chinese prose; code comments may be Chinese or English
- **Audience**: Beginners — explain "why", avoid undefined jargon
- **Markdown format**: `# 第 N 章 - <标题>（详细版）` → `### N.N` subsections → `#### 概念说明` → `#### 示例代码` → `#### 常见错误` → `#### 练习题`
- **ASCII diagrams**: Use box-drawing characters (┌─┬─┐)