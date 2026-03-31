# datetime 模块参考

Python datetime 模块提供日期和时间处理功能。

---

## 基本类型

### date 日期

```python
from datetime import date

# 创建日期
d = date(2024, 3, 15)
print(d)  # 2024-03-15

# 当前日期
today = date.today()
print(today)

# 从时间戳创建
d = date.fromtimestamp(1710460800)

# 从 ISO 格式创建
d = date.fromisoformat('2024-03-15')

# 属性
print(d.year)   # 2024
print(d.month)  # 3
print(d.day)    # 15

# 星期（0=周一, 6=周日）
print(d.weekday())  # 4（周五）

# ISO 星期（1=周一, 7=周日）
print(d.isoweekday())  # 5
```

### time 时间

```python
from datetime import time

# 创建时间
t = time(14, 30, 45, 123456)
print(t)  # 14:30:45.123456

# 属性
print(t.hour)        # 14
print(t.minute)      # 30
print(t.second)      # 45
print(t.microsecond) # 123456

# ISO 格式
print(t.isoformat())  # 14:30:45.123456
```

### datetime 日期时间

```python
from datetime import datetime

# 创建日期时间
dt = datetime(2024, 3, 15, 14, 30, 45)
print(dt)  # 2024-03-15 14:30:45

# 当前日期时间
now = datetime.now()
print(now)

# 当前 UTC 时间
utc_now = datetime.utcnow()
print(utc_now)

# 从字符串解析
dt = datetime.strptime('2024-03-15 14:30', '%Y-%m-%d %H:%M')

# 格式化输出
print(dt.strftime('%Y年%m月%d日 %H:%M'))  # 2024年03月15日 14:30

# 从 ISO 格式创建
dt = datetime.fromisoformat('2024-03-15T14:30:45')

# 属性
print(dt.year, dt.month, dt.day)
print(dt.hour, dt.minute, dt.second)
```

---

## 时间差 timedelta

### 创建时间差

```python
from datetime import datetime, timedelta

# 创建时间差
delta = timedelta(days=7, hours=3, minutes=30)
print(delta)  # 7 days, 3:30:00

# 属性
print(delta.days)       # 7
print(delta.seconds)    # 12600（3小时30分钟）
print(delta.total_seconds())  # 637800.0
```

### 时间运算

```python
from datetime import datetime, timedelta

now = datetime.now()

# 加减时间
tomorrow = now + timedelta(days=1)
last_week = now - timedelta(weeks=1)
in_3_hours = now + timedelta(hours=3)

print(f"明天: {tomorrow}")
print(f"上周: {last_week}")
print(f"3小时后: {in_3_hours}")

# 时间差
dt1 = datetime(2024, 3, 15)
dt2 = datetime(2024, 3, 20)
diff = dt2 - dt1
print(diff.days)  # 5
```

---

## 格式化

### strftime 格式化

```python
from datetime import datetime

dt = datetime(2024, 3, 15, 14, 30, 45)

# 常用格式
print(dt.strftime('%Y-%m-%d'))           # 2024-03-15
print(dt.strftime('%Y/%m/%d %H:%M'))     # 2024/03/15 14:30
print(dt.strftime('%Y年%m月%d日'))        # 2024年03月15日
print(dt.strftime('%A, %B %d, %Y'))      # Friday, March 15, 2024
```

**格式代码：**

| 代码 | 说明 | 示例 |
|------|------|------|
| `%Y` | 四位年份 | 2024 |
| `%y` | 两位年份 | 24 |
| `%m` | 月份（01-12） | 03 |
| `%d` | 日期（01-31） | 15 |
| `%H` | 小时（00-23） | 14 |
| `%M` | 分钟（00-59） | 30 |
| `%S` | 秒（00-59） | 45 |
| `%A` | 星期名称 | Friday |
| `%a` | 星期缩写 | Fri |
| `%B` | 月份名称 | March |
| `%b` | 月份缩写 | Mar |
| `%w` | 星期数字（0-6） | 5 |

### strptime 解析

```python
from datetime import datetime

# 从字符串解析
dt = datetime.strptime('2024-03-15', '%Y-%m-%d')
print(dt)  # 2024-03-15 00:00:00

dt = datetime.strptime('15/03/2024 14:30', '%d/%m/%Y %H:%M')
print(dt)  # 2024-03-15 14:30:00
```

---

## 时区处理

### timezone

```python
from datetime import datetime, timezone, timedelta

# UTC 时区
utc_dt = datetime.now(timezone.utc)
print(utc_dt)  # 2024-03-15 06:30:45+00:00

# 自定义时区（东八区）
beijing_tz = timezone(timedelta(hours=8))
beijing_dt = datetime.now(beijing_tz)
print(beijing_dt)  # 2024-03-15 14:30:45+08:00

# 时区转换
utc_dt = datetime.now(timezone.utc)
beijing_dt = utc_dt.astimezone(beijing_tz)
```

### zoneinfo（Python 3.9+）

```python
from datetime import datetime
from zoneinfo import ZoneInfo

# 使用 IANA 时区名称
dt = datetime.now(ZoneInfo('Asia/Shanghai'))
print(dt)  # 2024-03-15 14:30:45+08:00

dt = datetime.now(ZoneInfo('America/New_York'))
print(dt)  # 2024-03-15 02:30:45-04:00

# 时区转换
shanghai = datetime.now(ZoneInfo('Asia/Shanghai'))
new_york = shanghai.astimezone(ZoneInfo('America/New_York'))
```

---

## 常用示例

### 计算年龄

```python
from datetime import date

def calculate_age(birth_date):
    """计算年龄"""
    today = date.today()
    age = today.year - birth_date.year
    # 如果今年生日还没到，减 1
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age

birth = date(1990, 5, 15)
print(f"年龄: {calculate_age(birth)}")
```

### 计算工作日

```python
from datetime import date, timedelta

def count_workdays(start, end):
    """计算两个日期之间的工作日数"""
    workdays = 0
    current = start
    while current <= end:
        if current.weekday() < 5:  # 周一到周五
            workdays += 1
        current += timedelta(days=1)
    return workdays

start = date(2024, 3, 1)
end = date(2024, 3, 15)
print(f"工作日: {count_workdays(start, end)}")
```

### 倒计时

```python
from datetime import datetime

def countdown(target_date):
    """倒计时"""
    now = datetime.now()
    diff = target_date - now
    days = diff.days
    hours, remainder = divmod(diff.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days}天 {hours}小时 {minutes}分钟 {seconds}秒"

target = datetime(2024, 12, 31, 23, 59, 59)
print(countdown(target))
```