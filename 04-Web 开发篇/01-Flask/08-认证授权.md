# Flask 认证授权

掌握 Flask 用户认证和权限管理。

---

## 1. Flask-Login

### 1.1 安装

```bash
pip install flask-login flask-bcrypt
```

### 1.2 配置

```python
from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
```

### 1.3 用户模型

```python
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    
    def set_password(self, password):
        from flask_bcrypt import Bcrypt
        self.password_hash = Bcrypt().generate_password_hash(password).decode()
    
    def check_password(self, password):
        from flask_bcrypt import Bcrypt
        return Bcrypt().check_password_hash(self.password_hash, password)
```

### 1.4 加载用户

```python
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
```

---

## 2. 登录流程

### 2.1 登录视图

```python
from flask_login import login_user, logout_user, login_required
from flask import request, redirect, url_for, flash

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('用户名或密码错误')
    
    return render_template('auth/login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
```

### 2.2 受保护路由

```python
@app.route('/dashboard')
@login_required
def dashboard():
    return f'欢迎, {current_user.username}!'
```

---

## 3. JWT 认证

### 3.1 安装

```bash
pip install flask-jwt-extended
```

### 3.2 配置

```python
from flask_jwt_extended import JWTManager

app.config['JWT_SECRET_KEY'] = 'jwt-secret'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600

jwt = JWTManager(app)
```

### 3.3 使用

```python
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if user and user.check_password(data['password']):
        token = create_access_token(identity=user.id)
        return jsonify({'token': token})
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/protected')
@jwt_required()
def protected():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify({'user': user.username})
```

---

## 4. 权限管理

### 4.1 角色定义

```python
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', backref='users')
```

### 4.2 权限装饰器

```python
from functools import wraps
from flask import abort
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)
        if current_user.role.name != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin')
@admin_required
def admin_panel():
    return 'Admin Panel'
```

---

## 5. 完整示例

```python
# app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['JWT_SECRET_KEY'] = 'jwt-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
jwt = JWTManager(app)

# 模型
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(200))
    role = db.Column(db.String(20), default='user')
    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode()
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 路由
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'Created'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if user and user.check_password(data['password']):
        token = create_access_token(identity=user.id)
        return jsonify({'token': token})
    
    return jsonify({'error': 'Invalid'}), 401

@app.route('/profile')
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify({'username': user.username, 'email': user.email})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
```

---

## 总结

| 知识点 | 说明 |
|---------|------|
| Flask-Login | 会话认证 |
| UserMixin | 用户模型混入 |
| bcrypt | 密码哈希 |
| JWT | Token 认证 |
| 权限装饰器 | 角色权限 |

---

[← 上一章](./Flask/06-Flask蓝图Blueprint.md) | [下一章](./Flask/08-Flask缓存.md)