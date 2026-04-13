# VSCode Python 开发环境搭建

本章讲解如何使用 VSCode 搭建 2026 年工业级 Python 开发环境，包括扩展配置、settings.json、tasks.json 和 launch.json。

---

## 第一部分：基础配置

### 1.1 核心扩展

#### 概念说明

VSCode 通过扩展提供 Python 开发支持，以下是 2026 年工业级开发必备扩展。

**扩展列表：**

```
┌─────────────────────────────────────────────────────────────┐
│              VSCode Python 开发必备扩展                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   核心扩展：                                                 │
│   ┌───────────────────────────────────────────────────┐     │
│   │  Python (Microsoft)                                │     │
│   │  • 语言支持、调试、测试                             │     │
│   │  • 自动选择解释器                                   │     │
│   │  • 必装，官方维护                                   │     │
│   └───────────────────────────────────────────────────┘     │
│                                                             │
│   ┌───────────────────────────────────────────────────┐     │
│   │  Pylance (Microsoft)                               │     │
│   │  • 高性能类型检查                                   │     │
│   │  • 智能补全、签名帮助                               │     │
│   │  • 必装，替代旧版语言服务器                         │     │
│   └───────────────────────────────────────────────────┘     │
│                                                             │
│   ┌───────────────────────────────────────────────────┐     │
│   │  Python Debugger (Microsoft)                       │     │
│   │  • 调试器扩展                                       │     │
│   │  • 支持 attach、subprocess 调试                    │     │
│   └───────────────────────────────────────────────────┘     │
│                                                             │
│   代码质量扩展：                                             │
│   ┌───────────────────────────────────────────────────┐     │
│   │  Ruff (Astral)                                     │     │
│   │  • 极速 Linter + Formatter                         │     │
│   │  • 替代 Flake8 + Black + isort                    │     │
│   │  • 2026 年主流选择                                  │     │
│   └───────────────────────────────────────────────────┘     │
│                                                             │
│   ┌───────────────────────────────────────────────────┐     │
│   │  basedpyright (DetachHead)                         │     │
│   │  • 增强版类型检查                                   │     │
│   │  • 更严格的类型推断                                 │     │
│   │  • 大型项目推荐                                      │     │
│   └───────────────────────────────────────────────────┘     │
│                                                             │
│   辅助扩展：                                                 │
│   ┌───────────────────────────────────────────────────┐     │
│   │  Error Lens                                        │     │
│   │  • 行内显示错误信息                                 │     │
│   │  • 提高开发效率                                     │     │
│   └───────────────────────────────────────────────────┘     │
│                                                             │
│   ┌───────────────────────────────────────────────────┐     │
│   │  even better TOML                                  │     │
│   │  • pyproject.toml 语法支持                         │     │
│   │  • 配置文件编辑必备                                 │     │
│   └───────────────────────────────────────────────────┘     │
│                                                             │
│   ┌───────────────────────────────────────────────────┐     │
│   │  GitLens                                           │     │
│   │  • Git 增强                                         │     │
│   │  • 代码历史、作者信息                               │     │
│   └───────────────────────────────────────────────────┘     │
│                                                             │
│   ┌───────────────────────────────────────────────────┐     │
│   │  EditorConfig                                      │     │
│   │  • 跨编辑器格式统一                                 │     │
│   │  • 团队协作必备                                      │     │
│   └───────────────────────────────────────────────────┘     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**安装命令：**

```bash
# 通过命令行安装（推荐）
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension charliermarsh.ruff
code --install-extension usernamehw.errorlens
code --install-extension tamasfe.even-better-toml
code --install-extension eamodio.gitlens
code --install-extension EditorConfig.EditorConfig
```

---

### 1.2 Python 解释器配置

#### 概念说明

VSCode 需要正确选择 Python 解释器，推荐使用 uv 或 venv 管理虚拟环境。

**选择解释器：**

```
┌─────────────────────────────────────────────────────────────┐
│              Python 解释器选择流程                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   1. 快捷键：Cmd+Shift+P (Mac) / Ctrl+Shift+P (Win)         │
│                                                             │
│   2. 输入：Python: Select Interpreter                       │
│                                                             │
│   3. 选择解释器：                                            │
│      ├── 全局 Python（不推荐）                              │
│      ├── .venv/bin/python（推荐）                           │
│      ├── uv 创建的虚拟环境                                  │
│      └── conda 环境                                         │
│                                                             │
│   4. 状态栏显示当前解释器                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**创建虚拟环境：**

