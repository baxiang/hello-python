# datetime 模块参考（详细版）

> Python 3.11+

## 第一部分：日期时间基础类型

### 1.1 date 日期对象

#### 实际场景

在日程管理、生日提醒、日期计算等场景中，需要处理纯日期信息。比如计算两个日期之间的天数、判断工作日等。

**问题：如何创建和操作日期对象？如何获取日期的年、月、日等属性？**

```python
from datetime import date

# 创建日期
d: date = date(2024, 3, 15)
print(d)  # 2024-03-15

# 当前日期
today: date = date.today()
print(today)

# 从时间戳创建
d_from_ts: date = date.fromtimestamp(1710460800)

# 从 ISO 格式创建
d_from_iso: date = date.fromisoformat('2024-03-15')

# 属性
year: int = d.year        # 2024
month: int = d.month      # 3
day: int = d.day          # 15

# 星期（0=周一, 6=周日）
weekday: int = d.weekday()  # 4（周五）

# ISO 星期（1=周一, 7=周日）
iso_weekday: int = d.isoweekday()  # 5
```

### 1.2 time 时间对象

#### 实际场景

在闹钟应用、时间调度、日志记录等场景中，需要处理纯时间信息。

**问题：如何创建和格式化时间对象？**

```python
from datetime import time

# 创建时间
t: time = time(14, 30, 45, 123456)
print(t)  # 14:30:45.123456

# 属性
hour: int = t.hour                # 14
minute: int = t.minute            # 30
second: int = t.second            # 45
microsecond: int = t.microsecond  # 123456

# ISO 格式
iso_str: str = t.isoformat()  # 14:30:45.123456
```

### 1.3 datetime 日期时间对象

#### 实际场景

在日志系统、数据记录、事件管理等场景中，需要同时处理日期和时间。比如记录事件发生时间、计算时间差等。

**问题：datetime 和 date、time 有什么关系？如何解析和格式化日期时间字符串？**

```python
from datetime import datetime

# 创建日期时间
dt: datetime = datetime(2024, 3, 15, 14, 30, 45)
print(dt)  # 2024-03-15 14:30:45

# 当前日期时间
now: datetime = datetime.now()
print(now)

# 当前 UTC 时间
utc_now: datetime = datetime.utcnow()
print(utc_now)

# 从字符串解析
dt_parsed: datetime = datetime.strptime('2024-03-15 14:30', '%Y-%m-%d %H:%M')

# 格式化输出
formatted: str = dt.strftime('%Y年%m月%d日 %H:%M')  # 2024年03月15日 14:30

# 从 ISO 格式创建
dt_from_iso: datetime = datetime.fromisoformat('2024-03-15T14:30:45')

# 属性
year: int = dt.year
month: int = dt.month
day: int = dt.day
hour: int = dt.hour
minute: int = dt.minute
second: int = dt.second
```

## 第二部分：时间差计算

### 2.1 创建时间差

#### 实际场景

在定时任务、倒计时、时间预算管理等场景中，需要表示和计算时间差。比如计算未来某天、过去某天等。

**问题：如何表示和计算时间差？**

```python
from datetime import datetime, timedelta

# 创建时间差
delta: timedelta = timedelta(days=7, hours=3, minutes=30)
print(delta)  # 7 days, 3:30:00

# 属性
days: int = delta.days           # 7
seconds: int = delta.seconds     # 12600（3小时30分钟）
total_secs: float = delta.total_seconds()  # 637800.0
```

### 2.2 时间运算

#### 实际场景

在项目管理、日程安排、账单计算等场景中，需要计算相对时间。比如计算到期时间、计算账单周期等。

**问题：如何对日期时间进行加减运算？如何计算两个日期之间的差值？**

```python
from datetime import datetime, timedelta

now: datetime = datetime.now()

# 加减时间
tomorrow: datetime = now + timedelta(days=1)
last_week: datetime = now - timedelta(weeks=1)
in_3_hours: datetime = now + timedelta(hours=3)

print(f"明天: {tomorrow}")
print(f"上周: {last_week}")
print(f"3小时后: {in_3_hours}")

# 时间差
dt1: datetime = datetime(2024, 3, 15)
dt2: datetime = datetime(2024, 3, 20)
diff: timedelta = dt2 - dt1
days_diff: int = diff.days  # 5
```

