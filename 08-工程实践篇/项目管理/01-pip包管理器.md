# pip 包管理器

pip 是 Python 官方推荐的包管理工具。

---

## 基本命令

```bash
# 安装包
pip install package_name

# 安装指定版本
pip install package_name==1.0.0

# 升级包
pip install --upgrade package_name

# 卸载包
pip uninstall package_name

# 列出已安装的包
pip list

# 导出依赖
pip freeze > requirements.txt

# 从文件安装依赖
pip install -r requirements.txt
```

---

## 虚拟环境

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境 (macOS/Linux)
source venv/bin/activate

# 激活虚拟环境 (Windows)
venv\Scripts\activate

# 退出虚拟环境
deactivate
```

---

## 常见用法

### 指定源安装

```bash
# 使用国内镜像源
pip install package_name -i https://pypi.tuna.tsinghua.edu.cn/simple

# 设置默认源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### 依赖版本约束

```bash
# 兼容版本安装
pip install "package_name>=1.0,<2.0"

# 安装最新版本
pip install "package_name>=1.0"
```

---

## 本章小结

```
┌─────────────────────────────────────────────────────────────┐
│                    pip 包管理器 知识要点                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   pip：                                                      │
│   ✓ Python 官方包管理器                                     │
│   ✓ 配合 venv 使用虚拟环境                                  │
│   ✓ 通过 requirements.txt 管理依赖                          │
│   ✓ 支持国内镜像源加速                                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```
