# AGENTS.md

## Repository Overview

Python tutorial documentation repo with Chinese-language learning materials (50+ chapters). Contains markdown docs + sample Python projects per chapter.

## Key Architecture

**Multi-project monorepo**: Each chapter has its own `pyproject.toml`. No root-level config — **tests/lint must run per-project**.

Project structure:
```
<chapter_dir>/<project_name>/   # e.g., 01-基础入门篇/01-Python入门/python_basics/
├── pyproject.toml
├── app/                        # Source code
├── tests/                      # Test suite
└── uv.lock                     # Lockfile (if deps exist)
```

## Commands

**All commands require cd into project directory first:**

```bash
cd <project_directory>          # REQUIRED — no root-level commands
uv run pytest                   # Run tests
uv run pytest tests/test_x.py   # Single test file
uv run pytest -v --cov=app      # Verbose with coverage
uv run ruff check .             # Lint
uv run ruff check --fix .       # Auto-fix lint
uv run ruff format .            # Format
uv run uvicorn app.main:app --reload  # FastAPI apps
uv add <package>                # Add dependency
```

## Toolchain

- **Python**: 3.11+ (required for modern syntax)
- **Package manager**: uv (not pip)
- **Test framework**: pytest
- **Linter/formatter**: ruff (line-length 88)

## Language

- All prose: **Simplified Chinese**
- Code comments: Chinese or English
- Audience: beginners — explain "why", avoid undefined jargon

## Markdown Structure

Chapter format: `# 第 N 章 - <标题>（详细版）` → sections with `### N.N` subsections → `#### 概念说明` → `#### 示例代码` → `#### 常见错误` → `#### 练习题`

Use box-drawing characters (┌─┬─┐) for ASCII diagrams.

## Key Files

| File | Purpose |
|------|---------|
| `README.md` | Table of contents |
| `CLAUDE.md` | Claude Code guidance |
| `QWEN.md` | Qwen guidance |