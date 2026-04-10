# VSCode Python 工程开发环境配置指南

> **摘要**：本文档介绍如何使用 Visual Studio Code (VSCode) 搭建专业级 Python 开发环境，涵盖扩展安装、解释器配置、代码规范、调试技巧及远程开发。

---

## 1. 基础准备

### 1.1 安装 VSCode
从官网下载并安装 [Visual Studio Code](https://code.visualstudio.com/)。

### 1.2 安装 Python 官方扩展
在扩展面板 (`Ctrl+Shift+X` / `Cmd+Shift+X`) 搜索并安装：
*   **Python** (by Microsoft)：核心支持，提供智能补全、调试、环境管理。
*   **Pylance**：高性能语言服务器，提供静态类型检查和快速补全。

### 1.3 常用辅助插件
| 插件名 | 说明 |
| :--- | :--- |
| **Ruff** | 极速的 Python Linter 和 Formatter（推荐替代 Flake8/isort/Black） |
| **Error Lens** | 在代码行内直接显示错误和警告信息 |
| **GitLens** | 增强 Git 功能，查看代码行级变更记录 |
| **Todo Tree** | 高亮显示代码中的 TODO/FIXME 标签 |
| **Chinese Language Pack** | 中文界面支持 |

---

## 2. 项目工作区配置

VSCode 的配置分为三个级别：**用户 (User)** > **工作区 (Workspace)** > **文件夹 (Folder)**。
推荐使用 **工作区配置** (`.vscode/settings.json`)，以便将设置随项目代码一同提交到 Git。

### 2.1 创建配置文件
在项目根目录创建 `.vscode` 文件夹和 `settings.json`：
```
.
├── .vscode
│   ├── settings.json
│   ├── launch.json
│   └── tasks.json
└── src/
```

### 2.2 settings.json 核心配置示例
```json
{
  // 1. Python 环境设置
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.terminal.activateEnvironment": true,
  
  // 2. 代码格式化与规范 (使用 Ruff)
  "editor.defaultFormatter": "charliermarsh.ruff",
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll.ruff": "explicit",
      "source.organizeImports.ruff": "explicit"
    }
  },
  
  // 3. Linting 设置
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  
  // 4. 编辑器体验
  "editor.rulers": [88],
  "editor.tabSize": 4,
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true,
  
  // 5. 排除不需要的文件
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true,
    "**/.pytest_cache": true,
    "**/.venv": true
  }
}
```

---

## 3. Python 解释器管理

### 3.1 切换解释器
*   **快捷键**：`Ctrl+Shift+P` (Win/Linux) / `Cmd+Shift+P` (Mac) -> `Python: Select Interpreter`
*   **状态栏**：点击右下角的 Python 版本号进行切换。

### 3.2 自动发现虚拟环境
VSCode 会自动识别常见位置（`.venv`, `env`, `venv`）的虚拟环境。如果未识别，可在 `settings.json` 中配置：
```json
{
  "python.venvPath": "${workspaceFolder}/.venv"
}
```

---

## 4. 调试配置 (launch.json)

通过 `.vscode/launch.json` 定义调试行为。按 `F5` 开始调试。

### 4.1 常见调试模式

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: Current File",
      "type": "debugpy",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "justMyCode": true
    },
    {
      "name": "Python: FastAPI / Uvicorn",
      "type": "debugpy",
      "request": "launch",
      "module": "uvicorn",
      "args": ["app.main:app", "--reload"],
      "console": "integratedTerminal"
    },
    {
      "name": "Python: Pytest - Current File",
      "type": "debugpy",
      "request": "launch",
      "module": "pytest",
      "args": ["${file}", "-v"],
      "console": "integratedTerminal"
    },
    {
      "name": "Python: Django",
      "type": "debugpy",
      "request": "launch",
      "program": "${workspaceFolder}/manage.py",
      "args": ["runserver"],
      "django": true
    }
  ]
}
```

### 4.2 调试技巧
*   **断点**：点击行号左侧添加红点。
*   **条件断点**：右键断点 -> `编辑断点` -> 输入条件（如 `x > 10`），仅在条件满足时暂停。
*   **日志点**：右键断点 -> `添加日志消息`，输入 `{variable}` 可在不暂停程序的情况下打印日志。

---

## 5. 任务自动化 (tasks.json)

使用 `.vscode/tasks.json` 管理常用脚本。

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Run Tests",
      "type": "shell",
      "command": "pytest",
      "group": { "kind": "test", "isDefault": true },
      "problemMatcher": []
    },
    {
      "label": "Format Code",
      "type": "shell",
      "command": "ruff",
      "args": ["format", "."],
      "group": "build"
    },
    {
      "label": "Lint Code",
      "type": "shell",
      "command": "ruff",
      "args": ["check", "."],
      "group": "build"
    }
  ]
}
```
*   **运行任务**：`Ctrl+Shift+P` / `Cmd+Shift+P` -> `Tasks: Run Task` 或 `Ctrl+Shift+B` / `Cmd+Shift+B` 运行构建任务。

---

## 6. 远程开发

VSCode 强大的远程开发能力：

1.  **Remote - SSH**：直接连接远程服务器（如 Linux 虚拟机、云主机），编辑代码就像在本地一样，无需 SFTP 同步。
2.  **Dev Containers**：使用 Docker 容器作为开发环境，保证团队环境一致性。
    *   需安装 **Dev Containers** 扩展。
    *   项目根目录添加 `.devcontainer/devcontainer.json` 和 `Dockerfile`。
3.  **WSL (Windows Subsystem for Linux)**：在 Windows 上无缝使用 Linux 环境进行开发。

---

## 7. 常用快捷键清单

| 快捷键 (Win/Linux) | 快捷键 (Mac) | 说明 |
| :--- | :--- | :--- |
| `Ctrl+Shift+P` | `Cmd+Shift+P` | 打开命令面板 |
| `Ctrl+P` | `Cmd+P` | 快速打开文件 |
| `F12` / `Ctrl+Click` | `F12` / `Cmd+Click` | 跳转到定义 |
| `Alt+Click` | `Option+Click` | 多光标编辑 |
| `Shift+Alt+F` | `Shift+Option+F` | 格式化代码 |
| `Ctrl+/` | `Cmd+/` | 注释/取消注释 |
| `Ctrl+D` | `Cmd+D` | 选中下一个相同词 |
| `F5` | `F5` | 开始调试 |
| `F9` | `F9` | 切换断点 |

---

## 8. 常见问题排查

*   **终端未激活虚拟环境**：
    *   确保 `settings.json` 中 `"python.terminal.activateEnvironment": true`。
    *   或者在终端手动运行 `source .venv/bin/activate`。
*   **导入报错 (Missing imports)**：
    *   VSCode 找不到第三方库通常是因为解释器选错了。
    *   检查 `settings.json` 中的 `python.defaultInterpreterPath` 或重新选择解释器。
    *   如果是 Pylint 报错但代码能运行，尝试将 Pylint 的 Python Path 设置为与项目解释器一致。
