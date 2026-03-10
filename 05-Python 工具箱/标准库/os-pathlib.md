# os 与 pathlib 模块 - 文件系统操作

> 学习目标：掌握 Python 中操作文件系统的两种核心方式，理解 os 模块的传统用法和 pathlib 的现代风格，能够独立完成文件和目录的增删改查操作。

---

## 第一部分：os 模块

### 1.1 什么是 os 模块

#### 概念说明

`os` 模块是 Python 的标准库，提供了与操作系统交互的接口。可以把它理解成一位"系统管理员"——你告诉它要做什么，它负责和操作系统沟通，帮你完成文件夹创建、文件移动、目录扫描等工作。

无论你在 Windows、macOS 还是 Linux 上运行 Python，`os` 模块都会自动处理底层差异，让同一段代码在不同系统上都能正常工作。

```
os 模块的定位
┌─────────────────────────────────────────────────────┐
│                   你的 Python 程序                   │
├─────────────────────────────────────────────────────┤
│                    os 模块（翻译层）                  │
├──────────────┬──────────────────┬───────────────────┤
│   Windows    │      macOS       │      Linux        │
│   文件系统   │     文件系统     │     文件系统      │
└──────────────┴──────────────────┴───────────────────┘
```

同一段 Python 代码，`os` 模块在不同系统上会调用对应的底层命令，你不需要关心这些差异。

#### 示例代码

```python
import os

# 查看当前操作系统类型
print(os.name)        # 'nt' 表示 Windows，'posix' 表示 macOS/Linux

# 查看路径分隔符（Windows 是 \，macOS/Linux 是 /）
print(os.sep)         # macOS/Linux: /   Windows: \

# 查看行尾符
print(repr(os.linesep))  # Linux: '\n'   Windows: '\r\n'
```

---

### 1.2 目录操作

#### 概念说明

目录操作是文件系统管理的基础。下面是常用的目录操作函数：

```
常用目录操作函数速览
┌─────────────────────┬───────────────────────────────────┐
│       函数          │             说明                  │
├─────────────────────┼───────────────────────────────────┤
│ os.getcwd()         │ 获取当前工作目录                   │
│ os.chdir(path)      │ 切换当前工作目录                   │
│ os.mkdir(path)      │ 创建单个目录                       │
│ os.makedirs(path)   │ 递归创建多级目录                   │
│ os.rmdir(path)      │ 删除空目录                         │
│ os.removedirs(path) │ 递归删除空目录                     │
└─────────────────────┴───────────────────────────────────┘
```

`mkdir` 和 `makedirs` 的区别：

```
mkdir 只能创建一层目录：
  os.mkdir("a/b/c")  -> 报错（如果 a/b 不存在）

makedirs 可以创建多层目录：
  os.makedirs("a/b/c")  -> 自动创建 a、a/b、a/b/c
```

#### 示例代码

```python
import os

# 1. 获取当前工作目录
current = os.getcwd()
print(f"当前目录：{current}")

# 2. 切换工作目录
os.chdir("/tmp")
print(f"切换后：{os.getcwd()}")

# 3. 创建单个目录
os.mkdir("my_folder")
# 注意：如果 my_folder 已经存在，会抛出 FileExistsError

# 安全创建（先检查是否存在）
if not os.path.exists("my_folder"):
    os.mkdir("my_folder")

# 4. 递归创建多级目录
os.makedirs("project/src/utils", exist_ok=True)
# exist_ok=True 表示目录已存在时不报错（推荐加上这个参数）

# 5. 删除空目录
os.rmdir("my_folder")
# 注意：目录不为空时会报错 OSError

# 6. 递归删除多级空目录
os.removedirs("project/src/utils")
# 从最深层开始删除，遇到非空目录就停止
```

---

### 1.3 文件操作

#### 概念说明

`os` 模块提供了重命名、删除文件以及列出目录内容的功能。

```
常用文件操作函数速览
┌─────────────────────────────┬──────────────────────────────────┐
│            函数             │              说明                │
├─────────────────────────────┼──────────────────────────────────┤
│ os.rename(src, dst)         │ 重命名文件或目录                  │
│ os.replace(src, dst)        │ 重命名（目标存在时自动覆盖）      │
│ os.remove(path)             │ 删除文件（不能删除目录）          │
│ os.listdir(path)            │ 列出目录下所有文件和子目录名称    │
│ os.stat(path)               │ 获取文件详细信息（大小、时间等）  │
└─────────────────────────────┴──────────────────────────────────┘
```

#### 示例代码

```python
import os

# 1. 重命名文件
os.rename("old_name.txt", "new_name.txt")
# 如果 new_name.txt 已存在，在 Windows 上会报错

# 更安全的替代方案（目标存在时覆盖）
os.replace("old_name.txt", "new_name.txt")

# 2. 删除文件
os.remove("unwanted_file.txt")
# 注意：文件不存在时会抛出 FileNotFoundError

# 安全删除
if os.path.exists("unwanted_file.txt"):
    os.remove("unwanted_file.txt")

# 3. 列出目录内容
items = os.listdir(".")          # 列出当前目录
items = os.listdir("/tmp")       # 列出指定目录
print(items)
# 输出示例：['file1.txt', 'file2.py', 'subfolder']
# 注意：返回的只是名称，不包含完整路径

# 4. 获取文件信息
info = os.stat("example.txt")
print(f"文件大小：{info.st_size} 字节")
print(f"最后修改时间：{info.st_mtime}")  # 时间戳格式

import time
mtime = time.ctime(info.st_mtime)
print(f"可读的修改时间：{mtime}")

# 5. 只列出文件（过滤掉目录）
all_items = os.listdir(".")
files_only = [f for f in all_items if os.path.isfile(f)]
dirs_only  = [d for d in all_items if os.path.isdir(d)]

print("文件：", files_only)
print("目录：", dirs_only)
```

---

### 1.4 路径操作：os.path

#### 概念说明

`os.path` 是 `os` 模块的子模块，专门用于处理路径字符串。路径操作是文件系统编程中最常见的工作之一。

```
路径的组成结构（以 /home/user/project/main.py 为例）
┌────────────────────────────────────────────────────┐
│            /home/user/project/main.py              │
├────────────────────┬──────────────────────┬────────┤
│   dirname          │      basename         │        │
│  /home/user/project│      main.py          │        │
│                    ├──────────────┬────────┤        │
│                    │  stem        │ suffix │        │
│                    │  main        │ .py    │        │
└────────────────────┴──────────────┴────────┘
```

