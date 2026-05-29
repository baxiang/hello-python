# 03-Jinja2模板引擎

> Python 3.11+

本章讲解 Jinja2 模板引擎的基本语法、模板继承、过滤器和宏的使用。

---

## 概念铺垫

Jinja2 是 Flask 默认的模板引擎，是一个现代且设计师友好的 Python 模板语言。它将模板编译为 Python 代码后执行，支持自动 HTML 转义（防 XSS）、模板继承、宏、过滤器和沙盒渲染。

Jinja2 配置：

```python
from flask import Flask

app: Flask = Flask(__name__)

# Jinja2 配置
app.jinja_env.auto_reload = True  # 自动重载模板
app.jinja_env.cache = None  # 模板缓存

# 自定义配置
app.jinja_env.globals.update({
    "site_name": "My Site",
    "current_year": 2024
})

# 添加自定义过滤器
def datetime_format(value: str, format: str = "%Y-%m-%d") -> str:
    if value:
        return value.strftime(format)
    return ""

app.jinja_env.filters["datetime"] = datetime_format
```

---

### L1 理解层：会用

### 2.1 实际场景

你有一个用户对象，需要在 HTML 页面中显示用户的姓名、邮箱、头像等信息。

**问题：如何在模板中输出变量？**

### 2.2 变量输出

```html
<!-- 基本变量 -->
<p>用户名: {{ user.name }}</p>
<p>邮箱: {{ user.email }}</p>

<!-- 对象属性 -->
<p>{{ user.profile.bio }}</p>

<!-- 字典 -->
<p>{{ user_dict['name'] }}</p>

<!-- 列表 -->
<p>{{ items[0] }}</p>
```

### 2.3 注释

```html
{# 这是注释，不会被输出 #}

{# 
    多行注释
    可以包含多行内容
#}
```

---

## 第三部分：条件判断

### 3.1 实际场景

用户登录后显示"欢迎"，未登录显示"请登录"。文章已发布显示内容，未发布显示"草稿"。

**问题：如何在模板中进行条件判断？**

### 3.2 if 语句

```html
{% if user.is_active %}
    <p>用户已激活</p>
{% elif user.is_pending %}
    <p>等待审核</p>
{% else %}
    <p>用户未激活</p>
{% endif %}

<!-- 简化的条件 -->
<p>{{ "欢迎" if user.is_logged_in else "请登录" }}</p>
```

### 3.3 比较运算符

```html
{% if age >= 18 %}
    <p>成年人</p>
{% else %}
    <p>未成年人</p>
{% endif %}

{% if name == 'admin' %}
    <p>管理员</p>
{% endif %}
```

### 3.4 逻辑运算符

```html
{% if user.is_active and user.has_permission %}
    <p>可以访问</p>
{% endif %}

{% if not user.is_banned %}
    <p>未被封禁</p>
{% endif %}

{% if role == 'admin' or role == 'moderator' %}
    <p>有管理权限</p>
{% endif %}
```

---

## 第四部分：循环

### 4.1 实际场景

你有一组文章需要显示为列表，每篇文章显示标题、摘要和发布日期。

**问题：如何在模板中遍历数据并渲染？**

### 4.2 for 循环

```html
<!-- 遍历列表 -->
<ul>
{% for item in items %}
    <li>{{ item }}</li>
{% endfor %}
</ul>

<!-- 遍历字典 -->
<ul>
{% for key, value in user_dict.items() %}
    <li>{{ key }}: {{ value }}</li>
{% endfor %}
</ul>

<!-- 遍历对象属性 -->
<ul>
{% for post in posts %}
    <article>
        <h2>{{ post.title }}</h2>
        <p>{{ post.content }}</p>
    </article>
{% endfor %}
</ul>
```

### 4.3 循环变量

```html
<!-- loop 变量提供循环信息 -->
<ul>
{% for item in items %}
    <li>
        索引: {{ loop.index }}        <!-- 1-based -->
        索引: {{ loop.index0 }}       <!-- 0-based -->
        首个: {{ loop.first }}
        末位: {{ loop.last }}
        总数: {{ loop.length }}
    </li>
{% endfor %}
</ul>
```

### 4.4 循环过滤

```html
<!-- 反向遍历 -->
{% for item in items|reverse %}
    <li>{{ item }}</li>
{% endfor %}

<!-- 带条件遍历 -->
{% for item in items if item.is_active %}
    <li>{{ item.name }}</li>
{% endfor %}

<!-- 限制数量 -->
{% for item in items[:10] %}
    <li>{{ item }}</li>
{% endfor %}
```

---

## 第五部分：过滤器

### 5.1 实际场景

用户名需要大写显示，文章摘要需要截断为 200 字符，日期需要格式化显示。

