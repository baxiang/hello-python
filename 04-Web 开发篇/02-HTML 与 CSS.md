# 第 2 章：HTML 与 CSS

掌握网页结构搭建和样式设计。

---

## 本章目标

- 掌握 HTML 常用标签
- 理解 CSS 选择器和样式
- 学会使用 Flexbox 和 Grid 布局
- 能够创建响应式网页

---

## 2.1 HTML 基础

### 什么是 HTML？

HTML（HyperText Markup Language）是用于创建网页的标记语言。

### HTML 文档结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>网页标题</title>
    <meta name="description" content="网页描述">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>网站标题</h1>
        <nav>
            <a href="/">首页</a>
            <a href="/about">关于</a>
        </nav>
    </header>

    <main>
        <article>
            <h2>文章标题</h2>
            <p>文章内容...</p>
        </article>

        <aside>
            <h3>侧边栏</h3>
        </aside>
    </main>

    <footer>
        <p>&copy; 2024 公司名称</p>
    </footer>

    <script src="app.js"></script>
</body>
</html>
```

---

## 2.2 常用 HTML 标签

### 文本标签

```html
<!-- 标题 -->
<h1>一级标题</h1>
<h2>二级标题</h2>
<h3>三级标题</h3>

<!-- 段落 -->
<p>这是一个段落。</p>

<!-- 强调 -->
<strong>加粗（强调）</strong>
<em>斜体（强调）</em>
<mark>高亮</mark>

<!-- 换行和水平线 -->
<br>
<hr>

<!-- 预格式化文本 -->
<pre>
    保持    空格
    和    换行
</pre>
```

### 链接和图片

```html
<!-- 链接 -->
<a href="https://example.com" target="_blank" title="提示文字">
    访问网站
</a>

<!-- 图片 -->
<img src="image.jpg" 
     alt="图片描述" 
     width="800" 
     height="600"
     loading="lazy">

<!-- 图片和链接组合 -->
<a href="https://example.com">
    <img src="logo.png" alt="Logo">
</a>
```

### 列表

```html
<!-- 无序列表 -->
<ul>
    <li>项目 1</li>
    <li>项目 2</li>
</ul>

<!-- 有序列表 -->
<ol>
    <li>第一步</li>
    <li>第二步</li>
</ol>

<!-- 定义列表 -->
<dl>
    <dt>术语</dt>
    <dd>定义说明</dd>
</dl>
```

### 表格

```html
<table border="1">
    <thead>
        <tr>
            <th>表头1</th>
            <th>表头2</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>单元格1</td>
            <td>单元格2</td>
        </tr>
    </tbody>
    <tfoot>
        <tr>
            <td colspan="2">脚注</td>
        </tr>
    </tfoot>
</table>
```

### 表单

```html
<form action="/submit" method="POST">
    <!-- 文本输入 -->
    <label for="username">用户名：</label>
    <input type="text" 
           id="username" 
           name="username" 
           required 
           placeholder="请输入用户名">

    <!-- 密码输入 -->
    <label for="password">密码：</label>
    <input type="password" 
           id="password" 
           name="password" 
           required>

    <!-- 邮箱输入 -->
    <input type="email" name="email" required>

    <!-- 数字输入 -->
    <input type="number" name="age" min="1" max="100">

    <!-- 日期输入 -->
    <input type="date" name="birthday">

    <!-- 单选按钮 -->
    <input type="radio" name="gender" value="male"> 男
    <input type="radio" name="gender" value="female"> 女

    <!-- 复选框 -->
    <input type="checkbox" name="hobby" value="reading"> 阅读
    <input type="checkbox" name="hobby" value="sports"> 运动

    <!-- 下拉选择 -->
    <select name="country">
        <option value="">请选择</option>
        <option value="cn">中国</option>
        <option value="us">美国</option>
    </select>

    <!-- 文本域 -->
    <textarea name="message" rows="4" cols="50"></textarea>

    <!-- 提交按钮 -->
    <button type="submit">提交</button>
    <button type="reset">重置</button>