```bash
# 使用 uv（2026 年推荐）
uv venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# 或使用 venv
python -m venv .venv
source .venv/bin/activate
```

---

## 第二部分：settings.json 配置

### 2.1 工作区配置

#### 概念说明

`.vscode/settings.json` 用于工作区级别的配置，推荐项目级配置而非全局配置。

**工业级 settings.json：**

```json
{
  // Python 解释器路径（自动检测，可手动指定）
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",

  // 语言服务器配置
  "python.languageServer": "Pylance",
  "python.analysis.typeCheckingMode": "standard",
  "python.analysis.autoImportCompletions": true,
  "python.analysis.inlayHints.functionReturnTypes": true,
  "python.analysis.inlayHints.variableTypes": true,

  // 代码格式化（Ruff - 2026 年主流）
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll": "explicit",
      "source.organizeImports": "explicit"
    },
    "editor.rulers": [88],
    "editor.tabSize": 4
  },

  // Ruff 配置
  "ruff.lint.enable": true,
  "ruff.format.enable": true,
  "ruff.lineLength": 88,
  "ruff.lint.select": [
    "E",      // pycodestyle errors
    "F",      // Pyflakes
    "I",      // isort
    "UP",     // pyupgrade
    "B",      // flake8-bugbear
    "C4",     // flake8-comprehensions
    "SIM",    // flake8-simplify
    "TCH",    // flake8-type-checking
    "RUF"     // Ruff-specific rules
  ],
  "ruff.lint.ignore": [
    "E501"    // line too long (handled by formatter)
  ],

  // 测试配置
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "python.testing.pytestArgs": [
    "tests",
    "-v",
    "--tb=short"
  ],

  // 文件排除
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true,
    "**/.pytest_cache": true,
    "**/.ruff_cache": true,
    "**/.mypy_cache": true,
    "**/node_modules": true
  },

  // 搜索排除
  "search.exclude": {
    "**/__pycache__": true,
    "**/.venv": true,
    "**/venv": true,
    "**/.git": true
  },

  // 文件监视排除
  "files.watcherExclude": {
    "**/__pycache__/**": true,
    "**/.venv/**": true
  },

  // 终端配置
  "terminal.integrated.env.osx": {
    "PYTHONPATH": "${workspaceFolder}"
  },
  "terminal.integrated.env.windows": {
    "PYTHONPATH": "${workspaceFolder}"
  },
  "terminal.integrated.env.linux": {
    "PYTHONPATH": "${workspaceFolder}"
  },

  // Emmet 禁用（Python 文件不需要）
  "emmet.showExpandedAbbreviation": "never",

  // 自动保存
  "files.autoSave": "afterDelay",
  "files.autoSaveDelay": 1000
}
```

---

### 2.2 用户全局配置

#### 概念说明

用户级 `settings.json` 用于个人偏好设置，不影响团队协作。

**推荐全局配置：**

```json
{
  // 编辑器基础设置
  "editor.fontSize": 14,
  "editor.fontFamily": "'JetBrains Mono', 'Fira Code', Consolas, monospace",
  "editor.fontLigatures": true,
  "editor.minimap.enabled": false,
  "editor.renderWhitespace": "boundary",
  "editor.cursorBlinking": "smooth",
  "editor.smoothScrolling": true,

  // Python 全局设置
  "python.experiments.enabled": true,
  "python.installLanguageServer": true,
  "python.terminal.launchArgs": [],
  "python.globalModuleInstallation": false,

  // Git 设置
  "git.autofetch": true,
  "git.confirmSync": false,
  "git.enableSmartCommit": true,

  // 工作台设置
  "workbench.colorTheme": "One Dark Pro",
  "workbench.iconTheme": "material-icon-theme",
  "workbench.startupEditor": "none",

  // 远程开发
  "remote.SSH.remoteServerListenOnSocket": true
}
```

