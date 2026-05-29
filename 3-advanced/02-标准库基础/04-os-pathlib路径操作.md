# 04-os-pathlib路径操作

> Python 3.11+

---

## 为什么需要 os / pathlib？

### 问题场景

你需要读取一个数据文件，路径要兼容 Windows 和 macOS：

```python
# ❌ 字符串拼接路径：Windows 用 \，macOS/Linux 用 /，直接写死会报错
path = "data" + "/" + "2024" + "/" + "report.csv"

# ✅ pathlib：自动处理跨平台分隔符，代码清晰
from pathlib import Path
path = Path("data") / "2024" / "report.csv"   # 跨平台，Windows/macOS 均正常
print(path.stem)     # report（文件名无扩展名）
print(path.suffix)   # .csv（扩展名）
print(path.parent)   # data/2024（父目录）
```

`pathlib` 是 Python 3.4+ 推荐的路径处理方式，面向对象、跨平台；`os` 模块提供环境变量、进程等系统级操作。

---

## 概念铺垫

`pathlib` 和 `os`/`os.path` 是两种不同时代的路径处理范式。理解它们的底层差异有助于编写高效的跨平台代码。

```
┌──────────────────────────────────────────────────────────────┐
│          pathlib 类型系统                                     │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   PurePath  ← 纯路径操作，不访问文件系统                       │
│     ├── PurePosixPath   → Unix/POSIX 语义，正斜杠 /           │
│     └── PureWindowsPath  → Windows 语义，反斜杠 \             │
│                                                              │
│   Path  ← 具体路径操作，访问文件系统                           │
│     ├── PosixPath     → Unix/POSIX 实际文件系统               │
│     └── WindowsPath   → Windows 实际文件系统                  │
│                                                              │
│   关键区别：                                                  │
│   · PurePath：可在 Windows 上创建 POSIX 路径而不报错          │
│   · Path：创建类的实例必须匹配当前操作系统                    │
│   · PurePath 不能做 stat()、exists() 等 I/O 操作              │
│                                                              │
│   os.scandir() 优化：                                         │
│   · os.listdir(): 返回字符串列表，每项再 stat() 一次           │
│   · os.scandir(): 返回 DirEntry 迭代器，stat 信息已缓存       │
│   · pathlib.iterdir() 内部使用 os.scandir() 实现              │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### L1 理解层：会用

## 第一部分：pathlib 现代路径操作（推荐）

### 1.1 Path 基础

#### 实际场景

在文件处理、配置管理、数据存储等场景中，需要处理文件路径。比如读取配置文件、保存数据文件、组织项目结构等。

**问题：为什么要使用 pathlib 而不是字符串拼接路径？**

```python
from pathlib import Path

# 创建 Path 对象
p1: Path = Path('data/file.txt')
p2: Path = Path('/home/user/documents')

# 当前目录
cwd: Path = Path.cwd()

# 用户主目录
home: Path = Path.home()

# 路径拼接
p3: Path = Path('data') / 'subdir' / 'file.txt'
print(p3)  # data/subdir/file.txt
```

### 1.2 路径属性

#### 实际场景

在文件处理中，经常需要提取文件名、扩展名、父目录等信息。比如批量重命名文件、按扩展名分类文件等。

**问题：如何获取文件名、扩展名、父目录等路径组成部分？**

```python
from pathlib import Path

p: Path = Path('/home/user/documents/report.pdf')

# 路径各部分
name: str = p.name        # report.pdf（文件名）
stem: str = p.stem        # report（不含扩展名）
suffix: str = p.suffix    # .pdf（扩展名）
suffixes: list[str] = p.suffixes  # ['.pdf']（所有扩展名）
parent: Path = p.parent   # /home/user/documents（父目录）
anchor: str = p.anchor    # /（根路径）
parts: tuple[str, ...] = p.parts   # ('/', 'home', 'user', 'documents', 'report.pdf')

