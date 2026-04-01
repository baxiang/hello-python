# Flask 数据库集成

深入学习 Flask-SQLAlchemy，掌握数据库模型设计、CRUD 操作和关系映射。

---

## 1. 安装和配置

### 1.1 安装依赖

```bash
pip install flask-sqlalchemy sqlalchemy pymysql
```

### 1.2 基本配置

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SQLite 配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

# MySQL 配置
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql+pymysql://username:password@localhost:3306/dbname'

# PostgreSQL 配置
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql://username:password@localhost:5432/dbname'

# 其他配置
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭修改追踪
app.config['SQLALCHEMY_ECHO'] = True  # 打印 SQL 语句（调试用）
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True
}

db = SQLAlchemy(app)
```

---

## 2. 数据模型

### 2.1 定义模型

```python
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    # 表名（可选，默认使用类名小写）
    __tablename__ = 'users'
    
    # 字段定义
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 字符串表示
    def __repr__(self):
        return f'<User {self.username}>'
    
    # 字典表示
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
```

### 2.2 字段类型

| SQLAlchemy 类型 | Python 类型 | 说明 |
|-----------------|------------|------|
| Integer | int | 整数 |
| BigInteger | int | 大整数 |
| Float | float | 浮点数 |
| String | str | 字符串 |
| Text | str | 长文本 |
| Boolean | bool | 布尔值 |
| DateTime | datetime | 日期时间 |
| Date | date | 日期 |
| Time | time | 时间 |
| LargeBinary | bytes | 二进制数据 |
| PickleType | any | Python 对象 |
| JSON | dict/list | JSON 数据 |

### 2.3 字段参数

```python
class User(db.Model):
    # 主键
    id = db.Column(db.Integer, primary_key=True)
    
    # 索引
    username = db.Column(db.String(80), index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    
    # 约束
    name = db.Column(db.String(100), nullable=False)  # 非空
    code = db.Column(db.String(10), unique=True)      # 唯一
    status = db.Column(db.String(20), default='active') # 默认值
    
    # 长度限制
    bio = db.Column(db.String(500))
    
    # 可变长度字符串
    slug = db.Column(db.Unicode(100))  # 支持 Unicode
    
    # 数字范围
    age = db.Column(db.Integer, db.CheckConstraint('age >= 0', 'age >= 0'))
    
    # 注释
    description = db.Column(db.String(500), comment='用户描述')
```

---

## 3. 关系映射

### 3.1 一对多关系

```python
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    # 关系定义
    books = db.relationship('Book', back_populates='author', lazy='dynamic')

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    
    # 反向引用
    author = db.relationship('Author', back_populates='books')

# 使用
author = Author.query.first()
for book in author.books:
    print(book.title)

book = Book.query.first()
print(book.author.name)
```

### 3.2 多对多关系

```python
# 关联表
association_table = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    
    tags = db.relationship('Tag', secondary=association_table, back_populates='posts')

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    
    posts = db.relationship('Post', secondary=association_table, back_populates='tags')

# 使用
post = Post.query.first()
for tag in post.tags:
    print(tag.name)

tag = Tag.query.first()
for post in tag.posts:
    print(post.title)
```

### 3.3 一对一关系

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    
    profile = db.relationship('UserProfile', back_populates='user', uselist=False)

class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    bio = db.Column(db.Text)
    
    user = db.relationship('User', back_populates='profile')
```

### 3.4 自引用关系

```python
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    
    # 自引用关系
    parent = db.relationship('Category', remote_side=[id], backref='children')
```

---

## 4. CRUD 操作

### 4.1 创建数据

```python
# 创建单条记录
user = User(username='john', email='john@example.com')
db.session.add(user)
db.session.commit()

# 创建并返回
user = User(username='john', email='john@example.com')
db.session.add(user)
db.session.flush()  # 获取 ID 但不提交
print(user.id)

# 批量创建
users = [
    User(username='user1', email='user1@example.com'),
    User(username='user2', email='user2@example.com'),
    User(username='user3', email='user3@example.com'),
]
db.session.add_all(users)
db.session.commit()
```

### 4.2 读取数据

```python
# 根据主键查询
user = User.query.get(1)

# 根据条件查询
user = User.query.filter_by(username='john').first()
users = User.query.filter(User.email.like('%@example.com')).all()

# 排序
users = User.query.order_by(User.created_at.desc()).all()

# 分页
page = User.query.paginate(page=1, per_page=20)
users = page.items
total = page.total

# 限制和偏移
users = User.query.limit(10).offset(0).all()

# 计数
count = User.query.count()

# 存在性检查
exists = User.query.filter_by(username='john').first() is not None
```

### 4.3 更新数据

```python
# 更新单条记录
user = User.query.get(1)
user.email = 'newemail@example.com'
db.session.commit()

# 批量更新
User.query.filter_by(is_active=False).update({'status': 'inactive'})
db.session.commit()

# 使用 SQL 函数
from sqlalchemy import func
User.query.filter(User.id > 10).update(
    {User.status: 'archived'},
    synchronize_session='fetch'
)
db.session.commit()
```

### 4.4 删除数据

```python
# 删除单条记录
user = User.query.get(1)
db.session.delete(user)
db.session.commit()

# 批量删除
User.query.filter_by(is_active=False).delete()
db.session.commit()

# 级联删除（需要配置）
# 在关系中设置 cascade='all, delete-orphan'
```

---

## 5. 查询进阶

### 5.1 复杂查询

```python
from sqlalchemy import and_, or_, not_

# AND 条件
users = User.query.filter(
    and_(
        User.is_active == True,
        User.created_at >= datetime(2024, 1, 1)
    )
).all()

# OR 条件
users = User.query.filter(
    or_(
        User.username == 'admin',
        User.email == 'admin@example.com'
    )
).all()

# NOT 条件
users = User.query.filter(
    not_(User.is_active == True)
).all()
```

### 5.2 联表查询

```python
# 联表查询
results = db.session.query(User, Book).join(
    Book, User.id == Book.author_id
).all()

for user, book in results:
    print(f'{user.username} - {book.title}')

# 使用关系查询
author = Author.query.first()
books = author.books.filter(Book.published == True).all()
```

### 5.3 聚合查询

```python
from sqlalchemy import func

# 计数
count = db.session.query(func.count(User.id)).scalar()

# 求和
total = db.session.query(func.sum(Order.amount)).scalar()

# 平均值
avg_price = db.session.query(func.avg(Product.price)).scalar()

# 分组统计
from sqlalchemy import case
results = db.session.query(
    User.status,
    func.count(User.id)
).group_by(User.status).all()

for status, count in results:
    print(f'{status}: {count}')
```

---

## 6. 模型事件

### 6.1 生命周期事件

```python
from sqlalchemy import event

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 创建前
    @staticmethod
    def before_insert(mapper, connection, target):
        target.email = target.email.lower()
    
    # 创建后
    @staticmethod
    def after_insert(mapper, connection, target):
        print(f'Created user: {target.username}')

# 注册事件
event.listen(User, 'before_insert', User.before_insert)
event.listen(User, 'after_insert', User.after_insert)
```

---

## 7. 迁移管理

### 7.1 使用 Flask-Migrate

```bash
pip install flask-migrate

# 初始化
flask db init

# 创建迁移
flask db migrate -m "add users table"

# 执行迁移
flask db upgrade

# 回滚
flask db downgrade
```

### 7.2 配置

```python
from flask import Flask
from flask_migrate import Migrate

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    migrate.init_app(app, db)
    return app
```

---

## 8. 完整示例

```python
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ==================== 模型定义 ====================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    posts = db.relationship('Post', back_populates='author', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    author = db.relationship('User', back_populates='posts')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'published': self.published,
            'author': self.author.username,
            'created_at': self.created_at.isoformat()
        }

# ==================== API 路由 ====================
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(username=data['username'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@app.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.filter_by(published=True).all()
    return jsonify([p.to_dict() for p in posts])

# ==================== 初始化 ====================
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
```

---

## 总结

| 知识点 | 说明 |
|---------|------|
| 配置 | 数据库连接配置 |
| 模型 | 表结构定义 |
| 关系 | 一对多、多对多、自引用 |
| CRUD | 增删改查操作 |
| 查询 | 过滤、排序、分页 |
| 事件 | 生命周期钩子 |
| 迁移 | Flask-Migrate |

---

[← 上一章](./Flask/02-Jinja2模板引擎.md) | [下一章](./Flask/04-Flask表单处理.md)