## 第三部分：日期时间格式化

### 3.1 strftime 格式化（核心）

**strftime：** 将日期时间格式化为字符串。

```
strftime语法：
┌─────────────────────────────────────────────────────────────┐
│  strftime 格式化                                               │
│                                                              │
│  dt.strftime('格式字符串')                                     │
│              ↑                                                │
│              格式代码组合                                      │
│                                                              │
│  示例：                                                        │
│  dt.strftime('%Y-%m-%d %H:%M:%S')                             │
│  # 输出：2024-03-15 14:30:45                                   │
│                                                              │
│  ⚠️ 常用格式代码：                                             │
│  ─────────────────────────────                               │
│  %Y  四位年份    2024                                         │
│  %m  月份(01-12) 03                                           │
│  %d  日期(01-31) 15                                           │
│  %H  小时(00-23) 14                                           │
│  %M  分钟(00-59) 30                                           │
│  %S  秒(00-59)  45                                            │
│                                                              │
│  组合示例：                                                    │
│  '%Y-%m-%d'         → 2024-03-15                             │
│  '%Y年%m月%d日'      → 2024年03月15日                          │
│  '%A, %B %d, %Y'    → Friday, March 15, 2024                  │
└─────────────────────────────────────────────────────────────┘
```

### 最简示例

```python
from datetime import datetime

dt = datetime(2024, 3, 15, 14, 30, 45)

fmt = dt.strftime('%Y-%m-%d')
print(fmt)  # 2024-03-15
```

### 关键代码解释

| 格式代码 | 说明 | 示例 |
|------|------|------|
| `%Y` | 四位年份 | 2024 |
| `%m` | 月份 | 03 |
| `%d` | 日期 | 15 |
| `%H:%M:%S` | 时间 | 14:30:45 |

### 详细示例

```python
from datetime import datetime

dt = datetime(2024, 3, 15, 14, 30, 45)

# 常用格式
fmt1 = dt.strftime('%Y-%m-%d')           # 2024-03-15
fmt2 = dt.strftime('%Y/%m/%d %H:%M')    # 2024/03/15 14:30
fmt3 = dt.strftime('%Y年%m月%d日')       # 2024年03月15日
fmt4 = dt.strftime('%A, %B %d, %Y')     # Friday, March 15, 2024
```

---

### strptime 解析（核心）

**strptime：** 将字符串解析为日期时间对象。

```
strptime语法：
┌─────────────────────────────────────────────────────────────┐
│  strptime 解析                                                 │
│                                                              │
│  datetime.strptime('字符串', '格式')                           │
│                     ↑          ↑                              │
│                     待解析      格式代码                        │
│                                                              │
│  ⚠️ 格式代码必须与字符串匹配：                                 │
│                                                              │
│  字符串：'2024-03-15'                                          │
│  格式：  '%Y-%m-%d'    ← 完全对应                              │
│                                                              │
│  字符串：'15/03/2024 14:30'                                    │
│  格式：  '%d/%m/%Y %H:%M' ← 对应分隔符                         │
│                                                              │
│  ❌ 错误示例：                                                 │
│  datetime.strptime('2024-03-15', '%d/%m/%Y')                  │
│  # ValueError: 格式不匹配                                      │
└─────────────────────────────────────────────────────────────┘
```

### 最简示例

```python
from datetime import datetime

dt = datetime.strptime('2024-03-15', '%Y-%m-%d')
print(dt)  # 2024-03-15 00:00:00
```

### 关键代码解释

| 要素 | 说明 | 示例 |
|------|------|------|
| 字符串 | 待解析文本 | `'2024-03-15'` |
| 格式 | 对应格式代码 | `'%Y-%m-%d'` |
| 分隔符 | 必须匹配 | `-` 对应 `-` |

---

## 第四部分：时区处理

### 4.1 timezone 时区

#### 实际场景

在跨国应用、服务器时间处理、API 开发等场景中，需要处理不同时区的时间。比如用户在不同地区看到本地时间、服务器使用 UTC 时间等。

**问题：如何创建和转换不同时区的日期时间？**