# 路径信息
exists: bool = p.exists()       # 是否存在
is_file: bool = p.is_file()     # 是否是文件
is_dir: bool = p.is_dir()       # 是否是目录
is_absolute: bool = p.is_absolute()  # 是否是绝对路径
is_symlink: bool = p.is_symlink()     # 是否是符号链接
```

### 1.3 路径操作

#### 实际场景

在文件处理中，经常需要转换路径格式、修改文件名、计算相对路径等。比如生成文件 URL、修改文件扩展名等。

**问题：如何获取绝对路径？如何修改文件名和扩展名？如何计算相对路径？**

```python
from pathlib import Path

p: Path = Path('data/file.txt')

# 转换
absolute_path: Path = p.absolute()     # 绝对路径
resolved_path: Path = p.resolve()       # 解析符号链接后的绝对路径
posix_path: str = p.as_posix()          # POSIX 格式路径
uri: str = p.as_uri()                   # file:// URI

# 修改路径
new_name: Path = p.with_name('new_file.txt')       # 替换文件名
new_stem: Path = p.with_stem('new_name')           # 替换文件名（不含扩展名）
new_suffix: Path = p.with_suffix('.md')            # 替换扩展名

# 相对路径
base: Path = Path('/home/user')
full_path: Path = Path('/home/user/documents/file.txt')
relative: Path = full_path.relative_to(base)  # documents/file.txt
```

### 1.4 目录操作

#### 实际场景

在数据管理、文件组织、批量处理等场景中，需要创建、遍历、删除目录。比如创建输出目录、遍历数据文件、清理临时目录等。

**问题：如何创建多层目录？如何遍历目录内容？如何使用通配符匹配文件？**

```python
from pathlib import Path

# 创建目录
p: Path = Path('data/output')
p.mkdir()  # 创建目录
p.mkdir(parents=True, exist_ok=True)  # 递归创建，已存在不报错

# 遍历目录
data_dir: Path = Path('data')
for item in data_dir.iterdir():
    item_name: str = item.name
    item_is_file: bool = item.is_file()
    item_is_dir: bool = item.is_dir()
    print(item_name, item_is_file, item_is_dir)

# glob 模式匹配
for txt_file in data_dir.glob('*.txt'):
    print(txt_file)

# 递归匹配
for py_file in data_dir.rglob('*.py'):
    print(py_file)

# 删除空目录
empty_dir: Path = Path('empty_folder')
empty_dir.rmdir()
```

### 1.5 文件操作

#### 实际场景

在数据处理、配置管理、文件转换等场景中，需要读写文件内容、重命名文件、删除文件等。

**问题：如何使用 pathlib 读写文件？如何重命名和删除文件？**

```python
from pathlib import Path

p: Path = Path('data/file.txt')

# 读写文本
content: str = p.read_text(encoding='utf-8')
bytes_written: int = p.write_text('Hello, World!', encoding='utf-8')

# 读写二进制
data: bytes = p.read_bytes()
bytes_written: int = p.write_bytes(b'\x00\x01\x02')

# 重命名
new_path: Path = p.rename('new_name.txt')
new_path2: Path = p.rename(Path('new_dir/new_name.txt'))

# 删除文件
p.unlink()
p.unlink(missing_ok=True)  # 文件不存在不报错
```

## 第二部分：os 模块

### 2.1 环境变量

#### 实际场景

在配置管理、跨平台开发、Docker 容器等场景中，需要读取和设置环境变量。比如获取数据库连接信息、设置调试模式等。

**问题：如何安全地获取环境变量？如何设置和删除环境变量？**

```python
import os

# 获取环境变量
home: str | None = os.environ.get('HOME')
path_env: str | None = os.environ.get('PATH')
my_var: str = os.getenv('MY_VAR', 'default')  # 带默认值

# 设置环境变量
os.environ['MY_VAR'] = 'value'

# 删除环境变量
del os.environ['MY_VAR']
```

### 2.2 目录操作

#### 实际场景

在文件系统管理、脚本执行、项目导航等场景中，需要获取当前目录、切换目录、创建和删除目录。

**问题：os.mkdir() 和 os.makedirs() 有什么区别？**

```python
import os

# 当前目录
cwd: str = os.getcwd()

