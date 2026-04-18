# AGENTS.md

## Repository Overview

Python tutorial repo with Chinese markdown docs + 49 sample Python projects across 9 sections (基础→核心→高级→Web→ML→DL→项目→工程实践→LangChain/LangGraph).

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
uv run pytest -k "test_name"    # Run specific test by name
uv run ruff check .             # Lint
uv run ruff check --fix .       # Auto-fix
uv run ruff format .            # Format
uv run uvicorn app.main:app --reload  # FastAPI apps
uv add <package>                # Add dependency
```

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

## Writing Conventions

- **Language**: Simplified Chinese prose; code comments may be Chinese or English
- **Audience**: Beginners — explain "why", avoid undefined jargon
- **Markdown format**: `# 第 N 章 - <标题>（详细版）` → `### N.N` subsections → `#### 概念说明` → `#### 示例代码` → `#### 常见错误` → `#### 练习题`
- **ASCII diagrams**: Use box-drawing characters (┌─┬─┐)