常用函数速览：

```
┌─────────────────────────────┬──────────────────────────────────────────────┐
│            函数             │         说明                                 │
├─────────────────────────────┼──────────────────────────────────────────────┤
│ os.path.join(a, b, ...)     │ 拼接路径（推荐用这个，不要手动拼字符串）    │
│ os.path.basename(path)      │ 返回路径最后一部分（文件名）                │
│ os.path.dirname(path)       │ 返回目录部分                                │
│ os.path.split(path)         │ 分割为 (目录, 文件名) 元组                  │
│ os.path.splitext(path)      │ 分割为 (路径去后缀, 后缀) 元组              │
│ os.path.abspath(path)       │ 转为绝对路径                                │
│ os.path.exists(path)        │ 路径是否存在                                │
│ os.path.isfile(path)        │ 是否是文件                                  │
│ os.path.isdir(path)         │ 是否是目录                                  │
│ os.path.getsize(path)       │ 获取文件大小（字节）                        │
└─────────────────────────────┴──────────────────────────────────────────────┘
```

#### 示例代码

```python
import os

path = "/home/user/project/main.py"

# 1. 路径拼接（强烈推荐用 join，不要手动写 "/" 拼接）
# 错误方式：base + "/" + filename  -> 不同系统分隔符不同
# 正确方式：
new_path = os.path.join("/home/user", "project", "main.py")
print(new_path)   # /home/user/project/main.py

# 2. 获取文件名
print(os.path.basename(path))    # main.py

# 3. 获取目录名
print(os.path.dirname(path))     # /home/user/project

# 4. 同时获取目录和文件名
directory, filename = os.path.split(path)
print(directory)   # /home/user/project
print(filename)    # main.py

# 5. 分离文件名和后缀
name, ext = os.path.splitext("main.py")
print(name)   # main
print(ext)    # .py

name, ext = os.path.splitext("archive.tar.gz")
print(name)   # archive.tar
print(ext)    # .gz   （只分离最后一个后缀）

# 6. 转为绝对路径
rel_path = "scripts/run.sh"
abs_path = os.path.abspath(rel_path)
print(abs_path)   # 例：/Users/baxiang/scripts/run.sh

# 7. 判断路径状态
print(os.path.exists("/tmp"))       # True（存在）
print(os.path.isfile("/tmp"))       # False（/tmp 是目录，不是文件）
print(os.path.isdir("/tmp"))        # True

# 8. 获取文件大小
size = os.path.getsize("example.txt")
print(f"文件大小：{size} 字节")

# 实用技巧：构建相对于脚本所在目录的路径
# __file__ 是当前脚本的路径
script_dir = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join(script_dir, "data", "input.csv")
print(f"数据文件路径：{data_file}")
```

---

### 1.5 遍历目录：os.walk()

#### 概念说明

`os.walk()` 是一个强大的函数，可以递归遍历整个目录树，每次迭代返回三个值：当前目录路径、当前目录下的子目录列表、当前目录下的文件列表。

类比理解：想象你在整理一个多层书柜，`os.walk()` 就像一个助手，自动帮你逐层打开每个格子，告诉你"这个格子在哪里、里面有哪些小格子、里面有哪些书"。

```
目录树结构示例
project/
├── README.md
├── src/
│   ├── main.py
│   ├── utils.py
│   └── models/
│       ├── user.py
│       └── post.py
└── tests/
    ├── test_main.py
    └── test_utils.py

os.walk("project") 的遍历顺序：
┌─────────────────┬──────────────────┬─────────────────────────────────┐
│  当前路径        │   子目录列表      │          文件列表               │
├─────────────────┼──────────────────┼─────────────────────────────────┤
│ project         │ ['src', 'tests'] │ ['README.md']                   │
│ project/src     │ ['models']       │ ['main.py', 'utils.py']         │
│ project/src/... │ []               │ ['user.py', 'post.py']          │
│ project/tests   │ []               │ ['test_main.py','test_utils.py']│
└─────────────────┴──────────────────┴─────────────────────────────────┘
```

#### 示例代码

```python
import os

# 1. 基本用法：遍历所有文件
for dirpath, dirnames, filenames in os.walk("project"):
    print(f"当前目录：{dirpath}")
    print(f"  子目录：{dirnames}")
    print(f"  文件：{filenames}")
    print()

# 2. 列出所有文件的完整路径
for dirpath, dirnames, filenames in os.walk("project"):
    for filename in filenames:
        full_path = os.path.join(dirpath, filename)
        print(full_path)

# 3. 只列出特定类型的文件（例如所有 .py 文件）
py_files = []
for dirpath, dirnames, filenames in os.walk("."):
    for filename in filenames:
        if filename.endswith(".py"):
            py_files.append(os.path.join(dirpath, filename))

print("所有 Python 文件：")
for f in py_files:
    print(f"  {f}")

# 4. 控制遍历深度（通过修改 dirnames 来跳过某些目录）
for dirpath, dirnames, filenames in os.walk("project"):
    # 跳过隐藏目录（以 . 开头的目录，如 .git）
    dirnames[:] = [d for d in dirnames if not d.startswith(".")]
    # 跳过 __pycache__ 目录
    dirnames[:] = [d for d in dirnames if d != "__pycache__"]
    
    for filename in filenames:
        print(os.path.join(dirpath, filename))

# 5. 统计目录下的文件总数和总大小
total_files = 0
total_size = 0

for dirpath, dirnames, filenames in os.walk("."):
    for filename in filenames:
        total_files += 1
        full_path = os.path.join(dirpath, filename)
        total_size += os.path.getsize(full_path)

print(f"文件总数：{total_files}")
print(f"总大小：{total_size / 1024 / 1024:.2f} MB")
```

---

### 1.6 环境变量：os.environ

#### 概念说明

环境变量是操作系统维护的一组键值对，程序可以读取它们来获取配置信息。常见用途包括：读取 `PATH`（命令搜索路径）、`HOME`（用户主目录）、`API_KEY`（密钥配置）等。

类比理解：环境变量就像一张便利贴，贴在操作系统上，任何程序都可以读取。开发中常用它来存放不想写死在代码里的配置（比如数据库密码）。

#### 示例代码