```python
from datetime import datetime, timezone, timedelta

# UTC 时区
utc_dt: datetime = datetime.now(timezone.utc)
print(utc_dt)  # 2024-03-15 06:30:45+00:00

# 自定义时区（东八区）
beijing_tz: timezone = timezone(timedelta(hours=8))
beijing_dt: datetime = datetime.now(beijing_tz)
print(beijing_dt)  # 2024-03-15 14:30:45+08:00

# 时区转换
utc_dt2: datetime = datetime.now(timezone.utc)
beijing_dt2: datetime = utc_dt2.astimezone(beijing_tz)
```

### 4.2 zoneinfo 时区信息（Python 3.9+）

#### 实际场景

在实际开发中，需要使用真实的时区名称（如 Asia/Shanghai），而不仅仅是时差。`zoneinfo` 模块提供了完整的 IANA 时区数据库。

**问题：如何使用真实时区名称（如 Asia/Shanghai）进行时区转换？**

```python
from datetime import datetime
from zoneinfo import ZoneInfo

# 使用 IANA 时区名称
shanghai_dt: datetime = datetime.now(ZoneInfo('Asia/Shanghai'))
print(shanghai_dt)  # 2024-03-15 14:30:45+08:00

newyork_dt: datetime = datetime.now(ZoneInfo('America/New_York'))
print(newyork_dt)  # 2024-03-15 02:30:45-04:00

# 时区转换
shanghai: datetime = datetime.now(ZoneInfo('Asia/Shanghai'))
new_york: datetime = shanghai.astimezone(ZoneInfo('America/New_York'))
```

## 第五部分：实际应用示例

### 5.1 计算年龄

#### 实际场景

在用户管理、身份验证、生日提醒等场景中，需要根据出生日期计算年龄。

```python
from datetime import date

def calculate_age(birth_date: date) -> int:
    """计算年龄"""
    today: date = date.today()
    age: int = today.year - birth_date.year
    # 如果今年生日还没到，减 1
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age

birth: date = date(1990, 5, 15)
age: int = calculate_age(birth)
print(f"年龄: {age}")
```

### 5.2 计算工作日

#### 实际场景

在项目管理、考勤统计、工期计算等场景中，需要计算两个日期之间的工作日数（排除周末）。

```python
from datetime import date, timedelta

def count_workdays(start: date, end: date) -> int:
    """计算两个日期之间的工作日数"""
    workdays: int = 0
    current: date = start
    while current <= end:
        if current.weekday() < 5:  # 周一到周五
            workdays += 1
        current += timedelta(days=1)
    return workdays

start_date: date = date(2024, 3, 1)
end_date: date = date(2024, 3, 15)
workdays: int = count_workdays(start_date, end_date)
print(f"工作日: {workdays}")
```

### 5.3 倒计时

#### 实际场景

在活动倒计时、任务截止提醒等场景中，需要计算距离目标时间还剩多少。

```python
from datetime import datetime

def countdown(target_date: datetime) -> str:
    """倒计时"""
    now: datetime = datetime.now()
    diff: timedelta = target_date - now
    days: int = diff.days
    hours: int
    remainder: int
    hours, remainder = divmod(diff.seconds, 3600)
    minutes: int
    seconds: int
    minutes, seconds = divmod(remainder, 60)
    return f"{days}天 {hours}小时 {minutes}分钟 {seconds}秒"

target: datetime = datetime(2024, 12, 31, 23, 59, 59)
result: str = countdown(target)
print(result)
```

**关键代码说明：**

| 代码 | 含义 | 为什么这样写 |
|------|------|-------------|
| `if (today.month, today.day) < (birth_date.month, birth_date.day)` | 元组比较判断今年生日是否已过 | 元组按位比较：先比月，再比日，一行代替 `if month < m or (month == m and day < d)` |
| `current.weekday() < 5` | 判断是否工作日（0=周一，4=周五） | `weekday()` 返回 0-6，小于 5 即周一到周五，比 `isoweekday()` 减 1 后判断更直观 |
| `diff.seconds` | 获取 timedelta 中不满一天的秒数 | `timedelta` 存储为 `(days, seconds, microseconds)`，`seconds` 最大为 86399 |
| `divmod(diff.seconds, 3600)` | 一次性分解小时和余秒 | `divmod(a, b)` 返回 `(商, 余数)`，比手动写 `// 3600` 和 `% 3600` 更简洁 |