---

### 2.3 Python 缩进设置

#### 概念说明

Python 严格要求使用 **4 个空格** 进行缩进。如果 VSCode 的缩进设置不正确，回车后光标会跳到错误的位置。

**常见问题：**
- 回车后缩进位置不对
- 文件混用 Tab 和空格导致缩进混乱
- VSCode 自动检测到错误的缩进规则并模仿

**解决方案：**

```
┌─────────────────────────────────────────────────────────────┐
│              Python 缩进问题排查步骤                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   步骤1：检查 Auto Indent                                    │
│   • 打开设置：Ctrl+, (Mac: Cmd+,)                           │
│   • 搜索：Auto Indent                                        │
│   • Editor: Auto Indent → 设为 full 或 advanced             │
│                                                             │
│   步骤2：检查缩进方式                                         │
│   • 查看右下角状态栏                                         │
│   • 确保显示"空格：4"                                        │
│   • 如显示"制表符"，点击改为"缩进使用空格"                    │
│                                                             │
│   步骤3：禁用自动检测                                         │
│   • 搜索：Detect Indentation                                │
│   • Editor: Detect Indentation → 取消勾选                   │
│   • 强制使用设置中定义的规则                                  │
│                                                             │
│   步骤4：检查语言模式                                         │
│   • 确保右下角显示 Python（不是 Plain Text）                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**settings.json 配置：**

```json
{
    "[python]": {
        "editor.insertSpaces": true,
        "editor.tabSize": 4,
        "editor.autoIndent": "full",
        "editor.detectIndentation": false
    }
}
```

**配置说明：**

| 设置项 | 值 | 说明 |
|--------|-----|------|
| `editor.insertSpaces` | `true` | 使用空格而非 Tab |
| `editor.tabSize` | `4` | Python 标准 4 空格缩进 |
| `editor.autoIndent` | `"full"` | 回车自动跟随上一行缩进 |
| `editor.detectIndentation` | `false` | 禁用自动检测，防止模仿混乱缩进 |

**手动调整现有文件：**

如果文件已有混乱缩进，可以手动修复：

```
┌─────────────────────────────────────────────────────────────┐
│                  修复混乱缩进                                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   方法1：右下角状态栏                                         │
│   • 点击"空格/制表符"                                         │
│   • 选择"将缩进转换为空格"                                    │
│   • 或"将缩进转换为制表符"                                    │
│                                                             │
│   方法2：命令面板                                             │
│   • Ctrl+Shift+P (Mac: Cmd+Shift+P)                         │
│   • 输入：Convert Indentation to Spaces                     │
│                                                             │
│   方法3：Ruff 格式化                                          │
│   • 保存时自动格式化                                          │
│   • 或手动运行 Ruff: Format All                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 第三部分：tasks.json 配置

### 3.1 任务配置

#### 概念说明

`tasks.json` 定义常用任务的快捷执行方式，提高开发效率。

**工业级 tasks.json：**