**问题：如何在模板中对数据进行处理？**

### 5.2 内置过滤器

```html
<!-- 字符串过滤器 -->
<p>{{ name|upper }}</p>           <!-- 大写 -->
<p>{{ name|lower }}</p>           <!-- 小写 -->
<p>{{ name|capitalize }}</p>     <!-- 首字母大写 -->
<p>{{ title|trim }}</p>           <!-- 去除空格 -->
<p>{{ text|truncate(50) }}</p>   <!-- 截断 -->

<!-- 数字过滤器 -->
<p>{{ price|round(2) }}</p>      <!-- 四舍五入 -->

<!-- 列表过滤器 -->
<p>{{ items|length }}</p>        <!-- 长度 -->
<p>{{ items|first }}</p>         <!-- 第一个 -->
<p>{{ items|last }}</p>          <!-- 最后一个 -->
<p>{{ items|sort }}</p>          <!-- 排序 -->
<p>{{ items|unique }}</p>        <!-- 去重 -->

<!-- 布尔过滤器 -->
<p>{{ value|default('N/A') }}</p>  <!-- 默认值 -->
```

### 5.3 自定义过滤器

```python
from flask import Flask

app: Flask = Flask(__name__)

# 方法一：注册过滤器
@app.template_filter("reverse")
def reverse_filter(s: str) -> str:
    return s[::-1]

# 方法二：添加到全局
def markdown_to_html(text: str) -> str:
    import markdown
    return markdown.markdown(text)

app.jinja_env.globals["markdown"] = markdown_to_html
```

```html
<!-- 使用自定义过滤器 -->
<p>{{ name|reverse }}</p>
<p>{{ content|markdown }}</p>
```

### 5.4 测试器

```html
<!-- 测试类型 -->
{% if value is defined %}
    <p>已定义</p>
{% endif %}

{% if value is none %}
    <p>是 None</p>
{% endif %}

{% if name is string %}
    <p>是字符串</p>
{% endif %}

{% if number is even %}
    <p>是偶数</p>
{% endif %}

{% if user is mapping %}
    <p>是字典</p>
{% endif %}
```

### 5.5 自定义测试器

```python
# 注册自定义测试器
@app.template_test("adult")
def is_adult(age: int) -> bool:
    return age >= 18

@app.template_test("empty_list")
def is_empty_list(items: list) -> bool:
    return len(items) == 0
```

```html
{% if user.age is adult %}
    <p>欢迎进入成人区</p>
{% endif %}

{% if items is empty_list %}
    <p>没有数据</p>
{% endif %}
```

### 5.6 常用过滤器链与组合

```html
<!-- 过滤器链：多个过滤器依次应用 -->
<p>{{ article.content|striptags|trim|truncate(200) }}</p>

<!-- 默认值链 -->
<p>{{ user.avatar|default('/static/default.png') }}</p>

<!-- 条件格式化 -->
<p>{{ "VIP" if user.level >= 3 else "普通" }}</p>

<!-- 列表过滤器组合 -->
<ul>
{% for tag in post.tags|sort|unique %}
    <li>{{ tag|capitalize }}</li>
{% endfor %}
</ul>
```

---

## 第六部分：宏

### 6.1 实际场景

多个页面都有相似的表单输入框，如登录页、注册页、修改密码页，每次重复写相同的 HTML 很繁琐。

**问题：如何复用模板中的重复代码片段？**

### 6.2 定义宏

```html
<!-- 定义输入宏 -->
{% macro input_field(name, label, type='text', value='') %}
<div class="form-group">
    <label for="{{ name }}">{{ label }}</label>
    <input type="{{ type }}" 
           id="{{ name }}" 
           name="{{ name }}" 
           value="{{ value }}">
</div>
{% endmacro %}

<!-- 定义按钮宏 -->
{% macro button(text, type='button', onclick='') %}
<button type="{{ type }}" onclick="{{ onclick }}">{{ text }}</button>
{% endmacro %}
```

### 6.3 使用宏

```html
<!-- 使用宏 -->
{{ input_field('username', '用户名') }}
{{ input_field('email', '邮箱', 'email') }}
{{ input_field('password', '密码', 'password') }}
{{ button('提交', 'submit', 'submitForm()') }}
```

### 6.4 宏的导入

```html
<!-- 导入宏文件 -->
{% from 'forms.html' import input_field, button %}

<!-- 导入并重命名 -->
{% from 'forms.html' import input_field as input %}

<!-- 导入所有 -->
{% from 'forms.html' import * %}
```

### 6.5 宏系统深度实践

