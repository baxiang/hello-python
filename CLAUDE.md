# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Python tutorial repo with Chinese markdown docs + 40+ sample Python projects across 9 sections: 基础入门 → 核心编程 → 高级语法 → Web开发 → 机器学习 → 神经网络 → 项目实战 → 工程实践 → LangChain/LangGraph.

## Architecture

**Multi-project monorepo**: No root-level config. Each project has its own `pyproject.toml`.

```
<章节目录>/<项目>/
├── pyproject.toml
├── app/                       # Source code (most projects use app/)
│   ├── core/                  # Core logic
│   └── utils/                 # Helpers
├── tests/                     # pytest test suite
└── uv.lock                    # If dependencies exist
```

## Commands

**Must cd into project directory first — no root-level commands:**

```bash
cd <project_directory>
uv run pytest                   # Run all tests
uv run pytest tests/test_x.py   # Single test file
uv run pytest -k "test_name"    # Run specific test
uv run ruff check .             # Lint
uv run ruff check --fix .       # Auto-fix lint issues
uv run ruff format .            # Format code
uv run uvicorn app.main:app --reload  # FastAPI apps
uv add <package>                # Add dependency
uv remove <package>             # Remove dependency
```

## Content Organization

| Section | Directory | Topics |
|---------|-----------|--------|
| 01 | 01-基础入门篇 | Python入门、变量、运算符、字符串、数据结构 |
| 02 | 02-核心编程篇 | 函数、OOP、异常、迭代器、装饰器、类型提示 |
| 03 | 03-高级语法篇 | 模块与包、标准库、并发与异步 |
| 04 | 04-Web开发篇 | Flask、FastAPI |
| 05 | 05-机器学习篇 | 基础概念、数据预处理、监督/无监督学习、模型优化 |
| 06 | 06-神经网络与深度学习篇 | PyTorch、CNN、RNN、实战项目 |
| 07 | 07-项目实战篇 | Level 1-4 项目（入门→专业级） |
| 08 | 08-工程实践篇 | 代码质量、项目管理、运维监控、开发技巧 |
| 09 | 09-LangChain与LangGraph篇 | LangChain/LangGraph入门与进阶、Agent实战 |

## Writing Conventions

Markdown chapters follow a consistent structure:
- **Chapter heading**: `# 第 N 章 - <标题>（详细版）`
- **Sections**: `## 第一部分 / ## 第二部分` with `### N.N` subsections
- **Concept blocks**: `#### 概念说明` → `#### 示例代码` → `#### 常见错误` → `#### 练习题`
- **ASCII diagrams**: Use box-drawing characters (`┌─┬─┐`) for visual explanations
- **Language**: Simplified Chinese prose; code comments may be Chinese or English
- **Audience**: Beginners — explain the "why", avoid undefined jargon

## Toolchain

- **Python**: 3.11+
- **Package manager**: uv (not pip)
- **Test framework**: pytest
- **Lint/Format**: ruff (line-length 88, target py311, rules: E,F,I,N,W,UP,B,SIM)
- **Web framework**: Flask / FastAPI (uvicorn for serving)

## Key Reference Files

- **README.md** — Table of contents with learning roadmap
- **00-Python学习大纲.md** — Full curriculum outline
- **AGENTS.md** — Concise architecture summary for AI agents
