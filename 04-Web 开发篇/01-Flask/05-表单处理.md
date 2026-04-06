# Flask 表单处理

掌握 Flask-WTF 表单创建、验证和处理。

---

## 1. Flask-WTF 基础

### 1.1 安装

```bash
pip install flask-wtf email-validator
```

### 1.2 基本配置

```python
from flask import Flask
from flask_wtf import FlaskForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

# CSRF 配置
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_TIME_LIMIT'] = 3600
```

---

## 2. 创建表单

### 2.1 基础表单

```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('登录')
```

### 2.2 完整注册表单

```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, TextAreaField, BooleanField
from wtforms.validators import (
    DataRequired, Email, Length, EqualTo, 
    Optional, NumberRange
)

class RegisterForm(FlaskForm):
    # 文本字段
    username = StringField(
        '用户名',
        validators=[
            DataRequired(message='用户名不能为空'),
            Length(min=3, max=20, message='用户名长度3-20字符')
        ]
    )
    
    email = StringField(
        '邮箱',
        validators=[
            DataRequired(message='邮箱不能为空'),
            Email(message='请输入有效的邮箱地址')
        ]
    )
    
    password = PasswordField(
        '密码',
        validators=[
            DataRequired(message='密码不能为空'),
            Length(min=6, message='密码至少6位')
        ]
    )
    
    confirm_password = PasswordField(
        '确认密码',
        validators=[
            DataRequired(message='请确认密码'),
            EqualTo('password', message='两次密码不一致')
        ]
    )
    
    bio = TextAreaField(
        '个人简介',
        validators=[Optional(), Length(max=500)]
    )
    
    age = IntegerField(
        '年龄',
        validators=[Optional(), NumberRange(min=0, max=150)]
    )
    
    agree_terms = BooleanField(
        '同意服务条款',
        validators=[DataRequired(message='必须同意服务条款')]
    )
    
    submit = SubmitField('注册')
```

---

## 3. 模板中使用表单

### 3.1 渲染表单

```html
<form method="POST" action="{{ url_for('register') }}">
    {{ form.hidden_tag() }}  <!-- CSRF token -->
    
    <div>
        {{ form.username.label }}
        {{ form.username(size=20) }}
        {% if form.username.errors %}
            <ul class="errors">
            {% for error in form.username.errors %}
                <li>{{ error }}</li>
            {% endfor %}
            </ul>
        {% endif %}
    </div>
    
    <div>
        {{ form.email.label }}
        {{ form.email() }}
        {% for error in form.email.errors %}
            <span class="error">{{ error }}</span>
        {% endfor %}
    </div>
    
    <div>
        {{ form.password.label }}
        {{ form.password() }}
    </div>
    
    <div>
        {{ form.confirm_password.label }}
        {{ form.confirm_password() }}
    </div>
    
    {{ form.submit() }}
</form>
```

### 3.2 简化渲染

```html
<!-- 使用 quick_form 快速渲染 -->
{{ quick_form(form, action=url_for('register'), method='post') }}
```

---

## 4. 处理表单数据

### 4.1 视图函数

```python
from flask import render_template, request, redirect, url_for, flash

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    
    if request.method == 'POST' and form.validate_on_submit():
        # 获取表单数据
        username = form.username.data
        email = form.email.data
        password = form.password.data
        
        # 处理数据...
        
        flash('注册成功！', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)
```

### 4.2 自定义验证

```python
from wtforms.validators import ValidationError

class RegisterForm(FlaskForm):
    # ... 其他字段 ...
    
    # 自定义验证器
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('用户名已存在')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('邮箱已被注册')
```

---

## 5. 文件上传表单

```python
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired

class UploadForm(FlaskForm):
    avatar = FileField(
        '头像',
        validators=[
            FileRequired(message='请选择文件'),
            FileAllowed(['jpg', 'png', 'gif'], message='只支持 jpg, png, gif 格式')
        ]
    )
    
    document = FileField(
        '文档',
        validators=[
            FileAllowed(['pdf', 'doc', 'docx'], message='只支持 PDF 和 Word 文档')
        ]
    )
    
    submit = SubmitField('上传')
```

