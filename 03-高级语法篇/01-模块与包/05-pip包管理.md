# pip 包管理（详细版）

> Python 3.11+

## 第一部分：pip 基础

### 5.1 什么是 pip

#### 实际场景

你想用 Python 做数据分析，听说有个叫 `pandas` 的库很好用。但你的 Python 里没有这个库，直接 `import pandas` 会报错 `ModuleNotFoundError`。

**问题：如何安装别人开发的 Python 库？**

#### 概念说明

pip 是 Python 的包管理工具，用于安装和管理第三方库。

> **注意：** 2026年起，推荐使用 **uv** 作为包管理工具（速度快10-100倍）。本章保留pip介绍，用于维护老项目。

---

### 5.2 pip vs uv：如何选择

| 特性 | pip | uv |
|------|-----|-----|
| **速度** | 基准 | 10-100倍快 ⚡ |
| **依赖解析** | 慢，可能冲突 | 快速准确 ✅ |
| **虚拟环境** | 需要venv | 内置支持 ✅ |
| **锁文件** | 需要pip-tools | 自动生成 ✅ |
| **Python版本管理** | 不支持 | 支持 ✅ |
| **兼容性** | 广泛 | 广泛 |

### 何时使用 pip
- 维护老项目（已使用pip）
- CI/CD环境已配置pip
- 教学演示基础概念

### 何时使用 uv（推荐）
- 新项目 ✅
- 需要快速安装依赖
- 追求现代工具链
- 需要Python版本管理

---

#### 基本命令

```bash
# 推荐：使用 uv 安装包（更快）
uv add pandas numpy matplotlib

# 传统：使用 pip 安装包
pip install pandas numpy matplotlib

# 查看已安装的包
pip list

# 导出依赖列表
pip freeze > requirements.txt
```

---

## 第二部分：安装包

### 5.3 基本安装

```bash
# 推荐：使用 uv 安装（更快）
uv add requests

# 传统：使用 pip 安装
pip install requests

# 安装指定版本
uv add requests==2.28.0
pip install requests==2.28.0

# 安装版本范围
pip install "requests>=2.28.0,<3.0.0"

# 安装兼容版本
pip install requests~=2.28.0  # >=2.28.0, <2.29.0
```

### 5.4 从不同来源安装

```bash
# 从 PyPI 安装（默认）
pip install requests

# 从指定索引安装（国内镜像加速）
pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple

# 从 Git 仓库安装
pip install git+https://github.com/psf/requests.git

# 从本地目录安装
pip install ./my-package

# 从 requirements.txt 安装
pip install -r requirements.txt
uv pip install -r requirements.txt
```

### 5.5 安装选项

```bash
# 升级已安装的包
pip install --upgrade requests

# 安装开发版本
pip install --pre requests

# 只安装，不缓存
pip install --no-cache-dir requests

# 安装到用户目录
pip install --user requests
```

---

## 第三部分：卸载包

### 5.6 卸载命令

```bash
# 卸载包
pip uninstall requests

# 卸载多个包
pip uninstall requests numpy pandas

# 卸载时不确认
pip uninstall -y requests

# 卸载所有包（谨慎使用）
pip freeze | xargs pip uninstall -y
```

---

## 第四部分：查看包信息

### 5.7 查看命令

```bash
# 查看已安装的包
pip list

# 查看可升级的包
pip list --outdated

# 查看包详情
pip show requests

# 查看包的依赖
pip show requests

# 查看包的安装位置
pip show -f requests

# 搜索包（已禁用，使用 pypi.org）
# pip search requests
```

---

## 第五部分：依赖管理

### 5.8 requirements.txt

```bash
# 推荐：使用 uv 自动管理
uv add requests numpy pandas
# 自动生成 uv.lock 和 pyproject.toml

# 传统：pip + requirements.txt
pip freeze > requirements.txt

# 从 requirements.txt 安装
pip install -r requirements.txt
uv pip install -r requirements.txt
```

**requirements.txt 格式：**

```txt
# 注释
requests==2.28.0
numpy>=1.21.0
pandas>=1.3.0,<2.0.0
flask>=2.0

# 从 Git 安装
git+https://github.com/user/repo.git@main#egg=package

# 从本地安装
./local-package
```

### 5.9 版本 specifier

| 符号 | 含义 | 示例 |
|------|------|------|
| `==` | 精确版本 | `requests==2.28.0` |
| `!=` | 不等于 | `requests!=2.28.0` |
| `>=` | 大于等于 | `requests>=2.28.0` |
| `<=` | 小于等于 | `requests<=2.28.0` |
| `>` | 大于 | `requests>2.28.0` |
| `<` | 小于 | `requests<2.28.0` |
| `~=` | 兼容版本 | `requests~=2.28.0` |
| `===` | 任意版本 | `requests===2.28.0` |