```python
import os

# 1. 读取所有环境变量（返回类字典对象）
all_env = os.environ
print(type(all_env))   # <class 'os._Environ'>

# 2. 读取特定环境变量
home_dir = os.environ["HOME"]         # 不存在时抛出 KeyError
home_dir = os.environ.get("HOME")     # 不存在时返回 None（推荐）
home_dir = os.environ.get("HOME", "/tmp")  # 不存在时返回默认值

print(f"用户主目录：{home_dir}")
print(f"PATH：{os.environ.get('PATH')}")

# 3. 设置环境变量（只影响当前进程和子进程）
os.environ["MY_API_KEY"] = "secret_key_123"
print(os.environ.get("MY_API_KEY"))   # secret_key_123

# 4. 删除环境变量
del os.environ["MY_API_KEY"]

# 5. 实际应用：从环境变量读取配置
def get_database_url():
    db_host = os.environ.get("DB_HOST", "localhost")
    db_port = os.environ.get("DB_PORT", "5432")
    db_name = os.environ.get("DB_NAME", "myapp")
    return f"postgresql://{db_host}:{db_port}/{db_name}"

print(get_database_url())
# 没有设置时输出：postgresql://localhost:5432/myapp

# 6. 常用环境变量
print(os.environ.get("HOME"))      # 用户主目录（macOS/Linux）
print(os.environ.get("USER"))      # 当前用户名
print(os.environ.get("TMPDIR"))    # 临时文件目录（macOS）
print(os.environ.get("TEMP"))      # 临时文件目录（Windows）
```

---

## 第二部分：pathlib 模块

### 2.1 为什么推荐用 pathlib

#### 概念说明

Python 3.4 引入了 `pathlib` 模块，提供了面向对象的路径操作方式。相比 `os.path`，`pathlib` 的代码更简洁、更易读，是现代 Python 项目的推荐做法。

**两种风格的对比：**

```
os.path 风格（过程式）：
  用一堆独立函数处理字符串，路径只是普通字符串
  
pathlib 风格（面向对象）：
  路径是一个对象，对象自带方法，可以像操作变量一样操作路径
```

具体对比：

```
┌─────────────────────────────────────┬────────────────────────────────────┐
│            os.path 写法             │           pathlib 写法             │
├─────────────────────────────────────┼────────────────────────────────────┤
│ os.path.join(a, b, "c.txt")        │ Path(a) / b / "c.txt"              │
│ os.path.basename(path)             │ path.name                          │
│ os.path.dirname(path)              │ path.parent                        │
│ os.path.splitext(path)[1]          │ path.suffix                        │
│ os.path.exists(path)               │ path.exists()                      │
│ os.path.isfile(path)               │ path.is_file()                     │
│ os.makedirs(path, exist_ok=True)   │ path.mkdir(parents=True, ...)      │
└─────────────────────────────────────┴────────────────────────────────────┘
```

`pathlib` 的 `/` 运算符是最直观的改进——用 `/` 拼接路径，就像在操作系统里写路径一样自然。

#### 示例代码

```python
# os.path 风格（旧式）
import os
config_path = os.path.join(os.path.dirname(__file__), "config", "settings.json")

# pathlib 风格（现代）
from pathlib import Path
config_path = Path(__file__).parent / "config" / "settings.json"

# 明显更简洁、更易读
```

---

### 2.2 Path 对象的创建和路径拼接

#### 概念说明

`Path` 是 `pathlib` 的核心类。创建 `Path` 对象后，就可以通过 `/` 运算符来拼接路径，通过属性和方法来操作路径。

```
Path 对象的创建方式
┌──────────────────────────────────────────────────────────┐
│  Path(".")              当前目录                         │
│  Path("/tmp")           绝对路径                         │
│  Path.home()            用户主目录（如 /home/user）      │
│  Path.cwd()             当前工作目录                     │
│  Path(__file__)         当前脚本所在路径                  │
└──────────────────────────────────────────────────────────┘
```

#### 示例代码

```python
from pathlib import Path

# 1. 创建 Path 对象
p1 = Path(".")              # 当前目录
p2 = Path("/tmp")           # 绝对路径
p3 = Path.home()            # 用户主目录
p4 = Path.cwd()             # 当前工作目录

print(p3)   # 例：/Users/baxiang

# 2. 路径拼接：使用 / 运算符（pathlib 的精华）
base = Path("/home/user")
project = base / "projects" / "my_app"
config = project / "config" / "settings.json"

print(config)
# 输出：/home/user/projects/my_app/config/settings.json

# 3. 和字符串混用也没问题
base = Path("/home/user")
subdir = "documents"
filename = "report.pdf"

full_path = base / subdir / filename
print(full_path)   # /home/user/documents/report.pdf

# 4. 转为字符串（需要字符串时使用）
path_str = str(full_path)
# 或者
path_str = full_path.as_posix()   # 强制使用正斜杠（跨平台时有用）

# 5. 从字符串转为 Path
path_from_str = Path("/some/existing/path")

# 6. 拼接多个部分
parts = ["a", "b", "c", "file.txt"]
p = Path(*parts)
# 等价于 Path("a") / "b" / "c" / "file.txt"
print(p)   # a/b/c/file.txt
```

---

### 2.3 路径属性

#### 概念说明

`Path` 对象提供了一系列属性，可以直接获取路径的各个组成部分，不需要调用函数。

```
路径属性速览（以 /home/user/project/main.py 为例）
┌───────────────────────────────────────────────────────────────┐
│                /home/user/project/main.py                     │
├──────────────────────────┬────────────────────────────────────┤
│  .parent                 │  /home/user/project                │
│  .name                   │  main.py                           │
│  .stem                   │  main                              │
│  .suffix                 │  .py                               │
│  .suffixes               │  ['.py']                           │
│  .parts                  │  ('/', 'home', 'user',             │
│                          │   'project', 'main.py')            │
│  .root                   │  /                                 │
│  .anchor                 │  /                                 │
└──────────────────────────┴────────────────────────────────────┘
```

#### 示例代码