```json
{
  "version": "2.0.0",
  "tasks": [
    // 运行当前文件
    {
      "label": "Python: Run Current File",
      "type": "shell",
      "command": "${config:python.defaultInterpreterPath}",
      "args": ["${file}"],
      "options": {
        "cwd": "${workspaceFolder}"
      },
      "group": {
        "kind": "build",
        "isDefault": true
      },
      "presentation": {
        "echo": true,
        "reveal": "always",
        "focus": false,
        "panel": "shared",
        "showReuseMessage": false,
        "clear": true
      },
      "problemMatcher": []
    },

    // 运行模块
    {
      "label": "Python: Run Module",
      "type": "shell",
      "command": "${config:python.defaultInterpreterPath}",
      "args": ["-m", "${input:moduleName}"],
      "options": {
        "cwd": "${workspaceFolder}"
      },
      "group": "build",
      "presentation": {
        "reveal": "always",
        "clear": true
      }
    },

    // pytest 运行所有测试
    {
      "label": "Python: Run All Tests",
      "type": "shell",
      "command": "${config:python.defaultInterpreterPath}",
      "args": ["-m", "pytest", "tests/", "-v", "--tb=short"],
      "options": {
        "cwd": "${workspaceFolder}"
      },
      "group": "test",
      "presentation": {
        "reveal": "always",
        "clear": true
      },
      "problemMatcher": []
    },

    // pytest 运行当前测试文件
    {
      "label": "Python: Run Current Test File",
      "type": "shell",
      "command": "${config:python.defaultInterpreterPath}",
      "args": ["-m", "pytest", "${file}", "-v", "--tb=short"],
      "options": {
        "cwd": "${workspaceFolder}"
      },
      "group": "test",
      "presentation": {
        "reveal": "always",
        "clear": true
      }
    },

    // Ruff 检查
    {
      "label": "Ruff: Check All",
      "type": "shell",
      "command": "ruff",
      "args": ["check", ".", "--fix"],
      "options": {
        "cwd": "${workspaceFolder}"
      },
      "group": "build",
      "presentation": {
        "reveal": "always",
        "clear": true
      },
      "problemMatcher": []
    },

    // Ruff 格式化
    {
      "label": "Ruff: Format All",
      "type": "shell",
      "command": "ruff",
      "args": ["format", "."],
      "options": {
        "cwd": "${workspaceFolder}"
      },
      "group": "build",
      "presentation": {
        "reveal": "silent",
        "clear": true
      }
    },

    // 类型检查
    {
      "label": "Type Check (pyright)",
      "type": "shell",
      "command": "pyright",
      "args": ["."],
      "options": {
        "cwd": "${workspaceFolder}"
      },
      "group": "build",
      "presentation": {
        "reveal": "always",
        "clear": true
      },
      "problemMatcher": []
    },

    // uv 同步依赖
    {
      "label": "uv: Sync Dependencies",
      "type": "shell",
      "command": "uv",
      "args": ["sync"],
      "options": {
        "cwd": "${workspaceFolder}"
      },
      "group": "build",
      "presentation": {
        "reveal": "always",
        "clear": true
      }
    },

    // uv 添加依赖
    {
      "label": "uv: Add Package",
      "type": "shell",
      "command": "uv",
      "args": ["add", "${input:packageName}"],
      "options": {
        "cwd": "${workspaceFolder}"
      },
      "group": "build",
      "presentation": {
        "reveal": "always",
        "clear": true
      }
    },

    // 清理缓存
    {
      "label": "Python: Clean Cache",
      "type": "shell",
      "command": "find",
      "args": [
        ".", "-type", "d",
        "-name", "__pycache__",
        "-exec", "rm", "-rf", "{}", "+"
      ],
      "options": {
        "cwd": "${workspaceFolder}"
      },
      "group": "build",
      "presentation": {
        "reveal": "silent"
      }
    }
  ],

  // 输入变量
  "inputs": [
    {
      "id": "moduleName",
      "type": "promptString",
      "description": "Enter module name to run",
      "default": "app"
    },
    {
      "id": "packageName",
      "type": "promptString",
      "description": "Enter package name to add",
      "default": ""
    }
  ]
}
```

---

### 3.2 任务快捷键

#### 概念说明

为常用任务配置快捷键，提高开发效率。

**keybindings.json（用户级）：**

```json
[
  // 运行当前文件
  {
    "key": "ctrl+shift+r",
    "command": "workbench.action.tasks.runTask",
    "args": "Python: Run Current File"
  },
  // 运行所有测试
  {
    "key": "ctrl+shift+t",
    "command": "workbench.action.tasks.runTask",
    "args": "Python: Run All Tests"
  },
  // Ruff 检查
  {
    "key": "ctrl+shift+l",
    "command": "workbench.action.tasks.runTask",
    "args": "Ruff: Check All"
  }
]
```

