# 模板引擎 Jinja2

## 模板渲染

Jinja2 是 Flask 内置的模板引擎，允许在 HTML 中嵌入 Python 表达式，实现动态页面渲染。

**目录结构：**

```
my-app/
├── app.py
└── templates/          # 模板文件夹（固定名称）
    ├── base.html       # 基础模板
    ├── index.html      # 首页模板
    └── user.html       # 用户模板
```

**基本用法：**

```python
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    # 渲染模板，传递变量
    return render_template('index.html', title='首页', user='张三')
```

**templates/index.html：**

```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
</head>
<body>
    <h1>欢迎，{{ user }}！</h1>
</body>
</html>
```

**render_template() 参数：**

```python
# 传递多个变量
render_template(
    'index.html',
    title='首页',
    user='张三',
    age=25,
    items=[1, 2, 3]
)

# 使用字典解包
context = {'title': '首页', 'user': '张三'}
render_template('index.html', **context)
```

---

## 变量与表达式

Jinja2 使用 `{{ }}` 语法输出变量，支持表达式和过滤器。

**变量输出：**

```html
<!-- 基础变量 -->
<h1>{{ username }}</h1>

<!-- 对象属性 -->
<p>{{ user.name }}</p>
<p>{{ user.email }}</p>

<!-- 字典访问 -->
<p>{{ config['SITE_NAME'] }}</p>
<p>{{ data.key }}</p>

<!-- 列表索引 -->
<p>{{ items.0 }}</p>
<p>{{ users.0.name }}</p>
```

**表达式运算：**

```html
<!-- 算术运算 -->
<p>{{ price * quantity }}</p>
<p>{{ (price - discount) | round(2) }}</p>

<!-- 逻辑运算 -->
{% if user and user.is_active %}
    <p>活跃用户</p>
{% endif %}

<!-- 比较运算 -->
{% if score >= 60 %}
    <p>及格</p>
{% else %}
    <p>不及格</p>
{% endif %}
```

**过滤器（Filters）：**

```html
<!-- 字符串处理 -->
<p>{{ name | upper }}</p>           <!-- 大写 -->
<p>{{ name | lower }}</p>           <!-- 小写 -->
<p>{{ name | title }}</p>           <!-- 首字母大写 -->
<p>{{ name | capitalize }}</p>      <!-- 句首大写 -->

<!-- 默认值 -->
<p>{{ nickname | default('匿名用户') }}</p>
<p>{{ nickname | default('匿名用户', true) }}</p>  <!-- 空字符串也使用默认值 -->

<!-- 列表处理 -->
<p>{{ items | first }}</p>          <!-- 第一个元素 -->
<p>{{ items | last }}</p>           <!-- 最后一个元素 -->
<p>{{ items | length }}</p>         <!-- 长度 -->
<p>{{ items | join(', ') }}</p>     <!-- 连接字符串 -->

<!-- 其他 -->
<p>{{ content | truncate(100) }}</p>  <!-- 截断 -->
<p>{{ html | safe }}</p>              <!-- 不转义 HTML -->
<p>{{ text | escape }}</p>            <!-- HTML 转义 -->
```

**自定义过滤器：**

```python
# app.py
@app.template_filter('reverse')
def reverse_filter(s):
    return s[::-1]


# 使用
<p>{{ name | reverse }}</p>  <!-- 输出反向字符串 -->
```

---

## 控制结构

Jinja2 支持 `{% %}` 语法用于控制结构，如条件判断和循环。

**条件判断：**

```html
<!-- if / elif / else -->
{% if user.role == 'admin' %}
    <a href="/admin">管理后台</a>
{% elif user.role == 'editor' %}
    <a href="/editor">编辑后台</a>
{% else %}
    <a href="/user">用户中心</a>
{% endif %}

<!-- 逻辑运算 -->
{% if user and user.is_active %}
    <p>活跃用户</p>
{% endif %}

<!-- 比较运算 -->
{% if score >= 90 %}
    <p>优秀</p>
{% elif score >= 60 %}
    <p>及格</p>
{% else %}
    <p>不及格</p>
{% endif %}
```

**循环：**

```html
<!-- 遍历列表 -->
<ul>
{% for item in items %}
    <li>{{ item }}</li>
{% endfor %}
</ul>

<!-- 遍历对象列表 -->
<ul>
{% for user in users %}
    <li>
        <span class="loop-index">{{ loop.index }}</span>  <!-- 从 1 开始 -->
        <span class="loop-index0">{{ loop.index0 }}</span> <!-- 从 0 开始 -->
        <span>{{ user.name }}</span>
        {% if loop.first %}<span class="first">首个</span>{% endif %}
        {% if loop.last %}<span class="last">末尾</span>{% endif %}
    </li>
{% else %}
    <li>暂无数据</li>  <!-- 列表为空时执行 -->
{% endfor %}
</ul>

<!-- 嵌套循环 -->
{% for category in categories %}
    <h3>{{ category.name }}</h3>
    <ul>
    {% for article in category.articles %}
        <li>{{ article.title }}</li>
    {% endfor %}
    </ul>
{% endfor %}
```

---

## 模板继承

模板继承允许创建基础模板，子模板继承并覆盖特定部分，避免代码重复。

**基础模板 base.html：**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}默认标题{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <header>
        <nav>
            <a href="{{ url_for('index') }}">首页</a>
            <a href="{{ url_for('about') }}">关于</a>
            <a href="{{ url_for('contact') }}">联系</a>
        </nav>
    </header>

    <main>
        {% block content %}{% endblock %}
    </main>

    <footer>
        <p>&copy; 2027 我的网站</p>
    </footer>

    {% block extra_js %}{% endblock %}
</body>
</html>
```

**子模板 index.html：**

```html
{% extends "base.html" %}

{% block title %}首页 - {{ super() }}{% endblock %}

{% block content %}
<h1>欢迎来到首页</h1>
<p>这里是首页内容...</p>

{% for article in articles %}
    <article>
        <h2>{{ article.title }}</h2>
        <p>{{ article.summary }}</p>
    </article>
{% endfor %}
{% endblock %}

{% block extra_js %}
<script src="{{ url_for('static', filename='js/index.js') }}"></script>
{% endblock %}
```

**关键点：**
- `{% extends "base.html" %}` 必须在模板第一行
- `{% block name %}{% endblock %}` 定义可覆盖的区域
- `{{ super() }}` 调用父模板的内容

---

## 宏（Macro）

宏类似于函数，可以重复使用，用于封装常用的 HTML 片段。

**定义宏：**

```html
<!-- macros/form.html -->
{% macro input_field(name, type='text', label='', placeholder='') %}
<div class="form-group">
    {% if label %}
    <label for="{{ name }}">{{ label }}</label>
    {% endif %}
    <input type="{{ type }}" name="{{ name }}" id="{{ name }}" placeholder="{{ placeholder }}">
</div>
{% endmacro %}


{% macro button(text, type='submit', class='') %}
<button type="{{ type }}" class="{{ class }}">{{ text }}</button>
{% endmacro %}
```

**使用宏：**

```html
<!-- 方式 1：在同一文件中定义并使用 -->
{% from 'macros/form.html' import input_field, button %}

<form>
    {{ input_field('username', label='用户名', placeholder='请输入用户名') }}
    {{ input_field('password', type='password', label='密码') }}
    {{ button('登录', class='btn-primary') }}
</form>


<!-- 方式 2：导入整个宏文件 -->
{% import 'macros/form.html' as form %}

<form>
    {{ form.input_field('email', type='email', label='邮箱') }}
    {{ form.button('提交') }}
</form>
```