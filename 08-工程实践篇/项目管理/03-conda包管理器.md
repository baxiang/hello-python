# conda 包管理器

conda 是跨平台、语言无关的二进制包和环境管理器。它不仅能管理 Python 包，还能管理 C/C++、R、Ruby 等任意语言的二进制依赖。

在 conda 中，**环境是一等公民**。它使用硬链接技术，环境创建只需几秒且极其节省磁盘空间。

---

## 安装发行版

| 发行版 | 维护者 | 默认频道 | 特点 |
|--------|--------|----------|------|
| **Miniforge** | conda-forge 社区 | conda-forge | 社区驱动，完全免费，推荐首选 |
| **Miniconda** | Anaconda | defaults (Anaconda Repo) | 最小安装，企业使用可能受许可限制 |
| **Anaconda** | Anaconda | defaults | 预装数百个包，体积较大，适合新手 |

> **推荐**：使用 Miniforge，默认配置 conda-forge 频道，避免商业许可问题。

---

## 基本使用

```bash
# 创建环境（指定 Python 版本）
conda create -n myenv python=3.11

# 创建环境并安装包
conda create -n myenv python=3.11 numpy pandas scipy

# 激活/退出环境
conda activate myenv
conda deactivate

# 安装包
conda install matplotlib
conda install -n myenv scikit-learn

# 更新包
conda update numpy
conda update --all

# 卸载包
conda remove numpy

# 搜索包
conda search tensorflow
```

---

## 环境管理进阶

### 指定路径创建

使用 `--prefix` 可以将环境创建在项目目录下，便于管理和版本控制（忽略 .gitignore 后）。

```bash
# 在当前目录下创建 envs 环境
conda create --prefix ./envs python=3.11

# 激活路径环境
conda activate ./envs
```

### 克隆与回滚

```bash
# 克隆环境（完整复制）
conda create -n myclone --clone myenv

# 查看环境修改历史
conda list --revisions

# 回滚到指定版本
conda install --rev 2
```

### 嵌套激活

保留当前环境 PATH 的同时激活新环境（常用于 root 环境有工具链的情况）：

```bash
conda activate --stack myenv
```

---

## 环境导出与复现

### 导出格式

| 格式 | 命令 | 说明 |
|------|------|------|
| **YAML** | `conda export > env.yaml` | 推荐，跨平台，包含依赖树 |
| **History** | `conda export --from-history > env.yaml` | 仅导出显式安装的包，最通用 |
| **Explicit** | `conda list --explicit > spec.txt` | 包含完整 URL，精确复现但仅限同平台 |
| **Requirements** | `conda export --format=requirements > req.txt` | 类似 pip 的 requirements 格式 |

### 导入环境

```bash
# 从 YAML 创建
conda create --file environment.yml

# 从 Explicit 文件创建/安装
conda create -n myenv --file spec.txt
```

### 环境 YAML 示例

```yaml
name: myenv
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.11
  - numpy=1.24
  - pip:
    - some-pip-only-package
variables:
  MY_VAR: value
```

---

## 频道 (Channels) 管理

频道是包的存储仓库。conda 默认搜索 `defaults` 频道。

```bash
# 添加频道（优先级递增，最后添加的最高）
conda config --add channels conda-forge

# 设置频道优先级策略
conda config --set channel_priority strict

# 查看频道配置
conda config --show channels

# 临时从指定频道安装
conda install -c bioconda samtools
```

> **strict 策略**：确保同一包的所有依赖都来自同一频道，避免混用导致冲突。

---

## 配置文件 (.condarc)

`.condarc` 是 conda 的运行时配置文件，支持 YAML 语法。

### 文件位置与优先级

优先级从低到高：
1. 系统级：`/etc/conda/.condarc`
2. 用户级：`~/.condarc` 或 `~/.config/conda/.condarc`
3. 环境级：`$CONDA_PREFIX/.condarc`
4. 环境变量：`CONDA_*`
5. 命令行参数

### 常用配置示例

```yaml
# ~/.condarc
channels:
  - conda-forge
  - defaults

channel_priority: strict
show_channel_urls: true

# 自定义环境提示符
env_prompt: '({name})'

# 自动堆叠激活
auto_stack: 1

# 包缓存目录
pkgs_dirs:
  - ~/.conda/pkgs

# 环境存储目录
envs_dirs:
  - ~/.conda/envs
```

### 国内镜像配置

```bash
# 添加清华镜像源
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --set show_channel_urls yes
```

---

## 高级功能

### 跨平台支持

```bash
# 创建其他平台的环境（推荐先 dry-run）
conda create --platform linux-64 --name linux-env python --dry-run
```

### 环境变量管理

```bash
# 设置环境变量（持久化到环境）
conda env config vars set MY_KEY=secret -n myenv

# 查看环境变量
conda env config vars list -n myenv

# 删除环境变量
conda env config vars unset MY_KEY -n myenv
```

> 设置后需重新激活环境生效。

### 清理缓存

```bash
# 清理未使用的包和缓存
conda clean --all

# 仅清理 tarballs
conda clean --tarballs
```

---

## 与 pip 配合

conda 环境中可以使用 pip，但需注意隔离性。

**最佳实践：**

1. **先 conda 后 pip**：尽可能用 conda 安装所有依赖。
2. **避免混用**：在同一个环境中，不要先用 pip 安装再用 conda 安装同一个包。
3. **使用 --user 警告**：不要在 conda 环境中使用 `pip install --user`。

```bash
# 1. 创建环境
conda create -n myenv python=3.11 numpy

# 2. 激活
conda activate myenv

# 3. 用 pip 安装 conda 没有的包
pip install some-package --upgrade-strategy only-if-needed
```

> 如果环境已经用 pip 安装过包，后续需要添加 conda 包时，建议**重建环境**以避免依赖冲突。

---

## 本章小结

```
┌─────────────────────────────────────────────────────────────┐
│                   conda 包管理器 知识要点                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   核心特性：                                                 │
│   ✓ 跨平台、语言无关的二进制包管理                           │
│   ✓ 环境是一等公民，硬链接节省空间                           │
│   ✓ 预编译二进制，无需系统编译依赖                           │
│                                                             │
│   环境管理：                                                 │
│   ✓ 创建/克隆/删除/回滚                                     │
│   ✓ --prefix 项目级环境                                     │
│   ✓ 多格式导出：YAML、Explicit、Requirements                 │
│                                                             │
│   频道与配置：                                               │
│   ✓ conda-forge 社区频道推荐                                 │
│   ✓ strict 优先级策略                                       │
│   ✓ .condarc 多层级配置                                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```