---

## 第四部分：launch.json 配置

### 4.1 调试配置

#### 概念说明

`launch.json` 定义调试配置，支持多种调试场景。

**工业级 launch.json：**

```json
{
  "version": "0.2.0",
  "configurations": [
    // 调试当前文件
    {
      "name": "Python: Current File",
      "type": "debugpy",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal",
      "justMyCode": true,
      "cwd": "${workspaceFolder}",
      "env": {
        "PYTHONPATH": "${workspaceFolder}"
      }
    },

    // 调试模块
    {
      "name": "Python: Module",
      "type": "debugpy",
      "request": "launch",
      "module": "app.main",
      "console": "integratedTerminal",
      "justMyCode": true,
      "cwd": "${workspaceFolder}",
      "env": {
        "PYTHONPATH": "${workspaceFolder}"
      }
    },

    // 调试 FastAPI 应用
    {
      "name": "Python: FastAPI",
      "type": "debugpy",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "app.main:app",
        "--reload",
        "--host", "0.0.0.0",
        "--port", "8000"
      ],
      "console": "integratedTerminal",
      "justMyCode": false,
      "cwd": "${workspaceFolder}",
      "env": {
        "PYTHONPATH": "${workspaceFolder}",
        "ENV": "development"
      }
    },

    // 调试 Flask 应用
    {
      "name": "Python: Flask",
      "type": "debugpy",
      "request": "launch",
      "module": "flask",
      "args": [
        "run",
        "--debug",
        "--host", "0.0.0.0",
        "--port", "5000"
      ],
      "console": "integratedTerminal",
      "justMyCode": false,
      "cwd": "${workspaceFolder}",
      "env": {
        "FLASK_APP": "app.py",
        "FLASK_DEBUG": "1",
        "PYTHONPATH": "${workspaceFolder}"
      }
    },

    // 调试 pytest
    {
      "name": "Python: pytest",
      "type": "debugpy",
      "request": "launch",
      "module": "pytest",
      "args": [
        "tests/",
        "-v",
        "--tb=short",
        "-s"  // 允许 print 输出
      ],
      "console": "integratedTerminal",
      "justMyCode": false,
      "cwd": "${workspaceFolder}"
    },

    // 调试 pytest 单个文件
    {
      "name": "Python: pytest Current File",
      "type": "debugpy",
      "request": "launch",
      "module": "pytest",
      "args": [
        "${file}",
        "-v",
        "--tb=short",
        "-s"
      ],
      "console": "integratedTerminal",
      "justMyCode": false,
      "cwd": "${workspaceFolder}"
    },

    // 附加到进程
    {
      "name": "Python: Attach",
      "type": "debugpy",
      "request": "attach",
      "connect": {
        "host": "localhost",
        "port": 5678
      }
    },

    // 远程调试
    {
      "name": "Python: Remote Attach",
      "type": "debugpy",
      "request": "attach",
      "connect": {
        "host": "${input:remoteHost}",
        "port": 5678
      },
      "pathMappings": [
        {
          "localRoot": "${workspaceFolder}",
          "remoteRoot": "/app"
        }
      ]
    },

    // 调试 Django
    {
      "name": "Python: Django",
      "type": "debugpy",
      "request": "launch",
      "program": "${workspaceFolder}/manage.py",
      "args": [
        "runserver",
        "0.0.0.0:8000",
        "--noreload"
      ],
      "console": "integratedTerminal",
      "justMyCode": false,
      "cwd": "${workspaceFolder}",
      "env": {
        "PYTHONPATH": "${workspaceFolder}"
      }
    }
  ],

  "inputs": [
    {
      "id": "remoteHost",
      "type": "promptString",
      "description": "Enter remote host IP",
      "default": "localhost"
    }
  ]
}
```

---

### 4.2 调试技巧

#### 概念说明

