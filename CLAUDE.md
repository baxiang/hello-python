# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a **Python tutorial documentation repository** containing 20 markdown files in Chinese covering Python from beginner to advanced topics. There is no source code to build, lint, or test.

## File Structure

```
hello-python/
├── README.md               # Main navigation and table of contents
├── CLAUDE.md              # This file
├── 00-Python 学习大纲.md
├── 01-15              # Core tutorials (15 chapters)
├── 16-20              # Advanced/specialized topics (5 chapters)
└── ...
```

## Content Organization

| Chapter Range | Category | Description |
|---------------|----------|-------------|
| 00 | Overview | Learning roadmap |
| 01-10 | Basics | Python fundamentals |
| 11-15 | Intermediate | Advanced concepts and practical projects |
| 16-20 | Specialized | Deep dives (uv, type hints, strings, comprehensions, asyncio) |

## Key Files

- **README.md** - Main entry point with complete table of contents and navigation
- **00-Python 学习大纲.md** - Learning path and prerequisites
- **14-并发编程.md** - Concurrency (threading, multiprocessing, asyncio with detailed await explanation and coroutines)
- **20-asyncio 高级编程.md** - Advanced asyncio (event loop, Queue, Task management, synchronisation primitives)

## Toolchain (for code examples)

- **Python**: 3.11+
- **Package Manager**: `uv` (preferred) or `pip`
- **Editor**: VS Code with Python extension

## Common Commands

```bash
# Run a Python script from examples
python script.py

# Install dependencies for examples
uv pip install <package>
```
