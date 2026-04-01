# Flask 示例

"""
Flask Web 框架示例
包含：路由、模板、表单、REST API
"""

from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)


# 1. 基本路由
@app.route("/")
def index():
    """首页"""
    return "<h1>Hello, Flask!</h1>"


@app.route("/hello/<name>")
def hello(name):
    """动态路由"""
    return f"<h1>Hello, {name}!</h1>"


# 2. HTTP 方法
@app.route("/api/users", methods=["GET", "POST"])
def users():
    """用户 API"""
    if request.method == "GET":
        return jsonify({"users": ["Alice", "Bob", "Charlie"]})
    elif request.method == "POST":
        data = request.get_json()
        return jsonify({"message": "用户创建成功", "user": data}), 201


# 3. 模板渲染
@app.route("/template")
def template_example():
    """模板示例"""
    template = """
    <!DOCTYPE html>
    <html>
    <head><title>Flask 模板</title></head>
    <body>
        <h1>{{ title }}</h1>
        <ul>
        {% for item in items %}
            <li>{{ item }}</li>
        {% endfor %}
        </ul>
    </body>
    </html>
    """
    return render_template_string(
        template,
        title="Flask 模板示例",
        items=["Python", "Flask", "Web 开发"]
    )


# 4. 表单处理
@app.route("/form", methods=["GET", "POST"])
def form_example():
    """表单示例"""
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        return f"<h1>提交成功</h1><p>姓名: {name}</p><p>邮箱: {email}</p>"
    
    return """
    <form method="POST">
        <p><input name="name" placeholder="姓名"></p>
        <p><input name="email" placeholder="邮箱"></p>
        <p><button type="submit">提交</button></p>
    </form>
    """


# 5. REST API
class UserAPI:
    """用户 API 类"""
    
    users = [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"},
    ]
    
    @staticmethod
    @app.route("/api/v1/users", methods=["GET"])
    def get_users():
        return jsonify(UserAPI.users)
    
    @staticmethod
    @app.route("/api/v1/users/<int:user_id>", methods=["GET"])
    def get_user(user_id):
        user = next((u for u in UserAPI.users if u["id"] == user_id), None)
        if user:
            return jsonify(user)
        return jsonify({"error": "用户不存在"}), 404
    
    @staticmethod
    @app.route("/api/v1/users", methods=["POST"])
    def create_user():
        data = request.get_json()
        new_user = {
            "id": len(UserAPI.users) + 1,
            "name": data.get("name"),
            "email": data.get("email")
        }
        UserAPI.users.append(new_user)
        return jsonify(new_user), 201


# 6. 错误处理
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "页面不存在"}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "服务器错误"}), 500


# 7. 请求钩子
@app.before_request
def before_request():
    """请求前处理"""
    print(f"请求: {request.method} {request.path}")


@app.after_request
def after_request(response):
    """请求后处理"""
    print(f"响应: {response.status_code}")
    return response


if __name__ == "__main__":
    print("=" * 40)
    print("Flask 示例")
    print("=" * 40)
    print("\n访问 http://127.0.0.1:5000")
    print("\n路由:")
    print("  GET  /              - 首页")
    print("  GET  /hello/<name>  - 问候")
    print("  GET  /api/users     - 用户列表")
    print("  POST /api/users     - 创建用户")
    print("  GET  /template      - 模板示例")
    print("  GET  /form          - 表单示例")
    
    app.run(debug=True, port=5000)