# 切换目录
os.chdir('/path/to/dir')

# 创建目录
os.mkdir('new_dir')           # 创建单层目录
os.makedirs('a/b/c')          # 递归创建目录

# 删除目录
os.rmdir('empty_dir')         # 删除空目录
os.removedirs('a/b/c')        # 递归删除空目录

# 列出目录内容
items: list[str] = os.listdir('.')
for item in items:
    print(item)
```

### 2.3 文件操作

#### 实际场景

在文件管理、批量处理、文件同步等场景中，需要重命名、删除、获取文件信息等。

**问题：如何获取文件的大小、修改时间等属性？**

```python
import os

# 重命名
os.rename('old.txt', 'new.txt')

# 删除文件
os.remove('file.txt')
os.unlink('file.txt')  # 同上

# 文件信息
stat_info: os.stat_result = os.stat('file.txt')
size: int = stat_info.st_size      # 文件大小
mtime: float = stat_info.st_mtime  # 修改时间
mode: int = stat_info.st_mode      # 文件权限

# 文件测试
exists: bool = os.path.exists('file.txt')
is_file: bool = os.path.isfile('file.txt')
is_dir: bool = os.path.isdir('dir')
```

## 第三部分：os.path 传统路径操作

### 3.1 路径操作

#### 实际场景

在维护旧代码、兼容性要求高的项目中，可能需要使用 os.path 模块。了解其用法有助于阅读和迁移代码。

**问题：os.path 和 pathlib 有什么区别？如何选择？**

```python
import os.path

# 路径拼接
path: str = os.path.join('data', 'subdir', 'file.txt')
print(path)  # data/subdir/file.txt

# 路径分解
dir_name: str
file_name: str
dir_name, file_name = os.path.split('/home/user/file.txt')  # ('/home/user', 'file.txt')
base_name: str
ext: str
base_name, ext = os.path.splitext('file.txt')  # ('file', '.txt')

# 路径各部分
dirname: str = os.path.dirname('/home/user/file.txt')     # /home/user
basename: str = os.path.basename('/home/user/file.txt')   # file.txt

# 绝对路径
abs_path: str = os.path.abspath('file.txt')
real_path: str = os.path.realpath('symlink')  # 解析符号链接

# 相对路径
rel_path: str = os.path.relpath('/home/user/file.txt', '/home')
# user/file.txt
```

### 3.2 路径测试

#### 实际场景

在文件处理前，需要检查路径是否存在、是否为文件或目录等，以避免错误。

**问题：如何检查路径是否存在？如何判断是文件还是目录？**

```python
import os.path

# 存在性测试
exists: bool = os.path.exists('file.txt')
lexists: bool = os.path.lexists('symlink')  # 符号链接本身存在

# 类型测试
is_file: bool = os.path.isfile('file.txt')
is_dir: bool = os.path.isdir('directory')
is_link: bool = os.path.islink('symlink')
is_mount: bool = os.path.ismount('/')