```html
{# templates/macros/cards.html — 卡片组件宏库 #}

{# 基础卡片宏 #}
{% macro card(title, content, footer='', class='') %}
<div class="card {{ class }}">
    <div class="card-header">
        <h3>{{ title }}</h3>
    </div>
    <div class="card-body">
        {{ caller() if caller else content }}
    </div>
    {% if footer %}
    <div class="card-footer">
        {{ footer }}
    </div>
    {% endif %}
</div>
{% endmacro %}

{# 带调用者内容的卡片 #}
{% macro user_card(user, show_email=True) %}
    {% call card(title=user.name, class='user-card') %}
        <p>角色：{{ user.role }}</p>
        {% if show_email %}
        <p>邮箱：{{ user.email }}</p>
        {% endif %}
        <time>{{ user.created_at|date }}</time>
    {% endcall %}
{% endmacro %}

{# 分页宏 #}
{% macro pagination(page, total_pages, endpoint) %}
<nav class="pagination">
    {% if page > 1 %}
    <a href="{{ url_for(endpoint, page=page-1) }}">&laquo; 上一页</a>
    {% endif %}

    {% for p in range(1, total_pages + 1) %}
        {% if p == page %}
        <span class="current">{{ p }}</span>
        {% else %}
        <a href="{{ url_for(endpoint, page=p) }}">{{ p }}</a>
        {% endif %}
    {% endfor %}

    {% if page < total_pages %}
    <a href="{{ url_for(endpoint, page=page+1) }}">下一页 &raquo;</a>
    {% endif %}
</nav>
{% endmacro %}

{# 表格宏 #}
{% macro data_table(rows, columns, empty_message='暂无数据') %}
{% if rows %}
<table class="data-table">
    <thead>
        <tr>
        {% for col in columns %}
            <th>{{ col.label }}</th>
        {% endfor %}
        </tr>
    </thead>
    <tbody>
    {% for row in rows %}
        <tr>
        {% for col in columns %}
            <td>{{ row[col.key] }}</td>
        {% endfor %}
        </tr>
    {% endfor %}
    </tbody>
</table>
{% else %}
<p class="empty">{{ empty_message }}</p>
{% endif %}
{% endmacro %}
```

```html
{# 使用宏库 #}
{% from 'macros/cards.html' import card, user_card, pagination, data_table %}

{% call card(title="最新动态", class="news-card") %}
    <ul>
    {% for item in news_items %}
        <li>{{ item.title }}</li>
    {% endfor %}
    </ul>
{% endcall %}

{{ user_card(current_user, show_email=False) }}

{{ pagination(page=3, total_pages=10, endpoint='posts.list') }}

{% set cols = [
    {"key": "id", "label": "ID"},
    {"key": "name", "label": "姓名"},
    {"key": "score", "label": "分数"},
] %}
{{ data_table(students, cols) }}
```

---

## 第七部分：模板继承

### 7.1 实际场景

网站有统一的页面布局（头部导航、底部版权），但每个页面的内容区域不同。你不想在每个页面重复写导航和版权信息。

**问题：如何定义基础模板让其他页面继承？**

### 7.2 基础模板

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}我的网站{% endblock %}</title>
    <style>
        {% block styles %}{% endblock %}
    </style>
</head>
<body>
    <header>
        <nav>
            <a href="/">首页</a>
            <a href="/about">关于</a>
            {% block nav %}{% endblock %}
        </nav>
    </header>
    
    <main>
        {% block content %}
            <p>默认内容</p>
        {% endblock %}
    </main>
    
    <footer>
        {% block footer %}
            <p>&copy; 2024 我的网站</p>
        {% endblock %}
    </footer>
    
    <script>
        {% block scripts %}{% endblock %}
    </script>
</body>
</html>
```

### 7.3 子模板

```html
<!-- templates/home.html -->
{% extends "base.html" %}

{% block title %}首页{% endblock %}

