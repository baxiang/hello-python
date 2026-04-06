# Flask 文件上传下载

掌握 Flask 文件上传、下载和管理。

---

## 1. 基础文件上传

### 1.1 简单上传

```python
from flask import Flask, request, render_template_string

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

import os
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

HTML = '''
<!DOCTYPE html>
<html>
<body>
    <h1>文件上传</h1>
    <form method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <button type="submit">上传</button>
    </form>
    {% if filename %}
    <p>上传成功: {{ filename }}</p>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template_string(HTML, filename=filename)
    
    return render_template_string(HTML)
```

---

## 2. 安全上传

### 2.1 安全配置

```python
import os
from werkzeug.utils import secure_filename

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        
        if not file:
            return {'error': '没有选择文件'}, 400
        
        if not allowed_file(file.filename):
            return {'error': '不支持的文件类型'}, 400
        
        # 安全文件名
        filename = secure_filename(file.filename)
        
        # 防止文件名冲突
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S_')
        filename = timestamp + filename
        
        # 保存文件
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        return {'message': '上传成功', 'filename': filename}
    
    return {'message': 'POST 文件到此处'}
```

### 2.2 文件大小限制

```python
from flask import Flask, request

app = Flask(__name__)

# 全局大小限制
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# 路由级别限制
@app.route('/upload', methods=['POST'])
def upload():
    # 获取文件
    file = request.files.get('file')
    
    # 检查文件大小
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)
    
    if size > 10 * 1024 * 1024:  # 10MB
        return {'error': '文件太大'}, 400
    
    # 保存文件
    file.save(f'uploads/{file.filename}')
    return {'message': '上传成功'}
```

---

## 3. 多文件上传

### 3.1 批量上传

```python
@app.route('/upload/multiple', methods=['POST'])
def upload_multiple():
    files = request.files.getlist('files')
    
    uploaded = []
    errors = []
    
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            uploaded.append(filename)
        else:
            errors.append(file.filename if file else 'unknown')
    
    return {
        'uploaded': uploaded,
        'errors': errors,
        'total': len(uploaded)
    }
```

### 3.2 前端多文件

```html
<form method="post" enctype="multipart/form-data">
    <input type="file" name="files" multiple>
    <button type="submit">上传多个文件</button>
</form>
```

---

## 4. 文件下载

### 4.1 直接下载

```python
from flask import send_from_directory, send_file

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(
        app.config['UPLOAD_FOLDER'], 
        filename,
        as_attachment=True
    )
```

### 4.2 动态生成文件

```python
import io
from flask import Response

@app.route('/export/csv')
def export_csv():
    # 生成 CSV 数据
    output = io.StringIO()
    output.write('Name,Email\n')
    output.write('John,john@example.com\n')
    output.write('Jane,jane@example.com\n')
    
    # 返回文件
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment;filename=users.csv'}
    )
```

---

## 5. 完整上传类

### 5.1 上传管理器

```python
import os
import hashlib
from datetime import datetime
from werkzeug.utils import secure_filename

class FileUploader:
    def __init__(self, upload_folder, allowed_extensions=None):
        self.upload_folder = upload_folder
        self.allowed_extensions = allowed_extensions or {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
        os.makedirs(upload_folder, exist_ok=True)
    
    def save(self, file, custom_name=None):
        """保存文件"""
        if not file:
            raise ValueError('No file provided')
        
        # 验证文件类型
        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        
        if ext not in self.allowed_extensions:
            raise ValueError(f'File type not allowed: {ext}')
        
        # 生成唯一文件名
        if custom_name:
            filename = f"{custom_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
        else:
            # 使用哈希避免文件名冲突
            file_hash = hashlib.md5(file.read()).hexdigest()[:8]
            file.seek(0)
            filename = f"{file_hash}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
        
        # 保存文件
        filepath = os.path.join(self.upload_folder, filename)
        file.save(filepath)
        
        return {
            'filename': filename,
            'filepath': filepath,
            'size': os.path.getsize(filepath)
        }
    
    def delete(self, filename):
        """删除文件"""
        filepath = os.path.join(self.upload_folder, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False
    
    def list_files(self):
        """列出所有文件"""
        files = []
        for filename in os.listdir(self.upload_folder):
            filepath = os.path.join(self.upload_folder, filename)
            if os.path.isfile(filepath):
                files.append({
                    'filename': filename,
                    'size': os.path.getsize(filepath),
                    'modified': datetime.fromtimestamp(os.path.getmtime(filepath))
                })
        return files

# 使用
uploader = FileUploader('uploads', {'png', 'jpg', 'gif'})
```

---

## 6. 完整示例

### 6.1 应用代码

```python
from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

uploader = FileUploader(
    app.config['UPLOAD_FOLDER'],
    {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx'}
)

@app.route('/')
def index():
    files = uploader.list_files()
    return render_template('files.html', files=files)

@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files.get('file')
        if not file:
            return jsonify({'error': 'No file provided'}), 400
        
        result = uploader.save(file)
        return jsonify({
            'success': True,
            'filename': result['filename'],
            'size': result['size']
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        filename,
        as_attachment=True
    )

@app.route('/delete/<filename>', methods=['POST'])
def delete(filename):
    if uploader.delete(filename):
        return jsonify({'success': True})
    return jsonify({'error': 'File not found'}), 404
```

---

## 总结

| 知识点 | 说明 |
|---------|------|
| request.files | 获取上传文件 |
| secure_filename | 安全文件名 |
| allowed_extensions | 文件类型限制 |
| send_from_directory | 文件下载 |
| 文件大小限制 | MAX_CONTENT_LENGTH |

---

[← 上一章](./Flask/04-Flask表单处理.md) | [下一章](./Flask/06-Flask蓝图Blueprint.md)