# 路径属性
is_absolute: bool = os.path.isabs('/home/user')  # 是否绝对路径
same_file: bool = os.path.samefile('a.txt', 'b.txt')  # 是否同一文件
```

## 第四部分：pathlib vs os.path 对比

### 4.1 功能对比

#### 实际场景

在代码迁移、技术选型时，需要了解两种方式的差异，以便做出正确的选择。

**问题：pathlib 和 os.path 各有什么优缺点？**

| 操作 | pathlib | os.path |
|------|---------|---------|
| 当前目录 | `Path.cwd()` | `os.getcwd()` |
| 路径拼接 | `Path('a') / 'b'` | `os.path.join('a', 'b')` |
| 文件名 | `p.name` | `os.path.basename(p)` |
| 父目录 | `p.parent` | `os.path.dirname(p)` |
| 扩展名 | `p.suffix` | `os.path.splitext(p)[1]` |
| 是否存在 | `p.exists()` | `os.path.exists(p)` |
| 是否文件 | `p.is_file()` | `os.path.isfile(p)` |
| 是否目录 | `p.is_dir()` | `os.path.isdir(p)` |
| 绝对路径 | `p.absolute()` | `os.path.abspath(p)` |
| 创建目录 | `p.mkdir()` | `os.mkdir(p)` |
| 列出目录 | `p.iterdir()` | `os.listdir(p)` |
| glob 匹配 | `p.glob('*.txt')` | `glob.glob('*.txt')` |

**推荐使用 pathlib**：面向对象、代码更清晰、功能更强大。

---

### L2 实践层：用好

#### 推荐做法

| 做法 | 原因 | 示例 |
|------|------|------|
| 新代码统一用 `pathlib.Path` | 面向对象、跨平台、可读性强 | `Path("data") / "file.txt"` |
| 创建目录用 `mkdir(parents=True, exist_ok=True)` | 避免父目录不存在或目录已存在的报错 | `Path("a/b/c").mkdir(parents=True, exist_ok=True)` |
| 删除文件用 `unlink(missing_ok=True)` | 避免文件不存在时报错 | `p.unlink(missing_ok=True)` |
| 读写文件用 `read_text()`/`write_text()` | 自动处理打开/关闭，不会忘记 `close()` | `p.read_text(encoding="utf-8")` |
| 环境变量用 `os.getenv("KEY", "默认值")` | 比 `os.environ["KEY"]` 安全，不存在不报错 | `os.getenv("DB_URL", "sqlite:///dev.db")` |
| 遍历目录用 `iterdir()`，递归用 `rglob()` | 比 `os.listdir` 返回 `Path` 对象，可直接调用方法 | `Path(".").rglob("*.py")` |

#### 实际应用示例

```python
from pathlib import Path
import os

# 确保输出目录存在
output_dir = Path("output") / "2024"
output_dir.mkdir(parents=True, exist_ok=True)

# 遍历所有 Python 文件并打印行数
for py_file in Path("src").rglob("*.py"):
    lines = len(py_file.read_text(encoding="utf-8").splitlines())
    print(f"{py_file}: {lines} 行")

# 读取环境变量配置
db_host = os.getenv("DB_HOST", "localhost")
db_port = int(os.getenv("DB_PORT", "5432"))
```

#### 反模式：不要这样做

```python
# ❌ 字符串拼接路径（Windows / macOS 分隔符不同）
path = "data/" + "file.txt"

# ✅ 用 /  运算符
from pathlib import Path
path = Path("data") / "file.txt"

# ❌ mkdir 不加 exist_ok，目录已存在时报错
import os
os.makedirs("output")          # FileExistsError

# ✅
Path("output").mkdir(parents=True, exist_ok=True)

# ❌ 用 os.environ["KEY"] 读取可选环境变量
import os
host = os.environ["DB_HOST"]   # KeyError（变量不存在时）

# ✅
host = os.getenv("DB_HOST", "localhost")

# ❌ 读文件不指定编码
content = Path("file.txt").read_text()    # 不同系统默认编码不同

