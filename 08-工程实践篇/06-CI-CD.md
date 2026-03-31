# 第 06 章 - CI/CD 与自动化

> 持续集成和持续部署是现代软件开发的标配，本章介绍 Python 项目的 CI/CD 最佳实践。

---

## 第一部分 - GitHub Actions 基础

### 1.1 工作流文件结构

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

# 触发条件
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 2 * * *'  # 每天 UTC 2 点运行
  workflow_dispatch:  # 允许手动触发

# 环境变量
env:
  PYTHON_VERSION: "3.11"

# 任务定义
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install uv
        uses: astral-sh/setup-uv@v3
      
      - name: Install dependencies
        run: uv sync --dev
      
      - name: Run linter
        run: uv run ruff check .

  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
        os: [ubuntu-latest, macos-latest, windows-latest]
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Install uv
        uses: astral-sh/setup-uv@v3
      
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: uv sync --dev
      
      - name: Run tests
        run: uv run pytest --cov=src/my_package --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml
          flags: unittests

  build:
    needs: [lint, test]
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Install uv
        uses: astral-sh/setup-uv@v3
      
      - name: Build package
        run: uv run python -m build
      
      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/

  publish:
    needs: build
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Install uv
        uses: astral-sh/setup-uv@v3
      
      - name: Download artifacts
        uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/
      
      - name: Publish to PyPI
        env:
          PYPI_TOKEN: ${{ secrets.PYPI_TOKEN }}
        run: |
          uv run twine upload dist/*
```

### 1.2 常用触发条件

```yaml
on:
  # 推送触发
  push:
    branches: [main, develop]
    tags: ['v*']
    paths:
      - 'src/**'
      - 'tests/**'
      - 'pyproject.toml'
  
  # PR 触发
  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened]
  
  # 定时触发
  schedule:
    - cron: '0 0 * * *'      # 每天 UTC 0 点
    - cron: '0 */6 * * *'    # 每 6 小时
    - cron: '30 8 * * 1-5'   # 工作日早上 8:30
  
  # 手动触发
  workflow_dispatch:
    inputs:
      environment:
        description: '部署环境'
        required: true
        default: 'staging'
        type: choice
        options:
          - staging
          - production
  
  # 其他工作流完成时触发
  workflow_run:
    workflows: ["CI"]
    types: [completed]
```

---

## 第二部分 - 缓存与优化

### 2.1 缓存依赖

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Install uv
        uses: astral-sh/setup-uv@v3
      
      # 缓存 uv 依赖
      - name: Cache uv dependencies
        uses: actions/cache@v4
        with:
          path: |
            ~/.cache/uv
            .venv
          key: ${{ runner.os }}-uv-${{ hashFiles('uv.lock') }}
          restore-keys: |
            ${{ runner.os }}-uv-
      
      - name: Install dependencies
        run: uv sync --dev
      
      - name: Run tests
        run: uv run pytest
```

### 2.2 矩阵构建优化

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
        os: [ubuntu-latest, macos-latest, windows-latest]
      fail-fast: false  # 一个失败，其他继续
      max-parallel: 6   # 最大并行数
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Install uv
        uses: astral-sh/setup-uv@v3
      
      - name: Run tests
        run: uv run pytest
```

---

## 第三部分 - 发布自动化

### 3.1 语义化版本发布

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*.*.*'

permissions:
  contents: write
  id-token: write  # 用于 PyPI 可信发布

jobs:
  release:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Install uv
        uses: astral-sh/setup-uv@v3
      
      - name: Build package
        run: uv run python -m build
      
      # 创建 GitHub Release
      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          generate_release_notes: true
          files: dist/*
      
      # 发布到 PyPI
      - name: Publish to PyPI
        uses: pypa/gh-action-pypi-publish@release/v1
```

### 3.2 自动版本管理

```yaml
# .github/workflows/bump-version.yml
name: Bump Version

on:
  workflow_dispatch:
    inputs:
      bump_type:
        description: '版本类型'
        required: true
        default: 'patch'
        type: choice
        options:
          - major
          - minor
          - patch

jobs:
  bump:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Install uv
        uses: astral-sh/setup-uv@v3
      
      - name: Bump version
        run: |
          # 使用 bump2version 或自定义脚本
          uv run bump-my-version bump ${{ github.event.inputs.bump_type }}
      
      - name: Commit and push
        run: |
          git config --local user.email "github-actions[bot]@users.noreply.github.com"
          git config --local user.name "github-actions[bot]"
          git add pyproject.toml
          git commit -m "chore: bump version [skip ci]"
          git push --follow-tags
```

---

## 第四部分 - 部署自动化

### 4.1 Docker 部署

```yaml
# .github/workflows/docker.yml
name: Docker Build

on:
  push:
    branches: [main]
    tags: ['v*.*.*']

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha
      
      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### 4.2 Dockerfile 示例

```dockerfile
# Dockerfile
FROM python:3.11-slim

# 安装 uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# 复制项目文件
COPY pyproject.toml uv.lock ./
COPY src/ ./src/

# 安装依赖
RUN uv sync --frozen --no-dev

# 设置环境变量
ENV PATH="/app/.venv/bin:$PATH"

# 运行应用
CMD ["python", "-m", "my_package"]
```

---

## 第五部分 - 通知与监控

### 5.1 Slack 通知

```yaml
# .github/workflows/notify.yml
name: Notify

on:
  workflow_run:
    workflows: ["CI/CD Pipeline"]
    types: [completed]

jobs:
  notify:
    runs-on: ubuntu-latest
    if: ${{ always() }}
    
    steps:
      - name: Send Slack notification
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "${{ github.workflow }} ${{ job.status }}",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "*Workflow:* ${{ github.workflow }}\n*Status:* ${{ job.status }}\n*Repository:* ${{ github.repository }}\n*Commit:* ${{ github.sha }}"
                  }
                }
              ]
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

### 5.2 邮件通知

```yaml
# .github/workflows/notify-email.yml
name: Notify Email

on:
  workflow_run:
    workflows: ["CI/CD Pipeline"]
    types: [completed]

jobs:
  notify:
    runs-on: ubuntu-latest
    if: failure()
    
    steps:
      - name: Send email notification
        uses: dawidd6/action-send-mail@v3
        with:
          server_address: smtp.gmail.com
          server_port: 587
          username: ${{ secrets.SMTP_USERNAME }}
          password: ${{ secrets.SMTP_PASSWORD }}
          subject: 'CI/CD Pipeline Failed - ${{ github.repository }}'
          to: team@example.com
          body: |
            Workflow: ${{ github.workflow }}
            Status: Failed
            Repository: ${{ github.repository }}
            Commit: ${{ github.sha }}
            Run URL: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
```

---

## 最佳实践清单

### ✅ 必须遵守

1. 所有 PR 必须通过 CI 检查
2. 主分支必须保护，要求 CI 通过才能合并
3. 敏感信息必须使用 Secrets

### ✅ 推荐做法

1. 使用矩阵测试多版本兼容性
2. 缓存依赖加速构建
3. 使用可信发布到 PyPI
4. 失败时发送通知
5. 定期清理旧的工作流运行记录