```python
from pathlib import Path

p = Path("/home/user/project/main.py")

# 1. 获取文件名（含后缀）
print(p.name)        # main.py

# 2. 获取文件名（不含后缀）
print(p.stem)        # main

# 3. 获取后缀
print(p.suffix)      # .py

# 4. 获取多个后缀（例如 .tar.gz）
p2 = Path("archive.tar.gz")
print(p2.suffixes)   # ['.tar', '.gz']
print(p2.suffix)     # .gz（只返回最后一个）

# 5. 获取父目录
print(p.parent)      # /home/user/project

# 6. 逐级向上获取父目录
print(p.parent)         # /home/user/project
print(p.parent.parent)  # /home/user
print(p.parents[0])     # /home/user/project  （等同于 p.parent）
print(p.parents[1])     # /home/user
print(p.parents[2])     # /home
print(list(p.parents))  # 所有上级目录列表

# 7. 获取路径各部分（元组形式）
print(p.parts)
# ('/', 'home', 'user', 'project', 'main.py')

# 8. 获取根目录
print(p.root)     # /  (Windows 可能是 C:\)
print(p.anchor)   # /  (包含驱动器名，如 Windows 的 C:\)

# 9. 实用技巧：获取脚本所在目录
script_dir = Path(__file__).parent
data_dir = script_dir / "data"
output_dir = script_dir / "output"
```

---

### 2.4 路径判断

#### 概念说明

`Path` 对象提供了一系列 `is_*()` 和 `exists()` 方法，用于判断路径的状态。这些方法都会实际访问文件系统，所以路径必须存在才能得到有意义的结果（`exists()` 除外——它专门用来判断是否存在）。

#### 示例代码

```python
from pathlib import Path

p = Path("/tmp")

# 1. 判断路径是否存在
print(p.exists())       # True

# 2. 判断是否是文件
print(p.is_file())      # False（/tmp 是目录）

# 3. 判断是否是目录
print(p.is_dir())       # True

# 4. 判断是否是绝对路径（不访问文件系统，纯字符串判断）
print(p.is_absolute())  # True

p_rel = Path("relative/path")
print(p_rel.is_absolute())  # False

# 5. 判断是否是符号链接
print(p.is_symlink())   # False

# 6. 实际应用：安全创建目录
def ensure_dir(path: Path) -> None:
    if not path.exists():
        path.mkdir(parents=True)
        print(f"已创建目录：{path}")
    elif not path.is_dir():
        raise ValueError(f"{path} 存在但不是目录")
    else:
        print(f"目录已存在：{path}")

ensure_dir(Path("output/reports"))

# 7. 安全读取文件
def read_file_safe(path: Path) -> str | None:
    if not path.exists():
        print(f"文件不存在：{path}")
        return None
    if not path.is_file():
        print(f"不是文件：{path}")
        return None
    return path.read_text(encoding="utf-8")
```

---

### 2.5 路径修改：with_suffix 和 with_name

#### 概念说明

`pathlib` 提供了便捷方法，可以在不修改原路径对象的情况下，生成一个修改了某部分的新路径对象。这种设计叫做"不可变对象风格"，原来的路径对象不会被改变。

#### 示例代码

```python
from pathlib import Path

p = Path("/home/user/document.txt")

# 1. 修改文件后缀
new_p = p.with_suffix(".pdf")
print(new_p)   # /home/user/document.pdf
print(p)       # /home/user/document.txt  (原路径不变)

# 2. 去掉后缀
no_ext = p.with_suffix("")
print(no_ext)  # /home/user/document

# 3. 修改文件名（含后缀）
renamed = p.with_name("report.md")
print(renamed)  # /home/user/report.md

# 4. 修改文件名（不含后缀），需要组合使用
new_stem = p.with_stem("final_report")  # Python 3.9+
print(new_stem)  # /home/user/final_report.txt

# 3.9 之前的写法：
new_stem = p.with_name("final_report" + p.suffix)
print(new_stem)  # /home/user/final_report.txt

# 5. 修改父目录
new_parent = p.with_name(p.name)  # 保留文件名
in_new_dir = Path("/backup") / p.name
print(in_new_dir)   # /backup/document.txt

# 6. 实用场景：批量处理文件名
# 将所有 .txt 文件路径转为 .md 文件路径
txt_paths = [
    Path("docs/intro.txt"),
    Path("docs/guide.txt"),
    Path("docs/reference.txt"),
]

md_paths = [p.with_suffix(".md") for p in txt_paths]
for txt, md in zip(txt_paths, md_paths):
    print(f"{txt} -> {md}")
```

---

### 2.6 目录操作

#### 概念说明

`Path` 对象提供了创建目录、删除目录和列出目录内容的方法，用法比 `os` 模块更直观。

```
pathlib 目录操作方法速览
┌──────────────────────────────────────┬──────────────────────────────────────┐
│               方法                   │               说明                   │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ path.mkdir(parents, exist_ok)        │ 创建目录                             │
│ path.rmdir()                         │ 删除空目录                           │
│ path.iterdir()                       │ 列出目录内容（返回迭代器）            │
│ path.read_text(encoding)             │ 读取文件内容（字符串）               │
│ path.write_text(data, encoding)      │ 写入文件内容                         │
│ path.read_bytes()                    │ 读取文件内容（字节）                 │
│ path.write_bytes(data)               │ 写入字节内容                         │
│ path.unlink(missing_ok)              │ 删除文件                             │
│ path.rename(target)                  │ 重命名/移动                          │
│ path.replace(target)                 │ 重命名（覆盖已有文件）               │
│ path.stat()                          │ 获取文件信息                         │
└──────────────────────────────────────┴──────────────────────────────────────┘
```

#### 示例代码

```python
from pathlib import Path

# 1. 创建目录
p = Path("output/reports/2024")

# 普通创建（父目录不存在会报错）
# p.mkdir()

# 递归创建（推荐）
p.mkdir(parents=True, exist_ok=True)
# parents=True  : 自动创建所有中间目录
# exist_ok=True : 已存在时不报错

# 2. 删除空目录
empty_dir = Path("temp_dir")
empty_dir.mkdir(exist_ok=True)
empty_dir.rmdir()   # 目录不为空时抛出 OSError

# 3. 列出目录内容
current = Path(".")
for item in current.iterdir():
    if item.is_file():
        print(f"文件: {item.name}")
    elif item.is_dir():
        print(f"目录: {item.name}/")

# 4. 读写文件（pathlib 自带文件读写，非常方便）
# 写入文件
output = Path("hello.txt")
output.write_text("你好，pathlib！\n", encoding="utf-8")

# 读取文件
content = output.read_text(encoding="utf-8")
print(content)

# 读写字节
binary_file = Path("data.bin")
binary_file.write_bytes(b"\x00\x01\x02\x03")
data = binary_file.read_bytes()

# 5. 删除文件
output.unlink()               # 文件不存在时报错
output.unlink(missing_ok=True)  # Python 3.8+，不存在时不报错

# 6. 获取文件信息
p = Path("example.txt")
p.write_text("test", encoding="utf-8")
stat = p.stat()
print(f"大小：{stat.st_size} 字节")
print(f"修改时间：{stat.st_mtime}")
```