# ✅
content = Path("file.txt").read_text(encoding="utf-8")
```

#### 常见陷阱

| 陷阱 | 现象 | 解决方案 |
|------|------|---------|
| `Path` 对象传给只接受 `str` 的旧库 | `TypeError` | 用 `str(path)` 转换 |
| `mkdir()` 不加 `exist_ok=True` | 目录已存在时 `FileExistsError` | 加 `exist_ok=True` |
| `unlink()` 不加 `missing_ok=True` | 文件不存在时 `FileNotFoundError` | 加 `missing_ok=True` |
| `iterdir()` 不过滤类型 | 目录和文件混在一起 | 用 `is_file()`/`is_dir()` 过滤 |
| `glob("**/*.py")` 忘了 `**` | 只匹配当前层，不递归 | 用 `rglob("*.py")` 更简洁 |
| `os.chdir()` 改了全局工作目录 | 影响所有相对路径，难以回溯 | 尽量用绝对路径，避免 `chdir` |

#### 适用场景

| 场景 | 推荐方式 | 说明 |
|------|---------|------|
| 文件路径拼接与分解 | `pathlib.Path` | `/` 运算符，跨平台 |
| 文件读写 | `pathlib` 的 `read_text()`/`write_text()` | 简洁，自动关闭 |
| 目录遍历、glob | `pathlib` 的 `iterdir()`/`rglob()` | 返回 `Path` 对象，可直接操作 |
| 读取环境变量 | `os.getenv()` | 带默认值，不报错 |
| 进程操作、系统调用 | `os` / `subprocess` | `pathlib` 不覆盖这些功能 |
| 兼容旧代码 | `os.path` | 维护遗留项目时使用 |

---

### L3 专家层：深入

#### Python 如何实现

`pathlib` 模块（`Lib/pathlib.py`）是纯 Python 实现，约 1400 行。它通过 ABC（抽象基类）设计实现跨平台：

```
┌──────────────────────────────────────────────────────────────┐
│          pathlib 实现架构                                     │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   PurePath (ABC)                                              │
│   ├── _flavour 属性 → 平台风味对象（决定分隔符、大小写规则）   │
│   │                                                          │
│   │   _PosixFlavour:   sep='/',   case_sensitive=True       │
│   │   _WindowsFlavour: sep='\\',  case_sensitive=False      │
│   │                                                          │
│   ├── PurePosixPath   ─→ _flavour = _PosixFlavour()         │
│   └── PureWindowsPath ─→ _flavour = _WindowsFlavour()       │
│                                                              │
│   Path (具体路径，继承 PurePath + I/O 方法)                   │
│   ├── PosixPath    ─→ 当前 OS 是 POSIX 时使用               │
│   └── WindowsPath  ─→ 当前 OS 是 Windows 时使用             │
│                                                              │
│   Path() 工厂函数在内部根据 os.name 选择正确子类：             │
│   · os.name == 'posix' → PosixPath                          │
│   · os.name == 'nt'    → WindowsPath                        │
│                                                              │
│   os.scandir() 优化（C 实现，约 300 行）：                      │
│   · POSIX: opendir() + readdir() + stat() 批量调用           │
│   · Windows: FindFirstFileW() + FindNextFileW()              │
│   · 返回 DirEntry 对象，stat 信息已缓存（lstat 不重复系统调用）│
│   · 比 os.listdir() 快 5-20 倍（取决于目录大小和 OS）         │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

```python
# 验证：PurePath 平台独立性
from pathlib import PurePosixPath, PureWindowsPath

# 在 macOS 上创建 Windows 风格路径
win = PureWindowsPath('C:\\Users\\test\\file.txt')
print(win.parts)   # ('C:\\', 'Users', 'test', 'file.txt')
print(win.drive)   # C:

# 在 macOS 上创建 POSIX 风格路径
posix = PurePosixPath('/home/user/file.txt')
print(posix.parts)  # ('/', 'home', 'user', 'file.txt')
```

```python
# 验证：os.scandir() 性能优势
import os, timeit

# 准备测试：创建一个有 1000 个文件的临时目录
import tempfile, pathlib

with tempfile.TemporaryDirectory() as tmpdir:
    # 创建 1000 个空文件
    for i in range(1000):
        pathlib.Path(tmpdir, f"file_{i}.txt").touch()

    # listdir：每次迭代需要额外 stat 调用
    def use_listdir():
        result = []
        for name in os.listdir(tmpdir):
            path = os.path.join(tmpdir, name)
            result.append((name, os.path.getsize(path)))
        return result

    # scandir：stat 信息已缓存
    def use_scandir():
        result = []
        for entry in os.scandir(tmpdir):
            result.append((entry.name, entry.stat().st_size))
        return result

    print(f"listdir: {timeit.timeit(use_listdir, number=100):.4f}s / 100 runs")
    print(f"scandir: {timeit.timeit(use_scandir, number=100):.4f}s / 100 runs")
    # scandir 通常快 5-10 倍

# 验证：pathlib.iterdir() 使用 scandir 实现
import pathlib, inspect
# pathlib.Path.iterdir() 内部调用 os.scandir()
src = inspect.getsource(pathlib.Path.iterdir)
print("os.scandir" in src)  # True（验证使用 scandir）
```