---

## 第六部分：虚拟环境

### 5.10 venv（Python 内置）

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# macOS/Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate

# 退出虚拟环境
deactivate

# 删除虚拟环境
rm -rf .venv
```

### 5.11 virtualenv

```bash
# 安装
pip install virtualenv

# 创建虚拟环境
virtualenv .venv

# 指定 Python 版本
virtualenv -p python3.11 .venv
```

### 5.12 使用 uv（推荐）

```bash
# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 创建新项目（自动创建虚拟环境）
uv init my-project
cd my-project

# 添加依赖
uv add requests pandas

# 运行脚本
uv run python main.py

# 或使用 uv pip 兼容模式
uv venv
uv pip install requests
uv pip install -r requirements.txt
```

---

## 第七部分：配置 pip

### 5.13 配置文件

```bash
# 查看 pip 配置
pip config list

# 设置配置
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 配置文件位置
# Unix: ~/.config/pip/pip.conf
# Windows: %APPDATA%\pip\pip.ini
```

### 5.14 pip.conf 示例

```ini
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
trusted-host = pypi.tuna.tsinghua.edu.cn
timeout = 60

[install]
no-cache-dir = true
```

### 5.15 使用国内镜像

```bash
# 临时使用
pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple

# 永久配置
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

**常用国内镜像：**

| 镜像 | 地址 |
|------|------|
| 清华 | https://pypi.tuna.tsinghua.edu.cn/simple |
| 阿里云 | https://mirrors.aliyun.com/pypi/simple |
| 中科大 | https://pypi.mirrors.ustc.edu.cn/simple |
| 豆瓣 | https://pypi.douban.com/simple |

---

## 第八部分：迁移到 uv

### 5.16 安装 uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 5.17 基本使用对比

```bash
# pip 方式
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
pip install requests
pip freeze > requirements.txt
python main.py

# uv 方式（推荐）
uv init my-project
cd my-project
uv add requests
uv run python main.py
```

### 5.18 pip 命令 vs uv 命令

| 操作 | pip | uv |
|------|-----|-----|
| 创建项目 | 手动 | `uv init project` |
| 创建虚拟环境 | `python -m venv .venv` | 自动创建 |
| 安装包 | `pip install pkg` | `uv add pkg` |
| 安装开发依赖 | `pip install -e .` | `uv add --dev pkg` |
| 安装所有依赖 | `pip install -r requirements.txt` | `uv sync` |
| 运行脚本 | `python script.py` | `uv run python script.py` |
| 导出依赖 | `pip freeze > requirements.txt` | 自动生成 `uv.lock` |

### 5.19 从 pip 项目迁移

如果你有一个使用 pip 的老项目：

```bash
# 1. 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. 在项目目录初始化
cd your-project
uv init

# 3. 从 requirements.txt 安装依赖
uv add $(cat requirements.txt | tr '\n' ' ')

# 4. 使用 uv 运行
uv run python main.py
```

### 5.20 uv 的优势

1. **速度快** - 比 pip 快10-100倍
2. **自动管理虚拟环境** - 无需手动创建
3. **锁定依赖** - 自动生成 `uv.lock` 确保可重复性
4. **Python版本管理** - `uv python install 3.11`
5. **统一工具链** - 替代 pip, venv, pip-tools 等

### 5.21 何时继续使用 pip

- 维护不需要频繁更新的老项目
- 团队工作流已深度集成 pip
- 需要使用 pip 特有的插件或功能

对于新项目，**强烈推荐使用 uv**。

---

## 本章小结

```
┌─────────────────────────────────────────────────────────────┐
│                      pip 包管理 知识要点                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   安装包：                                                   │
│   ✓ pip install package                                     │
│   ✓ pip install package==version                            │
│   ✓ pip install -r requirements.txt                         │
│                                                             │
│   卸载包：                                                   │
│   ✓ pip uninstall package                                   │
│                                                             │
│   查看信息：                                                 │
│   ✓ pip list                                                │
│   ✓ pip show package                                        │
│   ✓ pip freeze > requirements.txt                           │
│                                                             │
│   虚拟环境：                                                 │
│   ✓ python -m venv .venv                                    │
│   ✓ source .venv/bin/activate                               │
│                                                             │
│   配置：                                                     │
│   ✓ pip config set                                          │
│   ✓ 国内镜像加速                                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```