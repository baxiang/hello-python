# Flask 模板引擎 Jinja2

深入学习 Jinja2 模板引擎，掌握模板语法、继承、过滤器和宏。

---

## 1. Jinja2 简介

### 1.1 什么是 Jinja2？

Jinja2 是 Flask 默认的模板引擎，是一个现代且设计师友好的 Python 模板语言。

### 1.2 配置 Jinja2

```python
from flask import Flask

app = Flask(__name__)

# Jinja2 配置
app.jinja_env.auto_reload = True  # 自动重载模板
app.jinja_env.cache = None  # 模板缓存

# 自定义配置
app.jinja_env.globals.update({
    'site_name': 'My Site',
    'current_year': 2024
})

# 添加自定义过滤器
def datetime_format(value, format='%Y-%m-%d'):
    if value:
        return value.strftime(format)
    return ''

app.jinja_env.filters['datetime'] = datetime_format
```

---

## 2. 模板基础语法

### 2.1 变量输出

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

### 2.2 注释

```html
{# 这是注释，不会被输出 #}

{# 
    多行注释
    可以包含多行内容
#}
```

---

## 3. 条件判断

### 3.1 if 语句

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

### 3.2 比较运算符

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

### 3.3 逻辑运算符

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

## 4. 循环

### 4.1 for 循环

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

### 4.2 循环变量

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

### 4.3 循环过滤

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

## 5. 过滤器

### 5.1 内置过滤器

```html
<!-- 字符串过滤器 -->
<p>{{ name|upper }}</p>           <!-- 大写 -->
<p>{{ name|lower }}</p>           <!-- 小写 -->
<p>{{ name|capitalize }}</p>     <!-- 首字母大写 -->
<p>{{ title|trim }}</p>           <!-- 去除空格 -->
<p>{{ text|truncate(50) }}</p>   <!-- 截断 -->

<!-- 数字过滤器 -->
<p>{{ price|round(2) }}</p>      <!-- 四舍五入 -->
<p>{{ number|format('d') }}</p>  <!-- 格式化 -->

<!-- 列表过滤器 -->
<p>{{ items|length }}</p>        <!-- 长度 -->
<p>{{ items|first }}</p>         <!-- 第一个 -->
<p>{{ items|last }}</p>          <!-- 最后一个 -->
<p>{{ items|sort }}</p>          <!-- 排序 -->
<p>{{ items|unique }}</p>        <!-- 去重 -->

<!-- 布尔过滤器 -->
<p>{{ value|default('N/A') }}</p>  <!-- 默认值 -->
<p>{{ value|boolean }}</p>           <!-- 转为布尔值 -->
```

### 5.2 自定义过滤器

```python
from flask import Flask

app = Flask(__name__)

# 方法一：注册过滤器
@app.template_filter('reverse')
def reverse_filter(s):
    return s[::-1]

# 方法二：添加到全局
def markdown_to_html(text):
    import markdown
    return markdown.markdown(text)

app.jinja_env.globals['markdown'] = markdown_to_html
```

```html
<!-- 使用自定义过滤器 -->
<p>{{ name|reverse }}</p>
<p>{{ content|markdown }}</p>
```

### 5.3 测试器

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

---

## 6. 宏

### 6.1 定义宏

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

### 6.2 使用宏

```html
<!-- 使用宏 -->
{{ input_field('username', '用户名') }}
{{ input_field('email', '邮箱', 'email') }}
{{ input_field('password', '密码', 'password') }}
{{ button('提交', 'submit', 'submitForm()') }}
```

### 6.3 宏的导入

```html
<!-- 导入宏文件 -->
{% from 'forms.html' import input_field, button %}

<!-- 导入并重命名 -->
{% from 'forms.html' import input_field as input %}

<!-- 导入所有 -->
{% from 'forms.html' import * %}
```

---

## 7. 模板继承

### 7.1 基础模板

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

### 7.2 子模板

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

---

## 8. 包含

### 8.1 include 语句

```html
<!-- 包含导航 -->
{% include 'navigation.html' %}

<!-- 条件包含 -->
{% include 'admin_sidebar.html' if current_user.is_admin %}

<!-- 包含并传递变量 -->
{% include 'post_item.html' with context %}
```

### 8.2 动态包含

```html
<!-- 根据变量选择模板 -->
{% include template_name %}
```

---

## 9. 模板继承进阶

### 9.1 块嵌套

```html
<!-- base.html -->
{% block content %}
    <div class="container">
        {% block main %}{% endblock %}
    </div>
{% endblock %}

<!-- page.html -->
{% extends "base.html" %}

{% block main %}
    <div class="main-content">
        {% block page_content %}{% endblock %}
    </div>
{% endblock %}

<!-- post.html -->
{% extends "page.html" %}

{% block page_content %}
    <article>{{ post.content }}</article>
{% endblock %}
```

### 9.2 super() 调用

```html
<!-- 在子模板中调用父模板的内容 -->
{% block content %}
    <div class="old-content">
        {{ super() }}
    </div>
    <div class="new-content">
        新的额外内容
    </div>
{% endblock %}
```

---

## 10. 实战示例

### 10.1 博客布局

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

---

[← 上一章](./Flask/01-Flask路由详解.md) | [下一章](./Flask/03-Flask数据库集成.md)