{% block styles %}
    {{ super() }}
    <style>
        .hero { background: #f0f0f0; }
    </style>
{% endblock %}

{% block nav %}
    <a href="/home">首页</a>
{% endblock %}

{% block content %}
    <div class="hero">
        <h1>欢迎来到首页</h1>
    </div>
{% endblock %}

{% block footer %}
    {{ super() }}
    <p>首页专属 footer</p>
{% endblock %}
```

### 7.4 多级模板继承实战

```html
{# templates/base.html — 第一层：全局布局 #}
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}默认标题{% endblock %}</title>
    {% block head_meta %}{% endblock %}
    {% block head_styles %}
    <link rel="stylesheet" href="{{ url_for('static', filename='css/base.css') }}">
    {% endblock %}
</head>
<body>
    {% block body_header %}
    <header class="global-header">
        <nav>{% block nav %}{% endblock %}</nav>
    </header>
    {% endblock %}

    {% block body_content %}
    <main>{% block content %}{% endblock %}</main>
    {% endblock %}

    {% block body_footer %}
    <footer class="global-footer">{% block footer %}{% endblock %}</footer>
    {% endblock %}

    {% block body_scripts %}
    <script src="{{ url_for('static', filename='js/base.js') }}"></script>
    {% endblock %}
</body>
</html>
```

```html
{# templates/layouts/admin.html — 第二层：管理后台布局 #}
{% extends "base.html" %}

{% block title %}管理后台 - {{ self.page_title() if self.page_title is defined else '' }}{% endblock %}

{% block head_styles %}
{{ super() }}
<link rel="stylesheet" href="{{ url_for('static', filename='css/admin.css') }}">
{% endblock %}

{% block body_content %}
<div class="admin-layout">
    <aside class="admin-sidebar">
        {% block sidebar %}
        <ul class="nav">
            <li><a href="{{ url_for('admin.dashboard') }}">仪表盘</a></li>
            <li><a href="{{ url_for('admin.users') }}">用户管理</a></li>
            <li><a href="{{ url_for('admin.posts') }}">文章管理</a></li>
        </ul>
        {% endblock %}
    </aside>
    <div class="admin-main">
        {% block content %}{% endblock %}
    </div>
</div>
{% endblock %}
```

```html
{# templates/admin/users.html — 第三层：用户管理页面 #}
{% extends "layouts/admin.html" %}

{% block page_title %}用户管理{% endblock %}

{% block content %}
<div class="page-header">
    <h2>用户列表</h2>
    <a class="btn" href="{{ url_for('admin.create_user') }}">新增用户</a>
</div>

<table class="data-table">
    <thead>
        <tr><th>ID</th><th>用户名</th><th>邮箱</th><th>操作</th></tr>
    </thead>
    <tbody>
    {% for user in users %}
        <tr>
            <td>{{ user.id }}</td>
            <td>{{ user.username }}</td>
            <td>{{ user.email }}</td>
            <td>
                <a href="{{ url_for('admin.edit_user', id=user.id) }}">编辑</a>
                <a href="{{ url_for('admin.delete_user', id=user.id) }}">删除</a>
            </td>
        </tr>
    {% endfor %}
    </tbody>
</table>
{% endblock %}
```

### 7.5 模板继承中的 set 与 block 嵌套

```html
{# 在子模板中设置父模板使用的变量 #}
{% extends "base.html" %}

{% set page_class = "home-page" %}
{% set body_data = {"controller": "home", "action": "index"} %}

{% block body_content %}
<body class="{{ page_class }}" data-controller="{{ body_data.controller }}">
    {{ super() }}
</body>
{% endblock %}
```

---

## 第八部分：包含

### 8.1 实际场景

导航栏在多个页面都要显示，但不同页面的导航栏可能有些细微差异。

**问题：如何在一个模板中嵌入另一个模板？**

### 8.2 include 语句

```html
<!-- 包含导航 -->
{% include 'navigation.html' %}

<!-- 条件包含 -->
{% include 'admin_sidebar.html' if current_user.is_admin %}

<!-- 包含并传递变量 -->
{% include 'post_item.html' with context %}
```

### 8.3 动态包含

```html
<!-- 根据变量选择模板 -->
{% include template_name %}
```

### 8.4 include vs macro vs extends 高级场景

```html
{# include 适合：大块独立 UI 片段，基本不需要参数 #}
{% include 'shared/footer.html' %}

{# macro 适合：需要参数控制的重复 UI 组件 #}
{% from 'shared/forms.html' import input_field %}
{{ input_field('email', '邮箱', type='email') }}

{# extends 适合：整体页面布局替换 #}
{% extends "layouts/base.html" %}
```

---

## 第九部分：实战示例

### 9.1 博客布局

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}博客{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <header class="site-header">
        <h1><a href="/">{{ site_name }}</a></h1>
        <nav>
            {% for item in nav_items %}
            <a href="{{ item.url }}">{{ item.name }}</a>
            {% endfor %}
        </nav>
    </header>
    
    <main class="content">
        {% block content %}{% endblock %}
    </main>
    
    <footer class="site-footer">
        <p>&copy; {{ current_year }} {{ site_name }}</p>
    </footer>
</body>
</html>
```

```html
<!-- templates/index.html -->
{% extends "base.html" %}

{% block title %}首页 - {{ site_name }}{% endblock %}

{% block content %}
    <section class="posts">
        <h2>最新文章</h2>
        
        {% for post in posts %}
        <article class="post-card">
            <h3>
                <a href="{{ url_for('post', slug=post.slug) }}">
                    {{ post.title }}
                </a>
            </h3>
            
            <div class="meta">
                <span>作者: {{ post.author.username }}</span>
                <span>日期: {{ post.created_at|date }}</span>
                <span>浏览: {{ post.views }}</span>
            </div>
            
            <p class="excerpt">{{ post.summary|truncate(200) }}</p>
            
            <a href="{{ url_for('post', slug=post.slug) }}" class="read-more">
                阅读全文 →
            </a>
        </article>
        {% else %}
        <p>暂无文章</p>
        {% endfor %}
    </section>
    
    <aside class="sidebar">
        {% block sidebar %}
        <div class="widget">
            <h3>分类</h3>
            <ul>
                {% for category in categories %}
                <li>
                    <a href="{{ url_for('category', slug=category.slug) }}">
                        {{ category.name }}
                    </a>
                    <span class="count">({{ category.post_count }})</span>
                </li>
                {% endfor %}
            </ul>
        </div>
        {% endblock %}
    </aside>
{% endblock %}
```

### 9.2 场景化模板配置

```python
from flask import Flask, render_template

app = Flask(__name__)

# 设置全局变量 — 所有模板自动可用
@app.context_processor
def inject_globals():
    return {
        "site_name": "我的博客",
        "current_year": 2025,
        "nav_items": [
            {"name": "首页", "url": "/"},
            {"name": "文章", "url": "/posts"},
            {"name": "关于", "url": "/about"},
        ],
    }

# 设置全局函数
@app.context_processor
def inject_functions():
    return {
        "is_admin": lambda user: user.get("role") == "admin",
    }

# 另一种方式：直接设置 jinja_env
app.jinja_env.globals["APP_VERSION"] = "2.0.1"
```

---

### L2 实践层：用好

| 做法 | 原因 | 示例 |
|------|------|------|
| 使用模板继承代替复制 HTML | DRY 原则，统一布局 | `{% extends "base.html" %}` |
| 宏封装可复用片段 | 表单输入框、按钮等 | `{% macro input_field(...) %}` |
| 自动转义防 XSS | Jinja2 默认转义 HTML | 模板中 `{{ user_input }}` 自动安全 |
| 自定义过滤器组织业务逻辑 | 日期格式化、文本截断等复用 | `{{ created_at\|date_format }}` |
| `super()` 继承父块内容 | 块内追加而非覆盖 | `{% block styles %}{{ super() }}{% endblock %}` |

#### 反模式

```html
<!-- ❌ 错误：用户输入使用 |safe -->
<p>{{ user_comment | safe }}</p>  <!-- XSS 漏洞！ -->

<!-- ✅ 正确：自动转义 -->
<p>{{ user_comment }}</p>

<!-- ❌ 错误：每页重复头部/底部 -->
<!-- ✅ 正确：使用 extends + block 继承 -->
```

#### 何时使用宏 vs include vs extends

| 方式 | 适用场景 |
|------|---------|
| `{% extends %}` | 全页面布局继承（base.html → page.html） |
| `{% include %}` | 嵌入独立组件片段（导航栏、页脚） |
| `{% macro %}` | 带参数的可复用 UI 组件（表单项） |

---

## 第十部分：Jinja2 进阶技巧

### 10.1 转义与 XSS 防护深入

```python
from markupsafe import Markup, escape

# Markup 类型：标记为安全，跳过转义
safe_html = Markup("<strong>安全的内容</strong>")

# escape：手动转义
unsafe = escape("<script>alert('xss')</script>")
# 结果: &lt;script&gt;alert(&#39;xss&#39;)&lt;/script&gt;

# 在 Python 视图中注册
@app.template_filter("safe_html")
def safe_html_filter(text: str) -> Markup:
    """仅在完全信任输入时使用"""
    return Markup(text)
```

```html
{# 模板中转义与安全输出 #}

{# 自动转义（默认） — 安全 #}
{{ user_supplied_content }}

{# 显式转义 #}
{{ user_supplied_content|e }}

{# 标记安全（危险！仅在你信任数据时使用） #}
{{ trusted_html|safe }}

{# 条件安全：仅允许白名单 HTML 标签 #}
{{ user_content|striptags|truncate(200) }}
```

### 10.2 模板性能优化

```python
from flask import Flask

app = Flask(__name__)

# 生产环境配置
app.jinja_env.cache = {}  # 启用模板缓存
app.jinja_env.auto_reload = False  # 禁用自动重载

# 模板字节码缓存（文件系统）
from jinja2 import FileSystemBytecodeCache
app.jinja_env.bytecode_cache = FileSystemBytecodeCache("/tmp/jinja2_cache")

# 或内存缓存
from jinja2 import MemcachedBytecodeCache
import pylibmc
client = pylibmc.Client(["127.0.0.1"])
app.jinja_env.bytecode_cache = MemcachedBytecodeCache(client)
```

```html
{# 模板优化技巧 #}

{# 1. 使用 {% cache %} 缓存片段（需要 Flask-Caching） #}
{% cache 300, 'sidebar' %}
    {# 复杂的侧边栏渲染 #}
{% endcache %}

{# 2. 避免在模板中做复杂计算 #}
{# ❌ 不好 #}
{% set avg = (items|sum / items|length)|round(2) %}

{# ✅ 在视图中计算好再传入 #}
{{ average_score }}  {# 视图函数中已计算 #}

{# 3. 减少嵌套循环的层级 #}
{# ❌ 3 层嵌套 #}
{% for category in categories %}
    {% for sub in category.sub_categories %}
        {% for item in sub.items %}
            {{ item.name }}
        {% endfor %}
    {% endfor %}
{% endfor %}

{# ✅ 在 Python 中扁平化数据 #}
{% for item in flat_items %}
    {{ item.name }}
{% endfor %}
```

### 10.3 Jinja2 模板测试

```python
from jinja2 import Environment, DictLoader

def test_template_rendering():
    """单元测试模板渲染结果"""
    env = Environment(loader=DictLoader({
        "test.html": """
            <h1>{{ title }}</h1>
            {% if items %}
            <ul>
            {% for item in items %}
                <li>{{ item }}</li>
            {% endfor %}
            </ul>
            {% endif %}
        """
    }))

    # 测试正常渲染
    template = env.get_template("test.html")
    output = template.render(title="Hello", items=["a", "b", "c"])

    assert "<h1>Hello</h1>" in output
    assert "<li>a</li>" in output
    assert "<li>b</li>" in output

    # 测试空列表
    output2 = template.render(title="Empty", items=[])
    assert "<ul>" not in output2

    # 测试 XSS 防护
    unsafe_env = Environment()
    tmpl = unsafe_env.from_string("{{ user_input }}")
    output3 = tmpl.render(user_input="<script>alert(1)</script>")
    assert "&lt;script&gt;" in output3
    assert "<script>" not in output3
```

### 10.4 常见错误与排查

| 错误现象 | 原因分析 | 解决方案 | 预防措施 |
|----------|---------|---------|---------|
| `TemplateNotFound: xxx.html` | 模板文件不在 `templates/` 目录，或路径拼写错误 | 检查文件路径和 Flask 实例化时的 `template_folder` | 使用绝对路径或统一约定模板目录 |
| `UndefinedError: 'xxx' is undefined` | 模板中引用了不存在的变量 | ① `{{ var\|default('') }}` ② 视图函数补充变量 | 始终为模板变量提供默认值 |
| 模板修改后不生效 | 缓存了编译后的模板 | 开发时 `app.jinja_env.auto_reload = True` | 生产环境禁用 auto_reload |

---

### L3 专家层：深入

## 第九部分：L3 专家层 — 底层原理

### 9.2 模板编译过程（AST → Python 代码）

Jinja2 模板在首次使用时被编译为 Python 字节码，后续请求直接执行编译后的代码。

```
┌─────────────────────────────────────────────────────────────────┐
│                  模板编译管线                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   原始模板 (template.html)                                       │
│       │                                                         │
│       ▼                                                         │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │ 1. Lexer (词法分析器)                                     │   │
│   │    输入: 模板源代码字符串                                  │   │
│   │    输出: Token 流 [Text, VariableStart, Name, ...]       │   │
│   │                                                          │   │
│   │    <h1>{{ user.name }}</h1>                              │   │
│   │    → TEXT('<h1>') VAR_START NAME('user') DOT NAME('name') │   │
│   └─────────────────────────────────────────────────────────┘   │
│       │                                                         │
│       ▼                                                         │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │ 2. Parser (语法分析器)                                    │   │
│   │    输入: Token 流                                         │   │
│   │    输出: AST (抽象语法树)                                  │   │
│   │                                                          │   │
│   │    Template                                              │   │
│   │    ├── nodes.Output                                      │   │
│   │    │   └── nodes.Getattr                                 │   │
│   │    │       ├── nodes.Name('user')                        │   │
│   │    │       └── 'name'                                    │   │
│   │    └── ...                                                │   │
│   └─────────────────────────────────────────────────────────┘   │
│       │                                                         │
│       ▼                                                         │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │ 3. Code Generator (代码生成器)                            │   │
│   │    输入: AST                                              │   │
│   │    输出: Python 源代码字符串                               │   │
│   │                                                          │   │
│   │    def root(context):                                    │   │
│   │        l_user = resolve(context, 'user')                 │   │
│   │        yield '<h1>'                                      │   │
│   │        yield escape(environment.getattr(l_user, 'name')) │   │
│   │        yield '</h1>'                                     │   │
│   └─────────────────────────────────────────────────────────┘   │
│       │                                                         │
│       ▼                                                         │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │ 4. Bytecode Compiler (字节码编译)                        │   │
│   │    输入: Python 源代码                                    │   │
│   │    输出: code object → 缓存到 TemplateModule              │   │
│   │                                                          │   │
│   │    compile(source, filename='<template>', 'exec')        │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

```python
# 查看模板编译后的 Python 代码
from jinja2 import Environment, FileSystemLoader

env: Environment = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("hello.html")

# 获取编译后的源码
source: str = env.compile_source(env.get_source("hello.html")[0])
print(source)
# 输出类似：
# from jinja2.runtime import LoopContext, Macro, Markup, TemplateRuntimeError
# def root(context, environment=environment):
#     yield '<h1>Hello, '
#     yield str(environment.getattr(resolve(context, 'user'), 'name'))
#     yield '</h1>'
```

### 9.3 沙盒机制

Jinja2 提供 SandboxedEnvironment 用于安全渲染不可信模板。

```
┌─────────────────────────────────────────────────────────────────┐
│                    沙盒环境安全控制                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   普通 Environment vs SandboxedEnvironment：                     │
│                                                                 │
│   ┌──────────────────────┬──────────────────────────────┐        │
│   │ 普通 Environment     │ SandboxedEnvironment         │        │
│   ├──────────────────────┼──────────────────────────────┤        │
│   │ 可调用任意 Python 函数│ 仅允许标记为 @unsafe 的属性  │        │
│   │ 可访问 __class__     │ 拦截 __class__/__mro__ 访问  │        │
│   │ 可执行 os.system()   │ 拦截危险方法调用              │        │
│   │ 无属性访问限制        │ is_safe_attribute() 检查     │        │
│   └──────────────────────┴──────────────────────────────┘        │
│                                                                 │
│   沙盒拦截点：                                                    │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │ • getattr: 拦截访问以下划线开头的属性                     │   │
│   │ • call: 拦截调用未标记为 safe 的可调用对象                │   │
│   │ • getitem: 拦截对非映射/序列类型的索引访问                │   │
│   │ • iter: 拦截对不可迭代对象的遍历                          │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│   典型攻击向量拦截：                                              │
│   {{ ''.__class__.__mro__[1].__subclasses__() }}                │
│   → SecurityError: access to attribute '__class__' is unsafe    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

```python
from jinja2 import SandboxedEnvironment

env = SandboxedEnvironment()

# 安全：普通属性访问
tmpl = env.from_string("Hello {{ user.name }}")
print(tmpl.render(user={"name": "Alice"}))  # Hello Alice

# 拦截：危险属性访问
tmpl = env.from_string("{{ data.__class__ }}")
try:
    tmpl.render(data="test")
except Exception as e:
    print(f"拦截: {e}")  # SecurityError

# 自定义安全检查
class MySandboxedEnv(SandboxedEnvironment):
    def is_safe_attribute(self, obj: object, attr: str, value: object) -> bool:
        # 禁止访问所有以 'secret' 开头的属性
        if attr.startswith("secret"):
            return False
        return super().is_safe_attribute(obj, attr, value)
```

### 9.4 模板继承的 MRO 查找规则

Jinja2 的模板继承机制类似 Python 类的 MRO（Method Resolution Order），使用 `super()` 调用父模板的 block。

```
┌─────────────────────────────────────────────────────────────────┐
│                  模板继承链与 block 解析                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   继承层次：                                                     │
│                                                                 │
│   base.html                                                     │
│   ├── block title: "默认标题"                                    │
│   ├── block styles: ""                                          │
│   ├── block content: "<p>默认内容</p>"                           │
│   └── block footer: "© 2024"                                    │
│       │                                                         │
│       ▲ extends                                                 │
│       │                                                         │
│   page.html                                                     │
│   ├── block title: "页面标题"                                    │
│   ├── block styles: {{ super() }} + 额外 CSS                    │
│   ├── block content: "<h1>页面内容</h1>"                         │
│   └── block footer: {{ super() }} + "额外信息"                   │
│       │                                                         │
│       ▲ extends                                                 │
│       │                                                         │
│   home.html                                                     │
│   ├── block content: {{ super() }} + "<p>首页特有</p>"           │
│   └── block title: "首页"                                       │
│                                                                 │
│   渲染 home.html 时的 block 解析：                                │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │ block title:    home → page → base                      │   │
│   │                 "首页" (home 覆盖)                       │   │
│   │                                                         │   │
│   │ block styles:   home → page → base                      │   │
│   │                 page 有 {{ super() }} + 额外 CSS          │   │
│   │                 → base 的 styles + page 的额外 CSS       │   │
│   │                                                         │   │
│   │ block content:  home → page → base                      │   │
│   │                 home 有 {{ super() }}                    │   │
│   │                 → page 的 content + home 的首页特有       │   │
│   │                                                         │   │
│   │ block footer:   home → page → base                      │   │
│   │                 page 有 {{ super() }} + "额外信息"       │   │
│   │                 → base 的 footer + page 的额外信息       │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│   内部实现：blocks 字典存储继承链上所有同名 block，               │
│   render 时从最派生类开始执行，遇到 super() 时调用父级版本。       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 9.5 性能考量

| 操作 | 耗时 | 内存 | 说明 |
|------|------|------|------|
| 模板首次编译 | ~5ms | ~50KB | Lexer → Parser → CodeGen → compile |
| 缓存命中渲染 | ~0.3ms | ~10KB | 直接执行编译后的 bytecode |
| 缓存未命中渲染 | ~5.3ms | ~60KB | 编译 + 渲染 |
| 模板继承（3 层） | ~0.5ms | ~15KB | block 链式调用开销 |
| 宏调用 | ~0.02ms | ~1KB | 函数调用级别开销 |
| 过滤器链（5 个） | ~0.1ms | — | 每个过滤器额外函数调用 |

**扩展性：** Jinja2 模板缓存默认启用（`cache_size=400`）。生产环境应设置 `cache=SimpleCache(400)` 或 `cache=FileSystemCache()`。模板数量超过 400 时，LRU 淘汰最久未使用的模板。

### 9.6 Jinja2 vs Mako vs Django Templates

| 维度 | Jinja2 | Mako | Django Templates |
|------|--------|------|------------------|
| 语法风格 | `{{ var }}` / `{% tag %}` | `${var}` / `<% %>` | `{{ var }}` / `{% tag %}` |
| 性能 | 快（编译为 Python） | 最快（直接生成 Python） | 较慢（解析式） |
| 内嵌 Python | 不支持（需沙盒） | 支持 `<% %>` | 不支持 |
| 模板继承 | `extends` + `block` | `inherits` + `block` | `extends` + `block` |
| 自动转义 | 默认开启 | 需手动开启 | 默认开启 |
| 适用场景 | 通用 Web、安全要求高 | 高性能、需嵌入式 Python | Django 项目标配 |

### 9.7 设计动机

| 设计决策 | 动机 | 权衡 |
|----------|------|------|
| 编译为 Python 代码后执行 | 利用 Python 虚拟机优化，性能接近原生代码 | 编译开销，首次渲染较慢 |
| 自动 HTML 转义（autoescape） | 防止 XSS 攻击，安全默认值 | 对不需要转义的内容需用 `|safe` |
| 沙盒环境独立于主环境 | 安全渲染不可信模板（用户自定义模板） | 功能受限，部分过滤器不可用 |
| block 而非占位符的继承机制 | 支持多层继承和 `super()` 组合 | 继承链过深时调试困难 |
| 宏作为模板函数 | 代码复用，参数化组件 | 宏内无法访问调用者上下文（需 `with context`） |

### 9.8 知识关联

```
              模板文件 (.html)
                    │
                    ▼
          ┌─────────────────┐
          │    Lexer        │ ← 词法分析
          │  (Token 流)     │
          └────────┬────────┘
                   │
                   ▼
          ┌─────────────────┐
          │    Parser       │ ← 语法分析
          │  (AST 树)       │
          └────────┬────────┘
                   │
            ┌──────┴──────┐
            ▼             ▼
    ┌──────────────┐ ┌──────────────┐
    │  Code Gen    │ │  Inheritance │
    │  (Python 码) │ │  (MRO 链)    │
    └──────┬───────┘ └──────┬───────┘
           │                │
           ▼                │
    ┌──────────────┐        │
    │  Bytecode    │        │
    │  (缓存)      │◄───────┘
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │  Renderer    │ ← 上下文数据 + 编译模板 → HTML
    └──────────────┘
```

---

## 总结

| 知识点 | 说明 |
|---------|------|
| 变量 | `{{ variable }}` |
| 条件 | `{% if %}` |
| 循环 | `{% for %}` |
| 过滤器 | `\| filter` |
| 宏 | `{% macro %}` |
| 继承 | `{% extends %}` |
| 包含 | `{% include %}` |
| 块 | `{% block %}` |
| 自定义过滤器 | `@app.template_filter()` |
| 自定义测试器 | `@app.template_test()` |
| 沙盒环境 | `SandboxedEnvironment` 安全渲染 |
| 转义 | 默认 autoescape 防 XSS |
| 性能优化 | 字节码缓存、减少嵌套、视图中计算 |
