# datetime 日期时间

> Python 3.11+

---

## 为什么需要 datetime 模块？

### 问题场景

你需要计算用户年龄、记录操作时间戳、或者把前端传来的字符串 `"2024-03-15"` 转成可以做加减的日期对象：

```python
# ❌ 用字符串处理日期：无法做加减，容易出错
birthday = "1990-05-15"
age = 2024 - int(birthday[:4])    # 忽略了今年生日是否已过

# ✅ 用 datetime：类型安全，支持加减、比较、格式化
from datetime import date, datetime, timedelta

birthday = date(1990, 5, 15)
today = date.today()
age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))

# 7 天后的日期
next_week = today + timedelta(days=7)

# 解析前端日期字符串
dt = datetime.strptime("2024-03-15 14:30", "%Y-%m-%d %H:%M")
```

`datetime` 模块是 Python 处理日期时间的标准工具，无需额外安装。

---

## 章节导航

| 部分 | 内容 |
|------|------|
| 第一部分 | 三种基础类型：date、time、datetime |
| 第二部分 | timedelta 时间差计算与运算 |
| 第三部分 | strftime 格式化与 strptime 解析 |
| 第四部分 | 时区处理（timezone / zoneinfo） |
| 第五部分 | 实际应用（年龄/工作日/倒计时） |
| L2 实践层 | 推荐做法、反模式、常见陷阱、适用场景 |

---

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

### 3.1 strftime 格式化

#### 实际场景

将 `datetime` 对象转换为人类可读的字符串，用于显示、日志记录、文件命名等场景。

**问题：如何把日期时间格式化为 "2024年03月15日" 或 "2024-03-15 14:30:45"？**

```
┌─────────────────────────────────────────────────────────────┐
│                  常用格式代码速查                              │
├────────┬──────────────────┬──────────────────────────────────┤
│  代码  │  说明            │  示例值                           │
├────────┼──────────────────┼──────────────────────────────────┤
│  %Y    │  四位年份        │  2024                            │
│  %m    │  月份 (01-12)    │  03                              │
│  %d    │  日期 (01-31)    │  15                              │
│  %H    │  小时 (00-23)    │  14                              │
│  %M    │  分钟 (00-59)    │  30                              │
│  %S    │  秒   (00-59)    │  45                              │
│  %A    │  星期全称        │  Friday                          │
│  %a    │  星期缩写        │  Fri                             │
│  %B    │  月份全称        │  March                           │
└────────┴──────────────────┴──────────────────────────────────┘
```

```python
from datetime import datetime

dt = datetime(2024, 3, 15, 14, 30, 45)

# 常用格式
fmt1: str = dt.strftime('%Y-%m-%d')           # 2024-03-15
fmt2: str = dt.strftime('%Y/%m/%d %H:%M')    # 2024/03/15 14:30
fmt3: str = dt.strftime('%Y年%m月%d日')       # 2024年03月15日
fmt4: str = dt.strftime('%A, %B %d, %Y')     # Friday, March 15, 2024
fmt5: str = dt.strftime('%Y-%m-%d %H:%M:%S') # 2024-03-15 14:30:45
```

**关键代码说明：**

| 格式代码 | 说明 | 示例输出 |
|---------|------|---------|
| `%Y-%m-%d` | ISO 日期格式 | `2024-03-15` |
| `%H:%M:%S` | 24 小时制时间 | `14:30:45` |
| `%Y年%m月%d日` | 中文格式 | `2024年03月15日` |

### 3.2 strptime 解析

#### 实际场景

将前端传来的日期字符串、CSV 文件中的时间列解析为 `datetime` 对象，用于计算和比较。

**问题：如何把 `"2024-03-15 14:30"` 字符串转换为可加减的 datetime 对象？**

```
┌─────────────────────────────────────────────────────────────┐
│   strptime 要点：格式代码必须与字符串完全匹配                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   字符串：'2024-03-15'                                       │
│   格式：  '%Y-%m-%d'    ← 分隔符 - 对应 -                    │
│                                                             │
│   字符串：'15/03/2024 14:30'                                 │
│   格式：  '%d/%m/%Y %H:%M'  ← 注意日在前、月在后             │
│                                                             │
│   ❌ 格式不匹配 → ValueError                                 │
│   datetime.strptime('2024-03-15', '%d/%m/%Y')               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

```python
from datetime import datetime

# 解析常见格式
dt1: datetime = datetime.strptime('2024-03-15', '%Y-%m-%d')
dt2: datetime = datetime.strptime('2024-03-15 14:30:45', '%Y-%m-%d %H:%M:%S')
dt3: datetime = datetime.strptime('15/03/2024', '%d/%m/%Y')

# 推荐：ISO 格式字符串用 fromisoformat()（更快）
dt4: datetime = datetime.fromisoformat('2024-03-15T14:30:45')