---

### 2.7 glob 模式：glob 和 rglob

#### 概念说明

`glob` 是一种用通配符匹配文件路径的方式，`Path` 对象提供了 `glob()` 和 `rglob()` 两个方法。

- `glob(pattern)` ：在当前目录下按模式匹配
- `rglob(pattern)` ：在当前目录及所有子目录下递归匹配（r 代表 recursive）

**glob 模式语法速查表：**

```
┌────────────┬──────────────────────────────────────────────────┐
│  通配符    │                      含义                        │
├────────────┼──────────────────────────────────────────────────┤
│     *      │ 匹配任意数量的字符（不含路径分隔符）             │
│     ?      │ 匹配单个字符                                     │
│    **      │ 匹配任意数量的目录层级（只能用于 rglob 或 **/） │
│  [abc]     │ 匹配括号内的任意一个字符                         │
│  [a-z]     │ 匹配范围内的任意字符                             │
│  [!abc]    │ 匹配括号内字符以外的字符                         │
├────────────┼──────────────────────────────────────────────────┤
│ 示例       │                                                  │
├────────────┼──────────────────────────────────────────────────┤
│ *.py       │ 所有 .py 文件                                    │
│ test_*.py  │ test_ 开头的 .py 文件                           │
│ *.py  ??   │ 文件名有两个字符的 .py 文件（如 ab.py）         │
│ **/*.py    │ 所有子目录下的 .py 文件（等同于 rglob("*.py")） │
│ data[0-9]  │ data0 到 data9                                   │
└────────────┴──────────────────────────────────────────────────┘
```

#### 示例代码

```python
from pathlib import Path

base = Path(".")

# 1. glob：在当前目录下匹配（不进入子目录）
py_files = list(base.glob("*.py"))
print("当前目录的 .py 文件：")
for f in py_files:
    print(f"  {f}")

# 2. rglob：递归匹配所有子目录
all_py = list(base.rglob("*.py"))
print("所有 .py 文件（含子目录）：")
for f in all_py:
    print(f"  {f}")

# 3. 匹配特定前缀的文件
test_files = list(base.rglob("test_*.py"))

# 4. 匹配所有 .txt 和 .md 文件（需要分两次 glob）
docs = list(base.rglob("*.txt")) + list(base.rglob("*.md"))

# 5. 匹配目录（以 / 结尾）
# pathlib 里直接过滤 is_dir()
subdirs = [p for p in base.iterdir() if p.is_dir()]

# 6. 使用 ** 的 glob（等效于 rglob）
# base.glob("**/*.py") 等同于 base.rglob("*.py")
all_py_v2 = list(base.glob("**/*.py"))

# 7. 实用示例：找出所有 Python 文件并按大小排序
py_files_sorted = sorted(
    base.rglob("*.py"),
    key=lambda p: p.stat().st_size,
    reverse=True   # 从大到小
)

print("Python 文件（按大小排序）：")
for f in py_files_sorted[:5]:   # 只显示前5个
    size_kb = f.stat().st_size / 1024
    print(f"  {f.name:<30} {size_kb:>8.1f} KB")

# 8. 生成器用法（节省内存，适合文件很多的情况）
# glob/rglob 返回的是生成器，list() 会全部加载到内存
# 如果只是遍历，直接用 for 循环更高效
for py_file in base.rglob("*.py"):
    # 逐个处理，不会一次性加载所有文件到内存
    print(py_file.name)
```

---

## 第三部分：综合实例

### 3.1 批量重命名文件：os 版 vs pathlib 版对比

#### 概念说明

批量重命名是文件操作的经典需求。通过对比两种实现方式，可以直观感受 pathlib 的简洁之处。

任务：将目录下所有 `.txt` 文件重命名，在文件名前加上 `backup_` 前缀。

```
重命名前：           重命名后：
report.txt    ->    backup_report.txt
notes.txt     ->    backup_notes.txt
data.txt      ->    backup_data.txt
```

#### 示例代码

```python
import os
from pathlib import Path

# ============================================================
# os 版本（传统写法）
# ============================================================
def batch_rename_os(directory: str, prefix: str) -> None:
    items = os.listdir(directory)
    renamed_count = 0
    
    for item in items:
        if item.endswith(".txt"):
            old_path = os.path.join(directory, item)
            new_name = prefix + item
            new_path = os.path.join(directory, new_name)
            os.rename(old_path, new_path)
            print(f"重命名：{item} -> {new_name}")
            renamed_count += 1
    
    print(f"共重命名 {renamed_count} 个文件")

# 调用
batch_rename_os("/tmp/test_files", "backup_")


# ============================================================
# pathlib 版本（现代写法）
# ============================================================
def batch_rename_pathlib(directory: str, prefix: str) -> None:
    base = Path(directory)
    renamed_count = 0
    
    for txt_file in base.glob("*.txt"):
        new_name = prefix + txt_file.name
        txt_file.rename(txt_file.parent / new_name)
        print(f"重命名：{txt_file.name} -> {new_name}")
        renamed_count += 1
    
    print(f"共重命名 {renamed_count} 个文件")

# 调用
batch_rename_pathlib("/tmp/test_files", "backup_")


# ============================================================
# 进阶版：支持预览（dry run）、撤销
# ============================================================
def batch_rename_advanced(
    directory: str,
    old_ext: str,
    new_ext: str,
    dry_run: bool = True
) -> list[tuple[Path, Path]]:
    """
    将目录下所有 old_ext 后缀的文件改为 new_ext 后缀
    dry_run=True 时只打印计划，不实际执行
    """
    base = Path(directory)
    
    if not old_ext.startswith("."):
        old_ext = "." + old_ext
    if not new_ext.startswith("."):
        new_ext = "." + new_ext
    
    plan = []  # 记录 (旧路径, 新路径) 对
    
    for old_path in base.glob(f"*{old_ext}"):
        new_path = old_path.with_suffix(new_ext)
        plan.append((old_path, new_path))
    
    if dry_run:
        print("[预览模式] 以下操作将被执行：")
        for old, new in plan:
            print(f"  {old.name} -> {new.name}")
        print(f"\n共 {len(plan)} 个文件，使用 dry_run=False 执行")
    else:
        for old, new in plan:
            old.rename(new)
            print(f"已重命名：{old.name} -> {new.name}")
        print(f"\n共重命名 {len(plan)} 个文件")
    
    return plan

# 先预览
batch_rename_advanced("/tmp/test", ".txt", ".md", dry_run=True)

# 确认后执行
# batch_rename_advanced("/tmp/test", ".txt", ".md", dry_run=False)
```