#### 性能考量

| 操作 | 复杂度 | 说明 |
|------|--------|------|
| `Path("a") / "b"` | O(len(parts)) | 字符串拼接 + 路径规范化 |
| `p.exists()` / `p.is_file()` | O(1) 系统调用 | 单次 stat() 调用 |
| `p.iterdir()` | O(n) | n=目录项数，scandir 缓存 stat |
| `p.glob("*.txt")` | O(n + m) | n=遍历目录，m=模式匹配项数 |
| `p.rglob("*.py")` | O(N) | N=递归遍历所有文件 |
| `os.listdir(path)` | O(n) | 但每次 stat 额外系统调用 |
| `os.scandir(path)` | O(n) | stat 信息已缓存，比 listdir 快 5-10x |

#### 知识关联

```
┌──────────────────────────────────────────────────────────────┐
│          路径操作知识关联图                                   │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌──────────┐     ┌──────────┐     ┌───────────┐          │
│   │ pathlib  │────→│ PurePath │────→│ ABC 抽象  │          │
│   │  (推荐)  │     │ 纯操作   │     │ 跨平台    │          │
│   └──────────┘     └──────────┘     └───────────┘          │
│        │                                                      │
│        ↓                                                      │
│   ┌──────────┐     ┌──────────┐     ┌───────────┐          │
│   │ os.path  │     │ 字符串   │     │ 兼容旧    │          │
│   │  传统    │────→│ 操作     │────→│ 代码      │          │
│   └──────────┘     └──────────┘     └───────────┘          │
│                                                              │
│   ┌──────────┐     ┌──────────┐     ┌───────────┐          │
│   │ os 模块  │     │ 环境变量 │     │ 进程管理  │          │
│   │          │────→│ getenv   │────→│ subprocess│          │
│   └──────────┘     └──────────┘     └───────────┘          │
│                                                              │
│   ┌──────────┐     ┌──────────┐     ┌───────────┐          │
│   │ shutil   │     │ 高级操作 │     │ 复制/     │          │
│   │          │────→│ rmtree   │────→│ 移动/归档 │          │
│   └──────────┘     └──────────┘     └───────────┘          │
│                                                              │
│   选择决策：                                                  │
│   路径操作  → pathlib.Path（新代码）                          │
│   环境变量  → os.getenv()                                     │
│   目录遍历  → Path.iterdir() > os.listdir()                  │
│   文件复制  → shutil.copy2()                                  │
│   旧代码兼容 → os.path                                        │
│                                                              │
│   scandir 性能原理：                                          │
│   · Windows: FindFirstFileW 返回 WIN32_FIND_DATA             │
│     已包含文件大小、时间戳、属性，无需额外 GetFileAttributes  │
│   · Linux: getdents64() 返回 struct dirent                   │
│     包含 d_type（DT_REG/DT_DIR），无需额外 stat()            │
│   · 这就是为什么 scandir 比 listdir + stat 快一个数量级       │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 本章小结

```
┌──────────────────────────────────────────────────────────────┐
│              os / pathlib 知识要点                            │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   pathlib.Path（推荐）：                                     │
│   Path("a") / "b"    路径拼接                                │
│   p.name  p.stem  p.suffix  p.parent   路径属性              │
│   p.exists()  p.is_file()  p.is_dir()  存在性判断            │
│   p.mkdir(parents=True, exist_ok=True) 创建目录              │
│   p.read_text(encoding="utf-8")        读文件                │
│   p.write_text(...)                    写文件                │
│   p.unlink(missing_ok=True)            删文件                │
│   p.iterdir()  p.glob()  p.rglob()     遍历目录              │
│                                                              │
│   os 模块：                                                  │
│   os.getenv("KEY", "默认值")           读环境变量             │
│   os.getcwd()  os.chdir()              工作目录               │
│   os.stat()                            文件属性               │
│                                                              │
│   原则：新代码用 pathlib，旧代码兼容用 os.path                │
│                                                              │
│   L3 要点: PurePosixPath → ABC 风味 → scandir 缓存 stat 快 10x │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```