print(dt1)  # 2024-03-15 00:00:00
print(dt4)  # 2024-03-15 14:30:45
```

**关键代码说明：**

| 要素 | 说明 | 示例 |
|------|------|------|
| `strptime(s, fmt)` | 字符串 → datetime，格式必须精确匹配 | `strptime('2024-03-15', '%Y-%m-%d')` |
| `fromisoformat(s)` | ISO 格式专用，比 `strptime` 快 | `fromisoformat('2024-03-15T14:30')` |
| `ValueError` | 格式不匹配时抛出 | 格式字符串与输入不对应 |

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

---

## L2 实践层：最佳实践

### 推荐做法

| 做法 | 原因 | 示例 |
|------|------|------|
| ISO 格式字符串用 `fromisoformat()` | 比 `strptime` 快，写法简洁 | `datetime.fromisoformat('2024-03-15T14:30')` |
| 存储时间用 UTC，显示时转本地时区 | 跨时区系统的标准做法，避免歧义 | `datetime.now(timezone.utc)` |
| 用 `zoneinfo.ZoneInfo` 处理真实时区 | 能正确处理夏令时 | `ZoneInfo('Asia/Shanghai')` |
| 时间差用 `timedelta`，不要手动换算 | 避免"一天=86400秒"在夏令时时出错 | `now + timedelta(days=7)` |
| 比较日期时注意 naive vs aware | naive（无时区）和 aware（有时区）不能直接比较 | 同类型才能 `dt1 < dt2` |

### 实际应用示例

```python
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

# 获取 UTC 时间并转换为本地时区
utc_now = datetime.now(timezone.utc)
shanghai_now = utc_now.astimezone(ZoneInfo("Asia/Shanghai"))
print(shanghai_now.strftime("%Y-%m-%d %H:%M:%S %Z"))

# API 返回统一 ISO 格式
def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

# 解析前端日期字符串
def parse_date(s: str) -> datetime:
    try:
        return datetime.fromisoformat(s)
    except ValueError:
        return datetime.strptime(s, "%Y-%m-%d")
```

### 反模式：不要这样做

```python
# ❌ 用字符串比较日期
if "2024-03-15" > "2024-02-28":    # 字符串比较，恰好工作
    pass
if "2024-3-5" > "2024-02-28":      # 月份不补零，比较结果错误！

# ✅ 用 date 对象
from datetime import date
if date(2024, 3, 15) > date(2024, 2, 28):
    pass

# ❌ 用 datetime.utcnow()（Python 3.12 已弃用）
from datetime import datetime
dt = datetime.utcnow()     # 返回 naive datetime，无时区信息，易引发歧义

# ✅ 用 datetime.now(timezone.utc)
from datetime import datetime, timezone
dt = datetime.now(timezone.utc)

# ❌ 手动计算秒数表示时间差
days = (end - start).total_seconds() / 86400   # 夏令时当天 != 86400 秒

# ✅ 用 timedelta.days
days = (end - start).days
```

### 常见陷阱

| 陷阱 | 现象 | 解决方案 |
|------|------|---------|
| `strptime` 格式与字符串不匹配 | `ValueError: time data ... does not match` | 对照字符串逐字符检查格式代码 |
| `naive` 与 `aware` datetime 比较 | `TypeError: can't compare offset-naive and offset-aware datetimes` | 统一加时区或统一去掉时区 |
| `timedelta.seconds` vs `total_seconds()` | `timedelta(days=1).seconds` → `0`（非 86400） | 跨天差值用 `total_seconds()` |
| `datetime.utcnow()` 返回无时区对象 | 存入数据库后时区含义不明确 | 改用 `datetime.now(timezone.utc)` |
| `%m` 和 `%M` 混淆 | `%m` 是月份，`%M` 是分钟 | 记忆：大写 `M` = Minute（分钟） |

### 适用场景

| 场景 | 推荐方式 | 说明 |
|------|---------|------|
| 纯日期操作（生日/工期） | `date` + `timedelta` | 不需要时间部分 |
| 日志时间戳 | `datetime.now(timezone.utc)` | 统一 UTC，避免时区混乱 |
| 解析 ISO 格式字符串 | `datetime.fromisoformat()` | 比 `strptime` 简洁快速 |
| 跨时区应用 | `zoneinfo.ZoneInfo` | 正确处理夏令时 |
| 高精度计时（性能测量） | `time.perf_counter()` | `datetime` 精度不够 |

---

## 本章小结

```
┌──────────────────────────────────────────────────────────────┐
│                  datetime 模块 知识要点                       │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   三种基础类型：                                             │
│   date(y,m,d)          纯日期                                │
│   time(H,M,S)          纯时间                                │
│   datetime(y,m,d,H,M,S) 日期+时间                           │
│                                                              │
│   时间差：timedelta(days=7, hours=3)                         │
│   运算：dt + timedelta / dt1 - dt2 → timedelta              │
│                                                              │
│   格式化：strftime('%Y-%m-%d %H:%M:%S')  对象 → 字符串       │
│   解析：  strptime(s, fmt)              字符串 → 对象        │
│           fromisoformat(s)              ISO 格式专用（更快）  │
│                                                              │
│   时区：timezone.utc  /  ZoneInfo('Asia/Shanghai')          │
│   原则：存储 UTC，显示时转本地时区                            │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```