</form>
```

### 语义化标签

```html
<!-- 页面头部 -->
<header>
    <nav>导航内容</nav>
</header>

<!-- 主要内容 -->
<main>
    <article>
        <section>文章章节</section>
    </article>
    <aside>侧边栏</aside>
</main>

<!-- 页面底部 -->
<footer>
    <address>联系信息</address>
</footer>

<!-- 通用容器 -->
<div>块级容器</div>
<span>行内容器</span>
```

---

## 2.3 CSS 基础

### CSS 引入方式

```html
<!-- 外部样式表 -->
<link rel="stylesheet" href="style.css">

<!-- 内部样式表 -->
<style>
    body { margin: 0; }
</style>

<!-- 内联样式 -->
<p style="color: red;">红色文字</p>
```

### CSS 选择器

```css
/* 元素选择器 */
p { color: blue; }

/* 类选择器 */
.highlight { background: yellow; }

/* ID 选择器 */
#header { height: 60px; }

/* 属性选择器 */
input[type="text"] { border: 1px solid gray; }

/* 后代选择器 */
nav a { text-decoration: none; }

/* 子选择器 */
ul > li { list-style: none; }

/* 相邻兄弟选择器 */
h1 + p { font-size: 1.2em; }

/* 伪类 */
a:hover { color: red; }
li:first-child { font-weight: bold; }

/* 伪元素 */
p::before { content: ">> "; }
p::first-line { color: gray; }
```

### CSS 常用属性

```css
/* 文本样式 */
p {
    color: #333;              /* 文字颜色 */
    font-size: 16px;         /* 字体大小 */
    font-family: Arial, sans-serif;  /* 字体 */
    font-weight: bold;       /* 字体粗细 */
    line-height: 1.6;         /* 行高 */
    text-align: center;       /* 文本对齐 */
    text-decoration: underline; /* 文本装饰 */
}

/* 背景 */
div {
    background-color: #f0f0f0;
    background-image: url('bg.jpg');
    background-repeat: no-repeat;
    background-position: center;
    background-size: cover;
}

/* 边框 */
.box {
    border: 1px solid #ccc;
    border-radius: 8px;
    border-width: 2px;
    border-style: solid;
    border-color: #999;
}

/* 尺寸 */
.box {
    width: 100px;
    height: 100px;
    max-width: 100%;
    min-height: 50px;
}
```

---

## 2.4 CSS 布局

### Flexbox 布局

```css
/* 容器 */
.container {
    display: flex;
    flex-direction: row;          /* 主轴方向 */
    justify-content: space-between; /* 主轴对齐 */
    align-items: center;           /* 交叉轴对齐 */
    flex-wrap: wrap;               /* 换行 */
    gap: 20px;                     /* 间距 */
}

/* 项目 */
.item {
    flex: 1;                       /* 占比 */
    flex-basis: 200px;            /* 基础宽度 */
    order: 1;                     /* 排序 */
}

/* 居中 */
.center {
    display: flex;
    justify-content: center;
    align-items: center;
}
```

### Grid 布局

```css
/* 网格容器 */
.grid-container {
    display: grid;
    grid-template-columns: repeat(3, 1fr);  /* 3列 */
    grid-template-rows: auto;                /* 自动行高 */
    gap: 20px;                               /* 间距 */
    grid-template-areas: 
        "header header header"
        "sidebar main main"
        "footer footer footer";
}