掌握调试技巧可以快速定位问题。

**常用调试操作：**

```
┌─────────────────────────────────────────────────────────────┐
│                  VSCode 调试快捷键                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   启动调试：                                                 │
│   • F5：开始调试                                            │
│   • Ctrl+F5：运行不调试                                     │
│   • Shift+F5：停止调试                                      │
│                                                             │
│   断点操作：                                                 │
│   • F9：切换断点                                            │
│   • 条件断点：右键 → Add Conditional Breakpoint             │
│   • 日志点：右键 → Add Logpoint                             │
│                                                             │
│   单步执行：                                                 │
│   • F10：单步跳过 (Step Over)                               │
│   • F11：单步进入 (Step Into)                               │
│   • Shift+F11：单步跳出 (Step Out)                          │
│                                                             │
│   变量查看：                                                 │
│   • 左侧 VARIABLES 面板                                     │
│   • WATCH 面板添加表达式                                    │
│   • 调试控制台执行代码                                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**条件断点示例：**

```python
# 只在 i > 100 时触发断点
for i in range(1000):
    result = process(i)  # 条件断点：i > 100
```

---

## 第五部分：项目配置文件

### 5.1 pyproject.toml

#### 概念说明

`pyproject.toml` 是 Python 项目的统一配置文件，2026 年工业级标准。

**示例配置：**

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "A Python project"
authors = [{name = "Author", email = "author@example.com"}]
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.115.0",
    "pydantic>=2.10.0",
    "uvicorn>=0.34.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=6.0.0",
    "ruff>=0.9.0",
    "pyright>=1.1.0",
    "basedpyright>=1.0.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

# Ruff 配置
[tool.ruff]
target-version = "py311"
line-length = 88
src = ["src", "tests"]

[tool.ruff.lint]
select = [
    "E",      # pycodestyle errors
    "F",      # Pyflakes
    "I",      # isort
    "UP",     # pyupgrade
    "B",      # flake8-bugbear
    "C4",     # flake8-comprehensions
    "SIM",    # flake8-simplify
    "TCH",    # flake8-type-checking
    "RUF",    # Ruff-specific rules
]
ignore = ["E501"]

[tool.ruff.lint.isort]
known-first-party = ["my_project"]

[tool.ruff.format]
docstring-code-format = true

# pytest 配置
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = "-v --tb=short --strict-markers"
markers = [
    "slow: marks tests as slow",
    "integration: marks integration tests",
]

# pyright 配置
[tool.pyright]
typeCheckingMode = "standard"
pythonVersion = "3.11"
pythonPlatform = "All"
reportMissingImports = true
reportMissingTypeStubs = false
exclude = ["**/__pycache__", "**/.venv"]
```

---

### 5.2 EditorConfig

#### 概念说明

`.editorconfig` 跨编辑器统一格式，团队协作必备。

**配置示例：**

```ini
# EditorConfig - 跨编辑器格式统一
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true

[*.py]
indent_style = space
indent_size = 4
max_line_length = 88

[*.{json,yaml,yml,toml}]
indent_style = space
indent_size = 2

[*.md]
trim_trailing_whitespace = false
max_line_length = off

[Makefile]
indent_style = tab
```

---

### 5.3 .gitignore

#### 概念说明

Python 项目标准 `.gitignore` 配置。

**配置示例：**

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
.venv/
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
.nox/

# Type checking
.mypy_cache/
.pytype/
.ruff_cache/

# Distribution
*.manifest
*.spec

# Logs
*.log
logs/

# Local config
.env
.env.local
*.local

