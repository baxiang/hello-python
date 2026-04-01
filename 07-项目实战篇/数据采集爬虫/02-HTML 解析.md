# HTML 解析

学习使用 BeautifulSoup 解析 HTML 提取数据。

---

## 1. BeautifulSoup 基础

### 1.1 安装

```bash
uv add beautifulsoup4 lxml
```

### 1.2 创建解析对象

```python
from bs4 import BeautifulSoup
import requests

# 从网页获取
response = requests.get("https://example.com")
soup = BeautifulSoup(response.text, "lxml")

# 从字符串创建
html = """
<html>
  <head><title>测试页面</title></head>
  <body>
    <div class="content">
      <h1>标题</h1>
      <p class="intro">段落内容</p>
      <ul>
        <li>项目 1</li>
        <li>项目 2</li>
      </ul>
    </div>
  </body>
</html>
"""
soup = BeautifulSoup(html, "lxml")
```

---

## 2. 查找元素

### 2.1 基本方法

```python
# find - 查找第一个匹配元素
title = soup.find("title")
print(title.text)  # 测试页面

# find_all - 查找所有匹配元素
items = soup.find_all("li")
for item in items:
    print(item.text)  # 项目 1, 项目 2

# 限制数量
items = soup.find_all("li", limit=1)
```

### 2.2 按属性查找

```python
# 按 class 查找
intro = soup.find("p", class_="intro")
# 或使用字典
intro = soup.find("p", {"class": "intro"})

# 按 id 查找
element = soup.find(id="main")

# 按多个属性查找
element = soup.find("div", {"class": "content", "id": "main"})

# 查找包含特定属性的元素
links = soup.find_all("a", href=True)  # 有 href 属性的 a 标签
```

### 2.3 CSS 选择器

```python
# select - 返回列表
items = soup.select("ul li")           # 后代选择器
items = soup.select("ul > li")         # 子选择器
items = soup.select(".intro")          # class 选择器
items = soup.select("#main")           # id 选择器
items = soup.select("p.intro")         # 标签 + class
items = soup.select("div.content h1")  # 组合选择器

# select_one - 返回第一个
title = soup.select_one("h1")
```

---

## 3. 提取数据

### 3.1 提取文本

```python
# 获取文本内容
p = soup.find("p")
print(p.text)        # 段落内容（包含子元素文本）
print(p.string)      # 段落内容（仅当只有一个文本节点时）
print(p.get_text())  # 同 text

# 去除空白
print(p.get_text(strip=True))

# 指定分隔符
print(p.get_text(separator="|"))
```

### 3.2 提取属性

```python
# 获取属性值
link = soup.find("a")
print(link.get("href"))     # URL
print(link["href"])         # 同上，但属性不存在会报错
print(link.get("title"))    # None（属性不存在）

# 获取所有属性
print(link.attrs)           # {'href': '...', 'class': ['btn']}
```

### 3.3 遍历元素

```python
div = soup.find("div")

# 子元素
for child in div.children:
    print(child)

# 所有子孙元素
for descendant in div.descendants:
    print(descendant)

# 父元素
parent = div.parent

# 兄弟元素
next_sibling = div.next_sibling
prev_sibling = div.previous_sibling
```

---

## 4. 实战示例

### 4.1 爬取新闻标题

```python
import requests
from bs4 import BeautifulSoup

def scrape_news(url: str) -> list:
    """爬取新闻标题和链接"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    
    news_list = []
    
    # 假设新闻在 <div class="news-item"> 中
    items = soup.select(".news-item")
    
    for item in items:
        title_elem = item.select_one("h2 a")
        if title_elem:
            news_list.append({
                "title": title_elem.text.strip(),
                "url": title_elem.get("href")
            })
    
    return news_list

# 使用
news = scrape_news("https://news.example.com")
for item in news:
    print(f"{item['title']}: {item['url']}")
```

### 4.2 爬取表格数据

```python
def scrape_table(url: str) -> list:
    """爬取表格数据"""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    
    table = soup.find("table")
    rows = table.find_all("tr")
    
    data = []
    headers = []
    
    for i, row in enumerate(rows):
        cells = row.find_all(["th", "td"])
        cell_data = [cell.text.strip() for cell in cells]
        
        if i == 0:  # 表头
            headers = cell_data
        else:
            data.append(dict(zip(headers, cell_data)))
    
    return data
```

### 4.3 爬取分页数据

```python
def scrape_paginated(base_url: str, pages: int = 5) -> list:
    """爬取分页数据"""
    all_data = []
    
    for page in range(1, pages + 1):
        url = f"{base_url}?page={page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "lxml")
        
        items = soup.select(".item")
        if not items:  # 没有数据了
            break
        
        for item in items:
            all_data.append({
                "title": item.select_one(".title").text,
                "price": item.select_one(".price").text
            })
        
        print(f"已爬取第 {page} 页，共 {len(items)} 条")
    
    return all_data
```

---

## 本章小结

```
┌─────────────────────────────────────────────────────────────┐
│                    HTML 解析知识要点                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   查找元素：                                                 │
│   ✓ find/find_all 标签查找                                  │
│   ✓ select/select_one CSS 选择器                            │
│   ✓ 按属性、class、id 查找                                  │
│                                                             │
│   提取数据：                                                 │
│   ✓ text/string/get_text() 文本                             │
│   ✓ get("attr") / ["attr"] 属性                             │
│                                                             │
│   遍历：                                                     │
│   ✓ children/descendants 子元素                             │
│   ✓ parent 父元素                                           │
│   ✓ siblings 兄弟元素                                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

[← 上一章：HTTP 请求基础](./01-HTTP%20请求基础.md) | [下一章：动态页面爬取 →](./03-动态页面爬取.md)