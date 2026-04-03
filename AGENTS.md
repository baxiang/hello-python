# AGENTS.md

This file provides guidance to AI coding agents working in this repository.

## Repository Overview

This is a **Python tutorial documentation repository** containing comprehensive Chinese-language learning materials covering Python from beginner to advanced topics, including web development, machine learning, and deep learning. The repository contains both markdown documentation and sample Python projects for each chapter.

## Project Structure

```
hello-python/
├── 00-Python学习大纲.md       # Full curriculum outline
├── README.md                   # Table of contents
├── CLAUDE.md                   # Claude Code guidance
├── QWEN.md                     # Qwen Code guidance
├── 01-基础入门篇/              # Python basics (10 chapters)
├── 02-核心编程篇/              # Core programming (7 chapters)
├── 03-高级语法篇/              # Advanced syntax (2 chapters)
├── 04-Web 开发篇/              # Web development (Flask/FastAPI)
├── 05-机器学习篇/              # Machine learning
├── 06-神经网络与深度学习篇/    # Deep learning
├── 07-项目实战篇/              # Practical projects
└── 08-工程实践篇/              # Engineering practices
```

Each chapter directory contains:
- Markdown documentation files (`NN-<title>.md`)
- Sample projects with `app/` and `tests/` directories
- `pyproject.toml` for project configuration

## Build/Lint/Test Commands

### Running Tests

Each sample project has its own test suite. Navigate to the project directory and run:

```bash
# Run all tests in a project
cd <project_directory>
uv run pytest

# Run a specific test file
uv run pytest tests/test_module.py

# Run a specific test function
uv run pytest tests/test_module.py::test_function_name

# Run with verbose output
uv run pytest -v

# Run with coverage
uv run pytest --cov=app --cov-report=term-missing
```

### Linting and Formatting

```bash
# Check code with ruff (per-project)
cd <project_directory>
uv run ruff check .

# Auto-fix linting issues
uv run ruff check --fix .

# Format code with ruff
uv run ruff format .

# Check formatting without modifying
uv run ruff format --check .
```

### Running Applications

```bash
# FastAPI applications
cd <project_directory>
uv run uvicorn app.main:app --reload

# Flask applications
cd <project_directory>
uv run python app/main.py

# Simple Python scripts
uv run python <script.py>
```

### Installing Dependencies

```bash
# Add a dependency
uv add <package>

# Add a development dependency
uv add --dev <package>

# Sync dependencies
uv sync
```

## Code Style Guidelines

### Imports

Follow PEP 8 import ordering with three groups separated by blank lines:

```python
# Standard library
import os
import sys
from pathlib import Path

# Third-party libraries
import requests
from fastapi import FastAPI, HTTPException

# Local modules
from app.core.config import get_settings
from app.services.user_service import UserService
```

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Variables/Functions | snake_case | `user_name`, `calculate_total()` |
| Classes | PascalCase | `UserProfile`, `DataProcessor` |
| Constants | UPPER_SNAKE_CASE | `MAX_SIZE`, `API_KEY` |
| Private attributes | _leading_underscore | `_internal_value`, `_cache` |
| Module-level "private" | __dunder__ | `__version__`, `__all__` |

### Type Hints

Use type hints for all function signatures:

```python
from typing import List, Dict, Optional, Any

# Basic types
def greet(name: str) -> str:
    return f"Hello, {name}"

# Container types (prefer Python 3.9+ syntax)
def process_items(items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}

# Optional types
def find_user(user_id: int) -> Optional[dict]:
    ...

# Union types (Python 3.10+ syntax)
def parse_value(value: str | int) -> str:
    return str(value)

# Use from __future__ import annotations for forward references
from __future__ import annotations
```

### Docstrings

Use Google-style docstrings:

```python
def calculate_average(numbers: list[float]) -> float:
    """
    Calculate the average of a list of numbers.

    Args:
        numbers: A list of numeric values

    Returns:
        The arithmetic mean of the numbers

    Raises:
        ValueError: If the list is empty

    Example:
        >>> calculate_average([1, 2, 3])
        2.0
    """
    if not numbers:
        raise ValueError("列表不能为空")
    return sum(numbers) / len(numbers)
```

### Error Handling

```python
# Use specific exceptions
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("除数不能为零")
    return a / b

# HTTP APIs: use appropriate status codes
@router.get("/users/{user_id}")
def get_user(user_id: int):
    user = user_service.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user

# Use try-except for expected exceptions
try:
    result = risky_operation()
except ValueError as e:
    logger.error(f"操作失败: {e}")
    return None
```

### Formatting

- Line length: 88 characters (Black/Ruff default)
- Indentation: 4 spaces
- Use trailing commas in multi-line collections
- String quotes: prefer double quotes for docstrings, single or double for code

```python
# Multi-line with trailing commas
users = [
    User(id=1, name="Alice", email="alice@example.com"),
    User(id=2, name="Bob", email="bob@example.com"),
]

# Function calls
result = some_function(
    arg1=value1,
    arg2=value2,
    arg3=value3,
)
```

### Data Classes

Prefer dataclasses for simple data structures:

```python
from dataclasses import dataclass

@dataclass
class User:
    """用户数据类"""
    id: int
    name: str
    email: str
    is_active: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "is_active": self.is_active,
        }
```

### Async Code

```python
import asyncio

# Use async/await for I/O-bound operations
async def fetch_data(url: str) -> dict:
    response = await client.get(url)
    return response.json()

# Use asyncio.Lock for thread-safe async operations
class AsyncCounter:
    def __init__(self, start: int = 0):
        self._value = start
        self._lock = asyncio.Lock()

    async def increment(self) -> int:
        async with self._lock:
            self._value += 1
            return self._value
```

## Markdown Writing Conventions

### Chapter Structure

```markdown
# 第 N 章 - <标题>（详细版）

## 第一部分：<主题>

### N.N <子主题>

#### 概念说明

<解释性文字>

#### 示例代码

```python
# 代码示例
print("Hello, World!")
```

#### 常见错误

<错误说明和解决方案>

#### 练习题

<练习题目>
```

### ASCII Diagrams

Use box-drawing characters for visual explanations:

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

## Key Reference Files

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Claude Code AI assistant guidance |
| `QWEN.md` | Qwen Code AI assistant guidance |
| `README.md` | Table of contents with learning path |
| `00-Python学习大纲.md` | Full curriculum outline |

## Toolchain

| Tool | Version | Notes |
|------|---------|-------|
| Python | 3.11+ | Required for modern syntax features |
| uv | Latest | Preferred package manager |
| pytest | 7.0+ | Test framework |
| ruff | Latest | Linter and formatter |

## Language

- All prose in **Simplified Chinese**
- Code comments can be in Chinese or English
- Target audience: beginners - explain the "why", avoid jargon without definition