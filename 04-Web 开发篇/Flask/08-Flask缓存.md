# Flask 缓存

掌握 Flask 缓存机制，提升应用性能。

---

## 1. Flask-Caching

### 1.1 安装

```bash
pip install flask-caching
```

### 1.2 配置

```python
from flask import Flask
from flask_caching import Cache

app = Flask(__name__)
app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300

cache = Cache(app)
```

### 1.3 缓存类型

| 类型 | 说明 |
|------|------|
| simple | 内存缓存（开发用） |
| redis | Redis 缓存 |
| memcached | Memcached 缓存 |
| filesystem | 文件系统缓存 |

---

## 2. 缓存使用

### 2.1 视图缓存

```python
@app.route('/api/data')
@cache.cached(timeout=60)
def get_data():
    # 耗时操作
    return {'data': expensive_operation()}
```

### 2.2 函数缓存

```python
@cache.memoize(timeout=300)
def expensive_function(param):
    # 缓存函数结果
    return compute(param)
```

### 2.3 手动缓存

```python
@app.route('/cache/set')
def set_cache():
    cache.set('key', 'value', timeout=60)
    return 'Cached'

@app.route('/cache/get')
def get_cache():
    value = cache.get('key')
    return str(value)

@app.route('/cache/delete')
def delete_cache():
    cache.delete('key')
    return 'Deleted'
```

---

## 3. Redis 缓存

### 3.1 配置

```python
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 0
app.config['CACHE_REDIS_PASSWORD'] = 'password'
```

### 3.2 使用

```python
# 缓存整个页面
@app.route('/users')
@cache.cached(timeout=60, query_string=True)
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])

# 缓存查询结果
def get_cached_user(user_id):
    cache_key = f'user_{user_id}'
    user = cache.get(cache_key)
    
    if not user:
        user = User.query.get(user_id)
        if user:
            cache.set(cache_key, user.to_dict(), timeout=300)
    
    return user
```

---

## 4. 完整示例

```python
from flask import Flask, jsonify
from flask_caching import Cache

app = Flask(__name__)
app.config['CACHE_TYPE'] = 'simple'
cache = Cache(app)

# 模拟数据库
data_store = {i: {'id': i, 'name': f'Item {i}'} for i in range(1, 101)}

@app.route('/items')
@cache.cached(timeout=60)
def get_items():
    return jsonify(list(data_store.values()))

@app.route('/items/<int:item_id>')
def get_item(item_id):
    cache_key = f'item_{item_id}'
    item = cache.get(cache_key)
    
    if not item:
        item = data_store.get(item_id)
        if item:
            cache.set(cache_key, item, timeout=300)
    
    return jsonify(item or {'error': 'Not found'})

@app.route('/cache/clear')
def clear_cache():
    cache.clear()
    return 'Cache cleared'

if __name__ == '__main__':
    app.run(debug=True)
```

---

## 总结

| 知识点 | 说明 |
|---------|------|
| Flask-Caching | 缓存扩展 |
| @cached | 视图缓存 |
| @memoize | 函数缓存 |
| Redis | 生产环境缓存 |

---

[← 上一章](./Flask/07-Flask认证授权.md) | [下一章](./Flask/09-Flask异步任务Celery.md)