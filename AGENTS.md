# AGENTS.md

## Architecture

**Multi-project monorepo** — no root-level Python config. Each project has its own `pyproject.toml`.

```
<章节>/<子目录>/<项目>/
├── pyproject.toml            # hatchling build
├── app/                      # Source (43/49 projects)
├── tests/                    # pytest (38/49 projects, ~110 test files total)
└── uv.lock                   # If deps installed (32/49 projects)
```

- All 49 projects use hatchling. 43 use `packages = ["app"]`, 1 uses `processor`, 1 uses `analyzer`, 1 uses `src/`, 3 have no explicit package.
- 26/49 projects have `[tool.ruff]` (line-length 88, py313, rules: E,F,I,N,W,UP,B,SIM). Projects without ruff config have no lint setup.
- 12 projects use Tsinghua PyPI mirror. 5 use `pytest-asyncio` with `asyncio_mode = "auto"`.
- Dev deps: 13 use `[dependency-groups]`, 6 use `[project.optional-dependencies]`. Prefer `[dependency-groups]` with `uv sync --group dev`.
- Some projects (Flask, FastAPI, functions_demo) have `.venv/` tracked in git — `.gitignore` is missing `/.venv/`. Avoid counting those files as project code.

## Commands

**Always cd into the project directory first — nothing works from root:**

```bash
cd <path/to/project>
uv run pytest                         # Run all tests
uv run pytest tests/test_x.py         # Single test file
uv run pytest -k "test_name"          # Run specific test
uv run ruff check .                   # Lint (only if [tool.ruff] exists)
uv run ruff check --fix .             # Auto-fix
uv run ruff format .                  # Format
uv run mypy app/                      # Type check (if [tool.mypy] exists)
uv run uvicorn app.main:app --reload  # FastAPI projects
uv add <package>                      # Add dependency
```

**VitePress docs site** (root-level, uses npm):

```bash
npm run docs:dev      # Start dev server
npm run docs:build    # Build for production
```

## Sections

Actual directory names (`find . -maxdepth 1 -type d`):

| Dir | Topics |
|-----|--------|
| `1-basics/` | Python入门、基础语法、字符串、数据结构 |
| `2-core/` | 函数、OOP、异常、迭代器、装饰器、类型提示 |
| `3-advanced/` | 模块与包、标准库、并发与异步 |
| `4-web/` | Flask、FastAPI |
| `5-ml/` | 基础概念、数据预处理、监督/无监督学习、模型优化 |
| `6-deep-learning/` | PyTorch、CNN、RNN |
| `7-projects/` | Level 1-4 项目（入门→专业级） |
| `8-engineering/` | 代码质量、项目管理、运维监控、开发技巧 |

## CI

- Documentation quality check only — no Python test CI.
- VitePress builds and deploys to GitHub Pages on push to `main`.

## References

- **CLAUDE.md** — Chinese markdown writing conventions (chapter structure, ASCII diagrams, audience level).
- **README.md** — Full learning roadmap with all chapter outlines.
- **`docs/技术内容编写规范.md`** — L1/L2/L3 content architecture, code standards, testing guidelines, type checking requirements.