---

## 6. 完整示例

### 6.1 表单类

```python
# forms.py
from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, TextAreaField, 
    IntegerField, SelectField, BooleanField,
    SubmitField
)
from wtforms.validators import (
    DataRequired, Email, Length, EqualTo,
    Optional, NumberRange
)

class ContactForm(FlaskForm):
    name = StringField(
        '姓名',
        validators=[DataRequired(), Length(max=50)],
        render_kw={'placeholder': '请输入姓名'}
    )
    
    email = StringField(
        '邮箱',
        validators=[DataRequired(), Email()],
        render_kw={'placeholder': 'example@mail.com'}
    )
    
    subject = SelectField(
        '主题',
        choices=[
            ('general', '一般咨询'),
            ('bug', '问题反馈'),
            ('business', '商务合作'),
            ('other', '其他')
        ],
        validators=[DataRequired()]
    )
    
    message = TextAreaField(
        '留言内容',
        validators=[DataRequired(), Length(min=10, max=1000)],
        render_kw={'rows': 5, 'placeholder': '请输入留言内容'}
    )
    
    subscribe = BooleanField('订阅Newsletter', default=True)
    
    submit = SubmitField('提交')
```

### 6.2 模板

```html
<!-- templates/contact.html -->
<!DOCTYPE html>
<html>
<head>
    <title>联系我们</title>
    <style>
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input, textarea, select { 
            width: 100%; 
            padding: 8px; 
            border: 1px solid #ddd; 
            border-radius: 4px;
        }
        .error { color: red; font-size: 0.9em; }
        .success { color: green; }
    </style>
</head>
<body>
    <h1>联系我们</h1>
    
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <div class="{{ category }}">{{ message }}</div>
            {% endfor %}
        {% endif %}
    {% endwith %}
    
    <form method="POST">
        {{ form.hidden_tag() }}
        
        <div class="form-group">
            {{ form.name.label }}
            {{ form.name() }}
            {% for error in form.name.errors %}
                <span class="error">{{ error }}</span>
            {% endfor %}
        </div>
        
        <div class="form-group">
            {{ form.email.label }}
            {{ form.email() }}
            {% for error in form.email.errors %}
                <span class="error">{{ error }}</span>
            {% endfor %}
        </div>
        
        <div class="form-group">
            {{ form.subject.label }}
            {{ form.subject() }}
        </div>
        
        <div class="form-group">
            {{ form.message.label }}
            {{ form.message() }}
            {% for error in form.message.errors %}
                <span class="error">{{ error }}</span>
            {% endfor %}
        </div>
        
        <div class="form-group">
            {{ form.subscribe() }} {{ form.subscribe.label }}
        </div>
        
        <div class="form-group">
            {{ form.submit() }}
        </div>
    </form>
</body>
</html>
```

### 6.3 视图函数

```python
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    
    if form.validate_on_submit():
        # 处理表单数据
        name = form.name.data
        email = form.email.data
        subject = form.subject.data
        message = form.message.data
        subscribe = form.subscribe.data
        
        # 保存到数据库或发送邮件
        save_message(name, email, subject, message)
        
        flash('感谢您的留言！', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html', form=form)
```

---

## 总结

| 知识点 | 说明 |
|---------|------|
| Flask-WTF | 表单处理扩展 |
| 字段类型 | String, Password, TextArea 等 |
| 验证器 | DataRequired, Email, Length 等 |
| CSRF 保护 | hidden_tag() |
| 自定义验证 | validate_字段名 |
| 文件上传 | FileField, FileAllowed |

---

[← 上一章](./Flask/03-Flask数据库集成.md) | [下一章](./Flask/05-Flask文件上传下载.md)