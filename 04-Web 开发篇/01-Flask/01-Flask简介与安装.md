# Flask 简介与安装

## 什么是 Flask

Flask 是一个轻量级的 Python Web 框架，被称为"微框架"（Microframework）。

**Flask 的核心理念：**

```
┌─────────────────────────────────────────────────────────────┐
│                    Flask 设计理念                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   核心特点：                                                │
│   • 轻量级：核心代码仅几千行                               │
│   • 灵活：不强制项目结构，按需选择扩展                     │
│   • 易上手：API 简洁直观，文档完善                          │
│   • 生态丰富：大量官方和第三方扩展                         │
│                                                             │
│   Flask vs 全栈框架（如 Django）：                          │
│   ┌───────────────────────────────────────────────────┐     │
│   │  Flask (微框架)          │  Django (全栈框架)     │     │
│   │  ├─ 核心：路由、视图     │  ├─ 自带 ORM            │     │
│   │  ├─ 扩展：按需添加       │  ├─ 自带 Admin          │     │
│   │  ├─ 数据库：Flask-SQLA   │  ├─ 自带表单系统        │     │
│   │  └─ 灵活：自由组织       │  └─ 约定：约定优于配置  │     │
│   └───────────────────────────────────────────────────┘     │
│                                                             │
│   适用场景：                                                │
│   • 小型到中型 Web 应用                                      │
│   • RESTful API 服务                                         │
│   • 快速原型开发                                             │
│   • 微服务架构                                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 安装 Flask

使用 uv 包管理器安装 Flask 及其常用扩展。

**安装步骤：**

```bash
# 1. 创建新项目
uv init my-flask-app
cd my-flask-app

# 2. 安装 Flask
uv add flask

# 3. 安装常用扩展（可选）
uv add flask-sqlalchemy    # 数据库 ORM
uv add flask-login         # 用户认证
uv add flask-wtf           # 表单处理
uv add flask-migrate       # 数据库迁移
uv add python-dotenv       # 环境变量

# 4. 运行应用
uv run python app.py
```

**项目结构建议：**

```
my-flask-app/
├── app.py              # 应用入口
├── requirements.txt    # 依赖列表
├── .env                # 环境变量
├── templates/          # HTML 模板
│   └── index.html
└── static/             # 静态文件
    ├── css/
    ├── js/
    └── images/
```

---

## 第一个 Flask 应用

一个最小的 Flask 应用只需要几行代码。

**示例代码：Hello World**

```python
# app.py
from flask import Flask

# 创建 Flask 应用实例
app = Flask(__name__)


# 定义路由和视图函数
@app.route('/')
def hello():
    return 'Hello, World!'


# 运行开发服务器
if __name__ == '__main__':
    app.run(debug=True)
```

**运行应用：**

```bash
# 方式一：直接运行 Python 文件
uv run python app.py

# 方式二：使用 flask 命令
# 设置环境变量
export FLASK_APP=app.py
export FLASK_DEBUG=1
uv run flask run
```

**输出：**

```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
```

**访问：** http://127.0.0.1:5000

---

## Flask(__name__) 参数详解

`Flask(__name__)` 中的 `__name__` 参数用于确定应用的根目录。

```python
# __name__ 的值取决于运行方式

# 方式 1：直接运行 python app.py
print(__name__)  # 输出：__main__

# 方式 2：作为模块导入 from app import app
print(__name__)  # 输出：app
```

**为什么需要 `__name__`？**

```
┌─────────────────────────────────────────────────────────────┐
│              __name__ 的作用                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   Flask 需要知道：                                          │
│   • 模板文件夹在哪里 (templates/)                           │
│   • 静态文件夹在哪里 (static/)                              │
│   • 相对路径如何解析                                        │
│                                                             │
│   使用 __name__，Flask 可以：                               │
│   • 自动定位到 app.py 所在目录                              │
│   • 正确加载 templates 和 static 文件夹                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 开发服务器与调试模式

### 开发服务器

Flask 内置了一个轻量级的开发服务器，适合开发环境使用。

**app.run() 参数详解：**

```python
app.run(
    host='127.0.0.1',   # 监听地址，0.0.0.0 表示所有网卡
    port=5000,          # 端口号
    debug=None,         # 调试模式
    load_dotenv=True,   # 加载.env 文件
    **options
)
```

**常用配置：**

```python
# 开发环境
app.run(debug=True)  # 启用调试模式

# 允许外部访问
app.run(host='0.0.0.0', port=5000)

# 指定端口
app.run(port=8080)
```

### 调试模式

调试模式启用后，代码变更会自动重载，并且提供交互式调试器。

**启用调试模式的方式：**

```python
# 方式 1：在代码中设置
app.run(debug=True)

# 方式 2：使用环境变量
export FLASK_DEBUG=1
uv run flask run

# 方式 3：使用 flask 命令
uv run flask --debug run
```

**调试模式的特性：**

```
┌─────────────────────────────────────────────────────────────┐
│                  调试模式特性                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   1. 自动重载 (Auto Reload)                                 │
│      代码修改后，服务器自动重启，无需手动停止               │
│                                                             │
│   2. 交互式调试器 (Interactive Debugger)                    │
│      出错时显示详细的堆栈信息                               │
│      可在浏览器中执行 Python 代码调试                        │
│                                                             │
│   3. 详细的错误页面                                         │
│      显示完整的 traceback                                   │
│      显示源代码和局部变量                                   │
│                                                             │
│   ⚠️ 警告：调试模式有安全风险，不要在生产环境使用！          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```