# OS
.DS_Store
Thumbs.db
```

---

## 第六部分：完整项目结构

### 6.1 推荐项目结构

#### 概念说明

2026 年工业级 Python 项目标准结构。

```
┌─────────────────────────────────────────────────────────────┐
│              Python 项目标准结构                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   my-project/                                               │
│   ├── .vscode/                                              │
│   │   ├── settings.json     # 工作区配置                    │
│   │   ├── tasks.json        # 任务配置                      │
│   │   ├── launch.json       # 调试配置                      │
│   │   └── extensions.json   # 推荐扩展                      │
│   │                                                         │
│   ├── .venv/                # 虚拟环境                      │
│   ├── src/                  # 源代码                        │
│   │   └── my_project/                                       │
│   │       ├── __init__.py                                   │
│   │       ├── main.py                                       │
│   │       └── core/                                         │
│   │           └ __init__.py                                 │
│   │           └ module.py                                   │
│   │                                                         │
│   ├── tests/                # 测试                          │
│   │   ├── __init__.py                                       │
│   │   ├── conftest.py                                       │
│   │   └ test_main.py                                        │
│   │                                                         │
│   ├── pyproject.toml        # 项目配置                      │
│   ├── .editorconfig         # 编辑器配置                    │
│   ├── .gitignore            # Git 忽略                      │
│   ├── README.md             # 项目说明                      │
│   └ LICENSE                  # 许可证                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### 6.2 extensions.json

#### 概念说明

`.vscode/extensions.json` 定义团队推荐扩展。

**配置示例：**

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "charliermarsh.ruff",
    "usernamehw.errorlens",
    "tamasfe.even-better-toml",
    "eamodio.gitlens",
    "EditorConfig.EditorConfig"
  ],
  "unwantedRecommendations": [
    "ms-python.black-formatter",
    "ms-python.flake8",
    "ms-python.isort"
  ]
}
```

---

## 第七部分：常见问题排查

### 7.1 终端未激活虚拟环境

**症状**：终端打开后没有自动激活 `.venv`。

**解决方案**：
```json
// settings.json
{
  "python.terminal.activateEnvironment": true
}
```

或手动激活：
```bash
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

### 7.2 导入报错 (Missing imports)

**症状**：代码能运行，但 VSCode 显示 "Import could not be resolved"。

**原因**：解释器选择错误或 Pylance 未识别。

**解决方案**：
1. 检查右下角状态栏的 Python 版本。
2. `Cmd+Shift+P` -> `Python: Select Interpreter`。
3. 确保 `python.defaultInterpreterPath` 正确。

### 7.3 Ruff 不生效

**症状**：Ruff 扩展安装后，代码没有自动格式化。

**解决方案**：
```json
// settings.json
{
  "editor.formatOnSave": true,
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff"
  }
}
```

### 7.4 调试时找不到模块

**症状**：调试时报 `ModuleNotFoundError`。

**解决方案**：
在 `launch.json` 中添加 `env`：
```json
{
  "name": "Python: Current File",
  "type": "debugpy",
  "request": "launch",
  "program": "${file}",
  "env": {
    "PYTHONPATH": "${workspaceFolder}/src"
  }
}
```

---

## 本章小结

```
┌─────────────────────────────────────────────────────────────┐
│              VSCode Python 开发环境 知识要点                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   核心扩展：                                                 │
│   ✓ Python + Pylance（语言支持）                            │
│   ✓ Ruff（Linter + Formatter，2026 主流）                   │
│   ✓ Error Lens（行内错误）                                  │
│   ✓ GitLens（Git 增强）                                     │
│                                                             │
│   settings.json：                                            │
│   ✓ python.defaultInterpreterPath                           │
│   ✓ Ruff 格式化配置                                         │
│   ✓ pytest 测试配置                                         │
│                                                             │
│   tasks.json：                                               │
│   ✓ 运行文件、运行测试                                       │
│   ✓ Ruff 检查、类型检查                                     │
│   ✓ uv 同步依赖                                             │
│                                                             │
│   launch.json：                                              │
│   ✓ 调试当前文件                                             │
│   ✓ FastAPI/Flask/Django 调试                               │
│   ✓ pytest 调试                                             │
│   ✓ 远程附加调试                                             │
│                                                             │
│   项目配置：                                                 │
│   ✓ pyproject.toml（统一配置）                              │
│   ✓ .editorconfig（格式统一）                               │
│   ✓ .gitignore（版本控制）                                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```