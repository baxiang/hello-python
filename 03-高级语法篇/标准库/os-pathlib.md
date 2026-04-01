# os 与 pathlib 参考

Python 提供两种路径处理方式：传统 os 模块和现代 pathlib 模块。

---

## pathlib 模块（推荐）

### Path 基础

```python
from pathlib import Path

# 创建 Path 对象
p = Path('data/file.txt')
p = Path('/home/user/documents')

# 当前目录
print(Path.cwd())

# 用户主目录
print(Path.home())

# 路径拼接
p = Path('data') / 'subdir' / 'file.txt'
print(p)  # data/subdir/file.txt
```

### 路径属性

```python
from pathlib import Path

p = Path('/home/user/documents/report.pdf')

# 路径各部分
print(p.name)      # report.pdf（文件名）
print(p.stem)      # report（不含扩展名）
print(p.suffix)    # .pdf（扩展名）
print(p.suffixes)  # ['.pdf']（所有扩展名）
print(p.parent)    # /home/user/documents（父目录）
print(p.anchor)    # /（根路径）
print(p.parts)     # ('/', 'home', 'user', 'documents', 'report.pdf')

# 路径信息
print(p.exists())       # 是否存在
print(p.is_file())      # 是否是文件
print(p.is_dir())       # 是否是目录
print(p.is_absolute())  # 是否是绝对路径
print(p.is_symlink())   # 是否是符号链接
```

### 路径操作

```python
from pathlib import Path

p = Path('data/file.txt')

# 转换
print(p.absolute())     # 绝对路径
print(p.resolve())      # 解析符号链接后的绝对路径
print(p.as_posix())     # POSIX 格式路径
print(p.as_uri())       # file:// URI

# 修改路径
print(p.with_name('new_file.txt'))     # 替换文件名
print(p.with_stem('new_name'))          # 替换文件名（不含扩展名）
print(p.with_suffix('.md'))             # 替换扩展名

# 相对路径
base = Path('/home/user')
p = Path('/home/user/documents/file.txt')
print(p.relative_to(base))  # documents/file.txt
```

### 目录操作

```python
from pathlib import Path

# 创建目录
p = Path('data/output')
p.mkdir()  # 创建目录
p.mkdir(parents=True, exist_ok=True)  # 递归创建，已存在不报错

# 遍历目录
p = Path('data')
for item in p.iterdir():
    print(item.name, item.is_file(), item.is_dir())

# glob 模式匹配
for txt_file in p.glob('*.txt'):
    print(txt_file)

# 递归匹配
for py_file in p.rglob('*.py'):
    print(py_file)

# 删除空目录
p.rmdir()
```

### 文件操作

```python
from pathlib import Path

p = Path('data/file.txt')

# 读写文本
content = p.read_text(encoding='utf-8')
p.write_text('Hello, World!', encoding='utf-8')

# 读写二进制
data = p.read_bytes()
p.write_bytes(b'\x00\x01\x02')

# 重命名
p.rename('new_name.txt')
p.rename(Path('new_dir/new_name.txt'))

# 删除文件
p.unlink()
p.unlink(missing_ok=True)  # 文件不存在不报错
```

---

## os 模块

### 环境变量

```python
import os

# 获取环境变量
print(os.environ.get('HOME'))
print(os.environ.get('PATH'))
print(os.getenv('MY_VAR', 'default'))  # 带默认值

# 设置环境变量
os.environ['MY_VAR'] = 'value'

# 删除环境变量
del os.environ['MY_VAR']
```

### 目录操作

```python
import os

# 当前目录
print(os.getcwd())

# 切换目录
os.chdir('/path/to/dir')

# 创建目录
os.mkdir('new_dir')           # 创建单层目录
os.makedirs('a/b/c')          # 递归创建目录

# 删除目录
os.rmdir('empty_dir')         # 删除空目录
os.removedirs('a/b/c')        # 递归删除空目录

# 列出目录内容
for item in os.listdir('.'):
    print(item)
```

### 文件操作

```python
import os

# 重命名
os.rename('old.txt', 'new.txt')

# 删除文件
os.remove('file.txt')
os.unlink('file.txt')  # 同上

# 文件信息
stat = os.stat('file.txt')
print(stat.st_size)    # 文件大小
print(stat.st_mtime)   # 修改时间
print(stat.st_mode)    # 文件权限

# 文件测试
print(os.path.exists('file.txt'))
print(os.path.isfile('file.txt'))
print(os.path.isdir('dir'))
```

---

## os.path 模块

### 路径操作

```python
import os.path

# 路径拼接
path = os.path.join('data', 'subdir', 'file.txt')
print(path)  # data/subdir/file.txt

# 路径分解
print(os.path.split('/home/user/file.txt'))  # ('/home/user', 'file.txt')
print(os.path.splitext('file.txt'))          # ('file', '.txt')

# 路径各部分
print(os.path.dirname('/home/user/file.txt'))  # /home/user
print(os.path.basename('/home/user/file.txt')) # file.txt

# 绝对路径
print(os.path.abspath('file.txt'))
print(os.path.realpath('symlink'))  # 解析符号链接

# 相对路径
print(os.path.relpath('/home/user/file.txt', '/home'))
# user/file.txt
```

### 路径测试

```python
import os.path

# 存在性测试
print(os.path.exists('file.txt'))
print(os.path.lexists('symlink'))  # 符号链接本身存在

# 类型测试
print(os.path.isfile('file.txt'))
print(os.path.isdir('directory'))
print(os.path.islink('symlink'))
print(os.path.ismount('/'))

# 路径属性
print(os.path.isabs('/home/user'))  # 是否绝对路径
print(os.path.samefile('a.txt', 'b.txt'))  # 是否同一文件
```

---

## 对比：pathlib vs os.path

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