---

### 3.2 统计目录下各类型文件数量

#### 概念说明

统计文件类型是日常工作中常见的需求，可以用来了解项目的文件构成。

#### 示例代码

```python
from pathlib import Path
from collections import defaultdict, Counter

def count_file_types(directory: str) -> dict[str, int]:
    """统计目录下（含子目录）各扩展名的文件数量"""
    base = Path(directory)
    type_counter: Counter = Counter()
    
    for file_path in base.rglob("*"):
        if file_path.is_file():
            ext = file_path.suffix.lower()
            if ext:
                type_counter[ext] += 1
            else:
                type_counter["(无后缀)"] += 1
    
    return dict(type_counter)


def print_file_type_report(directory: str) -> None:
    """打印文件类型统计报告"""
    counter = count_file_types(directory)
    
    if not counter:
        print("目录为空或不存在")
        return
    
    # 按数量从多到少排序
    sorted_types = sorted(counter.items(), key=lambda x: x[1], reverse=True)
    
    total = sum(counter.values())
    
    print(f"目录：{directory}")
    print(f"{'─' * 40}")
    print(f"{'扩展名':<15} {'数量':>6}  {'占比':>6}")
    print(f"{'─' * 40}")
    
    for ext, count in sorted_types:
        percentage = count / total * 100
        bar = "█" * int(percentage / 5)   # 简单的进度条
        print(f"{ext:<15} {count:>6}  {percentage:>5.1f}%  {bar}")
    
    print(f"{'─' * 40}")
    print(f"{'合计':<15} {total:>6}")


# 使用示例
print_file_type_report(".")

# 输出示例：
# 目录：.
# ────────────────────────────────────────
# 扩展名          数量    占比
# ────────────────────────────────────────
# .py              45   52.3%  ██████████
# .md              20   23.3%  ████
# .json             8    9.3%  █
# .txt              5    5.8%  █
# .yml              4    4.7%  
# (无后缀)          4    4.7%  
# ────────────────────────────────────────
# 合计             86


# 进阶版：按类别分组统计
def count_by_category(directory: str) -> dict[str, list[str]]:
    """按类别统计文件（代码、文档、图片、数据等）"""
    categories = {
        "代码":   {".py", ".js", ".ts", ".java", ".go", ".rs", ".c", ".cpp"},
        "文档":   {".md", ".txt", ".rst", ".pdf", ".docx"},
        "图片":   {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"},
        "数据":   {".json", ".yaml", ".yml", ".toml", ".csv", ".xml"},
        "配置":   {".ini", ".cfg", ".conf", ".env"},
    }
    
    result: dict[str, list[str]] = defaultdict(list)
    base = Path(directory)
    
    for file_path in base.rglob("*"):
        if not file_path.is_file():
            continue
        ext = file_path.suffix.lower()
        categorized = False
        for category, exts in categories.items():
            if ext in exts:
                result[category].append(str(file_path))
                categorized = True
                break
        if not categorized:
            result["其他"].append(str(file_path))
    
    return dict(result)
```

---

### 3.3 创建项目目录结构

#### 概念说明

开始新项目时，需要创建标准的目录结构。用 Python 自动化这个过程，可以保证结构一致性。

```
典型 Python 项目目录结构
my_project/
├── src/
│   └── my_project/
│       ├── __init__.py
│       └── main.py
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── docs/
│   └── README.md
├── data/
│   ├── raw/
│   └── processed/
├── scripts/
├── .gitignore
├── README.md
├── pyproject.toml
└── requirements.txt
```

#### 示例代码

```python
from pathlib import Path

def create_python_project(project_name: str, base_dir: str = ".") -> Path:
    """
    创建标准 Python 项目目录结构
    
    参数：
        project_name: 项目名称
        base_dir:     创建位置（默认当前目录）
    
    返回：
        创建的项目根目录路径
    """
    base = Path(base_dir)
    project_root = base / project_name
    
    if project_root.exists():
        raise FileExistsError(f"项目目录已存在：{project_root}")
    
    # 定义目录结构
    directories = [
        f"src/{project_name}",
        "tests",
        "docs",
        "data/raw",
        "data/processed",
        "scripts",
    ]
    
    # 创建所有目录
    for dir_path in directories:
        (project_root / dir_path).mkdir(parents=True, exist_ok=True)
    
    # 定义需要创建的文件和初始内容
    files = {
        "README.md": f"# {project_name}\n\n项目描述\n",
        
        f"src/{project_name}/__init__.py": f'"""\\n{project_name} 包\\n"""\n',
        
        f"src/{project_name}/main.py": (
            f'"""\\n{project_name} 主模块\\n"""\n\n'
            "def main() -> None:\n"
            f'    print("Hello from {project_name}!")\n\n\n'
            'if __name__ == "__main__":\n'
            "    main()\n"
        ),
        
        "tests/__init__.py": "",
        
        "tests/test_main.py": (
            f"from src.{project_name}.main import main\n\n\n"
            "def test_main() -> None:\n"
            "    # TODO: 添加实际测试\n"
            "    assert True\n"
        ),
        
        ".gitignore": (
            "__pycache__/\n"
            "*.pyc\n"
            ".venv/\n"
            "dist/\n"
            "*.egg-info/\n"
            ".env\n"
        ),
        
        "pyproject.toml": (
            "[project]\n"
            f'name = "{project_name}"\n'
            'version = "0.1.0"\n'
            'requires-python = ">=3.11"\n'
            "dependencies = []\n"
        ),
    }
    
    # 创建所有文件
    for file_path, content in files.items():
        full_path = project_root / file_path
        full_path.write_text(content, encoding="utf-8")
    
    # 打印创建结果
    print(f"项目 '{project_name}' 创建成功！")
    print(f"位置：{project_root.resolve()}")
    print("\n目录结构：")
    _print_tree(project_root)
    
    return project_root


def _print_tree(path: Path, prefix: str = "", is_last: bool = True) -> None:
    """递归打印目录树"""
    connector = "└── " if is_last else "├── "
    print(prefix + connector + path.name)
    
    if path.is_dir():
        children = sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name))
        for i, child in enumerate(children):
            is_last_child = i == len(children) - 1
            extension = "    " if is_last else "│   "
            _print_tree(child, prefix + extension, is_last_child)


# 使用示例
create_python_project("awesome_app", base_dir="/tmp")
```

