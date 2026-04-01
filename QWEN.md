# QWEN.md

This file provides guidance to Qwen Code when working with code in this repository.

## Repository Overview

This is a **Python tutorial documentation repository** containing comprehensive Chinese-language learning materials covering Python from beginner to advanced topics, including web development, machine learning, and deep learning. The repository contains **markdown documentation only** — there is no source code to build, lint, or test.

## Content Structure

The tutorial is organized into **8 major sections** with **50+ chapters**:

| Section | Directory | Chapters | Topics |
|---------|-----------|----------|--------|
| 语言基础篇 | `01-基础入门篇/` | 10 | Python intro, variables, operators, control flow, strings, list, tuple, dict, set, comprehensions |
| 核心语法篇 | `02-核心编程篇/` | 7 | Functions, modules/packages, file I/O, OOP, exceptions, iterators/generators, decorators/closures |
| 高级语法篇 | `03-高级语法篇/` | 2 | Regular expressions, concurrency & async programming |
| Web 开发篇 | `04-Web 开发篇/` | 6 | HTTP basics, Flask (intro/advanced/expert), FastAPI, server projects |
| 机器学习篇 | `05-机器学习篇/` | 5 | ML basics, data preprocessing, supervised/unsupervised learning, model evaluation |
| 神经网络篇 | `06-神经网络与深度学习篇/` | 5 | Neural network basics, PyTorch, CNN, RNN, deep learning projects |
| 项目实战篇 | `07-项目实战篇/` | 5 | Weather tool, file renamer, todo manager, web scraper, CSV analyzer |
| 工程实践篇 | `08-工程实践篇/` | 10 | Package management, code standards, testing, documentation, CI/CD, logging, security, performance, debugging |

Additional reference directories:
- `20-uv包管理器/` — uv package manager guide
- `21-类型提示/` — Type hints
- `22-列表推导式/` — List comprehensions
- `23-asyncio高级编程/` — Advanced asyncio

## File Naming Conventions

- **Chapter files**: `NN-<Chinese-title>.md` (e.g., `01-Python简介与环境搭建.md`, `13-面向对象编程.md`)
- **Section directories**: `NN-<Chinese-title>/` (e.g., `01-基础入门篇/`, `04-Web 开发篇/`)
- All content is in **Simplified Chinese**

## Writing Conventions

Chapters follow a consistent structure:

```markdown
# 第 N 章 - <标题>（详细版）

## 第一部分：<主题>

### N.N <子主题>

#### 概念说明

<解释性文字>

```
┌─────────────────────────────────────────┐
│          ASCII 图表说明                  │
├─────────────────────────────────────────┤
│                                         │
│  使用 box-drawing characters            │
│  (┌─┬─┐ │ ├─┼─┤ └─┴─┘)                  │
│                                         │
└─────────────────────────────────────────┘
```

#### 示例代码

```python
# 代码示例
# 注释可以是中文或英文
print("Hello, World!")
```

#### 常见错误

<错误说明和解决方案>

#### 练习题

<练习题目>
```

### Key Style Guidelines

1. **ASCII diagrams**: Used extensively for visual explanations with box-drawing characters
2. **Code blocks**: Always use fenced code blocks with language specifier (```python)
3. **Comments**: Can be in Chinese or English within code
4. **Audience**: Beginners — explain the "why", avoid jargon without definition, use analogies
5. **Structure**: Each concept follows: 概念说明 → 示例代码 → 常见错误 → 练习题

## Key Reference Files

| File | Purpose |
|------|---------|
| `README.md` | Table of contents with learning path diagram |
| `00-Python学习大纲.md` | Full curriculum outline with chapter-by-chapter topic breakdown |
| `CLAUDE.md` | AI assistant guidance (English) |

## Toolchain (for code examples in chapters)

| Tool | Version | Notes |
|------|---------|-------|
| Python | 3.11+ | Required for modern syntax features (match statements, type hints improvements) |
| uv | Latest | Preferred package manager (replaces pip + venv) |
| Editor | VS Code | With Python extension |

### uv Commands Reference

```bash
# Install uv (macOS/Linux)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Python
uv python install 3.11

# Create new project
uv init my-project
cd my-project

# Run Python files
uv run python main.py

# Add dependencies
uv add requests
```

## Learning Paths

| Direction | Recommended Chapters | Target Role |
|-----------|---------------------|-------------|
| Python 开发 | 1→2→3→8→7 | Python backend/automation |
| Web 后端开发 | 1→2→3→4→8 | Flask/FastAPI engineer |
| 全栈开发 | 1→2→3→4→8 + frontend | Full-stack engineer |
| 机器学习 | 1→2→3→5→8 | ML engineer |
| 深度学习 | 1→2→3→5→6→8 | CV/NLP algorithm engineer |
| AI 应用开发 | 1→2→3→4→5→6→8 | AI application engineer |

## When Editing Content

1. **Maintain consistency**: Follow the existing chapter structure and formatting
2. **Use ASCII diagrams**: For visual explanations, use box-drawing characters
3. **Include practical examples**: Every concept should have runnable code
4. **Add "常见错误" sections**: Help beginners avoid common pitfalls
5. **Keep Chinese prose**: All explanatory text should be in Simplified Chinese
6. **Update cross-references**: If adding new chapters, update README.md and 00-Python学习大纲.md

## Git Ignore Patterns

The repository ignores:
- `.DS_Store` (macOS)
- Editor files (`.vscode/`, `.idea/`, swap files)
- Python artifacts (`__pycache__/`, `*.pyc`, venv)
- `.env` files