/* 网格项目 */
.header { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main { grid-area: main; }
.footer { grid-area: footer; }

/* 响应式网格 */
@media (max-width: 768px) {
    .grid-container {
        grid-template-columns: 1fr;
    }
}
```

---

## 2.5 响应式设计

### 视口设置

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

### 媒体查询

```css
/* 移动优先 */

/* 小屏幕 */
body {
    font-size: 14px;
}

/* 中等屏幕 */
@media (min-width: 768px) {
    body {
        font-size: 16px;
    }
}

/* 大屏幕 */
@media (min-width: 1024px) {
    body {
        font-size: 18px;
    }
}

/* 横屏 */
@media (orientation: landscape) {
    .sidebar {
        display: none;
    }
}
```

### 常见断点

```css
/* 手机 */
@media (max-width: 576px) { }

/* 平板 */
@media (min-width: 577px) and (max-width: 992px) { }

/* 桌面 */
@media (min-width: 993px) { }
```

---

## 2.6 实战：创建个人简历页面

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>个人简历 - 张三</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }

        .container {
            max-width: 800px;
            margin: 40px auto;
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }

        header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }

        header .title {
            font-size: 1.2em;
            opacity: 0.9;
        }

        .content {
            padding: 30px;
        }

        section {
            margin-bottom: 30px;
        }

        h2 {
            color: #667eea;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }

        .info-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
        }

        .info-item {
            display: flex;
            align-items: center;
        }

        .info-item strong {
            width: 80px;
            color: #666;
        }

        ul {
            list-style: none;
        }

        li {
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }

        li:last-child {
            border-bottom: none;
        }

        .skill-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }

        .tag {
            background: #e8f4ff;
            color: #667eea;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
        }

        @media (max-width: 600px) {
            .info-grid {
                grid-template-columns: 1fr;
            }
            
            .container {
                margin: 0;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>张三</h1>
            <div class="title">全栈开发工程师</div>
        </header>
        
        <div class="content">
            <section>
                <h2>基本信息</h2>
                <div class="info-grid">
                    <div class="info-item">
                        <strong>邮箱：</strong>
                        zhangsan@email.com
                    </div>
                    <div class="info-item">
                        <strong>电话：</strong>
                        13800138000
                    </div>
                    <div class="info-item">
                        <strong>年龄：</strong>
                        28 岁
                    </div>
                    <div class="info-item">
                        <strong>城市：</strong>
                        北京
                    </div>
                </div>
            </section>

            <section>
                <h2>技术技能</h2>
                <div class="skill-tags">
                    <span class="tag">Python</span>
                    <span class="tag">JavaScript</span>
                    <span class="tag">React</span>
                    <span class="tag">Flask</span>
                    <span class="tag">MySQL</span>
                    <span class="tag">Redis</span>
                    <span class="tag">Docker</span>
                </div>
            </section>

            <section>
                <h2>工作经历</h2>
                <ul>
                    <li>
                        <strong>高级开发工程师</strong> - 某某科技公司<br>
                        2021.03 - 至今<br>
                        负责公司核心产品后端开发
                    </li>
                    <li>
                        <strong>开发工程师</strong> - 某某网络公司<br>
                        2018.06 - 2021.02<br>
                        参与多个 Web 项目开发
                    </li>
                </ul>
            </section>

            <section>
                <h2>项目经验</h2>
                <ul>
                    <li>
                        <strong>电商平台后端</strong><br>
                        使用 Flask + MySQL + Redis 构建，支持日活 10 万用户
                    </li>
                    <li>
                        <strong>企业内部管理系统</strong><br>
                        使用 React + FastAPI 开发，实现完整的权限管理
                    </li>
                </ul>
            </section>
        </div>
    </div>
</body>
</html>
```

---

## 本章总结

### 学到的技能

| 技能 | 说明 |
|------|------|
| HTML 标签 | 文本、链接、表格、表单 |
| CSS 选择器 | 元素、类、ID、属性、伪类 |
| CSS 布局 | Flexbox、Grid |
| 响应式设计 | 媒体查询、视口 |

### 下一步

在 [第 3 章](./03-JavaScript 基础.md) 中，我们将学习 JavaScript 基础。

---

[← 上一章](./01-Web 基础入门.md) | [下一章 →](./03-JavaScript 基础.md)