---

### 3.4 查找大文件

#### 概念说明

磁盘空间不足时，经常需要找出占用空间最多的大文件。这是 `os.walk` 或 `pathlib.rglob` 的典型应用场景。

#### 示例代码

```python
from pathlib import Path

def find_large_files(
    directory: str,
    min_size_mb: float = 100,
    top_n: int = 10
) -> list[tuple[Path, int]]:
    """
    查找目录下的大文件
    
    参数：
        directory:    搜索目录
        min_size_mb:  最小文件大小（MB），只返回大于此值的文件
        top_n:        返回最大的前 N 个文件
    
    返回：
        [(文件路径, 文件大小字节)] 列表，按大小降序排列
    """
    min_size_bytes = int(min_size_mb * 1024 * 1024)
    base = Path(directory)
    large_files = []
    
    print(f"正在扫描 {directory} ...")
    
    for file_path in base.rglob("*"):
        if not file_path.is_file():
            continue
        try:
            size = file_path.stat().st_size
            if size >= min_size_bytes:
                large_files.append((file_path, size))
        except (PermissionError, OSError):
            # 跳过无权限访问的文件
            continue
    
    # 按大小从大到小排序
    large_files.sort(key=lambda x: x[1], reverse=True)
    
    return large_files[:top_n]


def format_size(size_bytes: int) -> str:
    """将字节数格式化为人类可读的大小"""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} PB"


def print_large_files_report(directory: str, min_size_mb: float = 50) -> None:
    """打印大文件报告"""
    results = find_large_files(directory, min_size_mb)
    
    if not results:
        print(f"未找到大于 {min_size_mb} MB 的文件")
        return
    
    print(f"\n大文件报告（大于 {min_size_mb} MB）：")
    print(f"{'─' * 70}")
    print(f"{'大小':>10}  文件路径")
    print(f"{'─' * 70}")
    
    for file_path, size in results:
        print(f"{format_size(size):>10}  {file_path}")
    
    total = sum(size for _, size in results)
    print(f"{'─' * 70}")
    print(f"{format_size(total):>10}  合计（{len(results)} 个文件）")


# 使用示例
print_large_files_report("/Users/baxiang/Downloads", min_size_mb=50)

# 输出示例：
# 大文件报告（大于 50 MB）：
# ──────────────────────────────────────────────────────────────────────
#       大小  文件路径
# ──────────────────────────────────────────────────────────────────────
#   2.1 GB  /Users/baxiang/Downloads/ubuntu-22.04.iso
# 512.0 MB  /Users/baxiang/Downloads/dataset.zip
#  89.3 MB  /Users/baxiang/Downloads/video.mp4
# ──────────────────────────────────────────────────────────────────────
#   2.7 GB  合计（3 个文件）
```

---

## 第四部分：os vs pathlib 对比速查表

### 4.1 完整对比表

#### 概念说明

下面是 `os`/`os.path` 和 `pathlib` 最常用操作的完整对比表，便于查阅和对照学习。

```
os / os.path  vs  pathlib 完整对比
┌──────────────────────────────────────┬──────────────────────────────────────┐
│          os / os.path                │           pathlib.Path               │
├──────────────────────────────────────┼──────────────────────────────────────┤
│  【路径创建与拼接】                   │                                      │
│  os.path.join(a, b, c)              │  Path(a) / b / c                     │
│  os.path.abspath("rel")             │  Path("rel").resolve()               │
│  os.path.expanduser("~")            │  Path.home()                         │
│  os.getcwd()                        │  Path.cwd()                          │
├──────────────────────────────────────┼──────────────────────────────────────┤
│  【路径解析】                         │                                      │
│  os.path.basename(p)               │  Path(p).name                        │
│  os.path.dirname(p)                │  Path(p).parent                      │
│  os.path.splitext(p)[0]            │  Path(p).stem                        │
│  os.path.splitext(p)[1]            │  Path(p).suffix                      │
│  p.split(os.sep)                   │  Path(p).parts                       │
├──────────────────────────────────────┼──────────────────────────────────────┤
│  【路径判断】                         │                                      │
│  os.path.exists(p)                 │  Path(p).exists()                    │
│  os.path.isfile(p)                 │  Path(p).is_file()                   │
│  os.path.isdir(p)                  │  Path(p).is_dir()                    │
│  os.path.isabs(p)                  │  Path(p).is_absolute()               │
│  os.path.islink(p)                 │  Path(p).is_symlink()                │
├──────────────────────────────────────┼──────────────────────────────────────┤
│  【目录操作】                         │                                      │
│  os.mkdir(p)                       │  Path(p).mkdir()                     │
│  os.makedirs(p, exist_ok=True)     │  Path(p).mkdir(parents=True,         │
│                                    │           exist_ok=True)             │
│  os.rmdir(p)                       │  Path(p).rmdir()                     │
│  os.listdir(p)                     │  list(Path(p).iterdir())             │
│  os.getcwd()                       │  Path.cwd()                          │
│  os.chdir(p)                       │  os.chdir(p) (pathlib 无此方法)      │
├──────────────────────────────────────┼──────────────────────────────────────┤
│  【文件操作】                         │                                      │
│  os.rename(src, dst)               │  Path(src).rename(dst)               │
│  os.replace(src, dst)              │  Path(src).replace(dst)              │
│  os.remove(p)                      │  Path(p).unlink()                    │
│  open(p).read()                    │  Path(p).read_text()                 │
│  open(p, "rb").read()              │  Path(p).read_bytes()                │
│  open(p, "w").write(s)             │  Path(p).write_text(s)               │
│  os.path.getsize(p)                │  Path(p).stat().st_size              │
├──────────────────────────────────────┼──────────────────────────────────────┤
│  【遍历】                             │                                      │
│  os.walk(p)                        │  Path(p).rglob("*")                  │
│  for f in os.listdir(p)            │  for f in Path(p).iterdir()          │
│  glob.glob("*.py")                 │  Path(".").glob("*.py")              │
│  glob.glob("**/*.py", recursive=T) │  Path(".").rglob("*.py")             │
├──────────────────────────────────────┼──────────────────────────────────────┤
│  【路径修改】                         │                                      │
│  手动字符串拼接                      │  Path(p).with_suffix(".md")          │
│  手动字符串拼接                      │  Path(p).with_name("new.txt")        │
│  手动字符串拼接                      │  Path(p).with_stem("new")            │
└──────────────────────────────────────┴──────────────────────────────────────┘
```

