# pip 包管理

本章讲解 pip 包管理工具的使用，包括安装、卸载、依赖管理等操作。

---

## pip 基础

### 什么是 pip

pip 是 Python 的包管理工具，用于安装和管理第三方库。

```bash
# 查看 pip 版本
pip --version

# 查看 pip 帮助
pip help

# 查看 pip 配置
pip config list
```

---

## 安装包

### 基本安装

```bash
# 安装最新版本
pip install requests

# 安装指定版本
pip install requests==2.28.0

# 安装最低版本
pip install requests>=2.28.0

# 安装版本范围
pip install "requests>=2.28.0,<3.0.0"

# 安装兼容版本
pip install requests~=2.28.0  # >=2.28.0, <2.29.0
```

### 从不同来源安装

```bash
# 从 PyPI 安装（默认）
pip install requests

# 从指定索引安装
pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple

# 从 Git 仓库安装
pip install git+https://github.com/psf/requests.git

# 从本地目录安装
pip install ./my-package

# 从压缩包安装
pip install ./package.tar.gz

# 从 requirements.txt 安装
pip install -r requirements.txt
```

### 安装选项

```bash
# 升级已安装的包
pip install --upgrade requests

# 安装开发版本
pip install --pre requests

# 只安装，不缓存
pip install --no-cache-dir requests

# 安装到用户目录
pip install --user requests

# 忽略已安装的依赖
pip install --ignore-installed requests
```

---

## 卸载包

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

## 查看包信息

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

## 依赖管理

### requirements.txt

```bash
# 导出当前环境的所有包
pip freeze > requirements.txt

# 导出时指定格式
pip freeze --format=freeze > requirements.txt

# 从 requirements.txt 安装
pip install -r requirements.txt

# 安装时忽略失败
pip install -r requirements.txt --ignore-errors
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

### 版本 specifier

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

## 虚拟环境

### venv（推荐）

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

### virtualenv

```bash
# 安装
pip install virtualenv

# 创建虚拟环境
virtualenv .venv

# 指定 Python 版本
virtualenv -p python3.11 .venv
```

### 使用 uv（推荐）

```bash
# 安装 uv
pip install uv

# 创建虚拟环境
uv venv

# 安装包
uv pip install requests

# 从 requirements.txt 安装
uv pip install -r requirements.txt

# 同步依赖
uv pip sync requirements.txt
```

---

## 配置 pip

### 配置文件

```bash
# 查看 pip 配置
pip config list

# 设置配置
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 配置文件位置
# Unix: ~/.config/pip/pip.conf
# Windows: %APPDATA%\pip\pip.ini
```

### pip.conf 示例

```ini
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
trusted-host = pypi.tuna.tsinghua.edu.cn
timeout = 60

[install]
no-cache-dir = true
```

### 使用国内镜像

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