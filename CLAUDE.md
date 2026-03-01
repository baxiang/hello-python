# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a **Python tutorial documentation repository** containing 21 markdown files in Chinese, covering Python from beginner to advanced topics. There is no source code to build, lint, or test — the primary task is writing and editing markdown tutorial content.

## Content Organization

| Chapter Range | Category | Topics |
|---------------|----------|--------|
| 00 | Overview | Learning roadmap and prerequisites |
| 01–10 | Basics | Python fundamentals (variables, flow control, data structures, OOP, exceptions) |
| 11–15 | Intermediate | Iterators, decorators, regex, concurrency, practical projects |
| 16–20 | Specialized | uv package manager, type hints, strings, comprehensions, asyncio |

All chapters are named `NN-<Chinese title>.md`, e.g., `09-面向对象编程.md`.

## Writing Conventions

Chapters follow a consistent structure:
- **Chapter heading**: `# 第 N 章 - <Title>（详细版）`
- **Sections**: `## 第一部分 / ## 第二部分 ...` with `### N.N` subsections
- **Concept blocks**: `#### 概念说明` followed by explanation, then `#### 示例代码` with fenced Python code blocks
- **ASCII diagrams**: Used extensively for visual explanations (box-drawing characters `┌─┬─┐`)
- **Language**: All prose in Simplified Chinese; code comments/identifiers may be Chinese or English
- **Audience**: Beginners — explain the "why", avoid jargon without definition, use analogies

When editing or adding content, maintain these conventions so chapters feel uniform.

## Key Reference Files

- **README.md** — Table of contents and three-stage learning path diagram
- **00-Python学习大纲.md** — Full curriculum outline with chapter-by-chapter topic breakdown
- **14-并发编程.md** — Threading, multiprocessing, asyncio; includes detailed `await`/coroutine explanations
- **20-asyncio高级编程.md** — Event loop internals, `asyncio.Queue`, `Task`, synchronization primitives

## Toolchain (for code examples in chapters)

- **Python**: 3.11+
- **Package manager**: `uv` (preferred) or `pip`