---

### 4.2 选择建议

#### 概念说明

两个模块都可以完成文件系统操作，应该如何选择？

```
选择建议
┌─────────────────────────────────────────────────────────────┐
│  推荐 pathlib 的场景：                                      │
│  ✔  新项目、新代码                                         │
│  ✔  需要大量路径拼接和属性访问                             │
│  ✔  代码可读性要求高                                       │
│  ✔  Python 3.6+                                           │
│                                                             │
│  仍需 os 的场景：                                           │
│  ✔  os.walk()（pathlib 没有完全等价的替代）                │
│  ✔  os.environ（环境变量）                                 │
│  ✔  os.chdir()（切换工作目录）                             │
│  ✔  维护旧代码                                             │
│  ✔  某些第三方库只接受字符串路径（用 str(path) 转换）      │
└─────────────────────────────────────────────────────────────┘
```

实际上，两者可以混用。`pathlib.Path` 对象在大多数接受文件路径的函数（如 `open()`、`os.stat()`）中都可以直接使用，不需要转为字符串。

#### 示例代码

```python
from pathlib import Path
import os

# pathlib 和 os 混用示例
config_path = Path("config") / "settings.json"

# pathlib Path 对象可以直接用于 open()
with open(config_path, "r", encoding="utf-8") as f:
    content = f.read()

# pathlib Path 对象可以直接用于 os.stat()
stat = os.stat(config_path)
print(stat.st_size)

# os.walk 遍历，结合 pathlib 处理路径
for dirpath, dirnames, filenames in os.walk("."):
    for filename in filenames:
        # 用 pathlib 做路径操作
        full_path = Path(dirpath) / filename
        if full_path.suffix == ".py":
            print(full_path.stem)   # 文件名（不含后缀）

# 最佳实践：在函数签名里接受两种类型
from pathlib import Path

def process_file(path: str | Path) -> None:
    """接受字符串或 Path 对象"""
    path = Path(path)   # 统一转为 Path 对象
    
    if not path.exists():
        raise FileNotFoundError(f"文件不存在：{path}")
    
    content = path.read_text(encoding="utf-8")
    print(f"处理文件：{path.name}，大小：{len(content)} 字节")

# 两种调用方式都可以
process_file("README.md")
process_file(Path("README.md"))
```

---

### 4.3 常见错误和注意事项

#### 概念说明

使用文件系统操作时，有一些常见的陷阱需要注意。

#### 示例代码

```python
from pathlib import Path
import os

# ============================================================
# 错误 1：用字符串拼接路径（跨平台问题）
# ============================================================

# 错误写法（Windows 上会出问题，分隔符不同）
# path = base + "/" + subdir + "/" + filename

# 正确写法
path = Path(base) / subdir / filename
# 或
path = os.path.join(base, subdir, filename)


# ============================================================
# 错误 2：不处理路径不存在的情况
# ============================================================

# 错误写法（文件不存在时直接崩溃）
# content = Path("data.txt").read_text()

# 正确写法
p = Path("data.txt")
if p.exists():
    content = p.read_text(encoding="utf-8")
else:
    print("文件不存在")

# 或者用异常处理
try:
    content = Path("data.txt").read_text(encoding="utf-8")
except FileNotFoundError:
    print("文件不存在")


# ============================================================
# 错误 3：删除非空目录用 rmdir
# ============================================================

# 错误（非空目录会报错 OSError）
# Path("non_empty_dir").rmdir()

# 正确：删除非空目录用 shutil.rmtree
import shutil
shutil.rmtree("non_empty_dir", ignore_errors=True)


# ============================================================
# 错误 4：混淆 Path.resolve() 和 Path.absolute()
# ============================================================

p = Path("../parent/file.txt")
print(p.absolute())   # 相对于当前目录的绝对路径（不解析 ..）
print(p.resolve())    # 解析所有符号链接和 ..，得到真实路径
# resolve() 更安全，推荐用 resolve()


# ============================================================
# 错误 5：忘记 iterdir() 返回生成器
# ============================================================

# 如果需要多次遍历，先转为列表
items = list(Path(".").iterdir())

# 直接用 for 循环只能遍历一次
items_gen = Path(".").iterdir()
first_pass  = list(items_gen)   # 有内容
second_pass = list(items_gen)   # 空列表！生成器已耗尽


# ============================================================
# 错误 6：不处理权限错误
# ============================================================

for file_path in Path("/").rglob("*"):
    try:
        size = file_path.stat().st_size
    except PermissionError:
        continue   # 跳过无权限的文件
    except OSError:
        continue   # 跳过其他系统错误（如符号链接循环）
```

---

## 总结

本章介绍了 Python 文件系统操作的两个核心模块：

```
知识点总结
┌─────────────────────────────────────────────────────────────────┐
│  os 模块                                                        │
│  ├── 目录操作：getcwd / chdir / mkdir / makedirs / rmdir        │
│  ├── 文件操作：rename / replace / remove / listdir / stat       │
│  ├── 路径操作：os.path.join / basename / dirname / exists 等    │
│  ├── 遍历：os.walk（返回三元组：当前路径/子目录/文件列表）       │
│  └── 环境变量：os.environ.get / os.environ["KEY"]              │
│                                                                 │
│  pathlib 模块                                                   │
│  ├── 路径创建：Path(".")  Path.home()  Path.cwd()              │
│  ├── 路径拼接：Path(a) / b / c（/ 运算符）                      │
│  ├── 路径属性：.name / .stem / .suffix / .parent / .parts       │
│  ├── 路径判断：.exists() / .is_file() / .is_dir()              │
│  ├── 路径修改：.with_suffix() / .with_name() / .with_stem()     │
│  ├── 目录操作：.mkdir() / .rmdir() / .iterdir()                │
│  ├── 文件读写：.read_text() / .write_text() / .unlink()        │
│  └── 模式匹配：.glob("*.py") / .rglob("**/*.py")               │
│                                                                 │
│  选择原则                                                       │
│  ├── 新代码优先用 pathlib                                       │
│  ├── 环境变量、os.walk 等场景仍用 os                           │
│  └── 两者可以混用，Path 对象大多数情况可直接替代字符串路径      │
└─────────────────────────────────────────────────────────────────┘
```

---

[返回索引](../README.md) | [返回 11-模块与包](../11-模块与包.md)
