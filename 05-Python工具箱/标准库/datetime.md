# datetime 模块 - 日期时间

> Python 标准库 | 无需安装 | 适合初学者

---

## 第一部分：为什么需要 datetime 模块

### 1.1 手动处理日期的麻烦

#### 概念说明

想象一下，如果没有手表，你每次想知道现在几点，就得靠心算：从昨天中午12点算起，睡了多少小时，吃饭用了多少分钟……这不仅麻烦，还极易出错。

处理日期和时间也是同样的道理。在编程中，日期时间看似简单，实则暗藏陷阱：

- 每个月的天数不同（28、29、30、31 天）
- 闰年的二月有 29 天
- 跨年、跨月的计算容易出错
- 日期的字符串格式五花八门（"2024-01-15" vs "15/01/2024" vs "Jan 15, 2024"）
- 时区问题极其复杂

如果手动处理这些，代码会又长又容易出 bug。Python 的 `datetime` 模块就像一块精准的手表，帮你把所有复杂的日期时间运算都封装好了。

#### 示例代码

```python
# 不使用 datetime 模块：手动计算"今天加 30 天是几号"（容易出错）
year = 2024
month = 1
day = 15
day += 30  # 加 30 天
# 问题来了：1 月只有 31 天，加完之后 day = 45，这显然不对
# 还要判断是否超过当月天数，是否需要进位到下一月，下一月是几月...
# 代码会越来越复杂

# 使用 datetime 模块：一行搞定
from datetime import date, timedelta

today = date(2024, 1, 15)
future = today + timedelta(days=30)
print(future)  # 2024-02-14，自动处理月份进位
```

---

## 第二部分：datetime 模块的四个核心类

### 2.1 模块结构概览

#### 概念说明

`datetime` 模块（注意：模块名和类名都叫 `datetime`，初学者常常混淆）包含四个最常用的类，每个类负责不同的功能：

```
datetime 模块
┌─────────────────────────────────────────────────────────┐
│                    datetime 模块                         │
│                                                         │
│  ┌─────────────┐   ┌─────────────┐                     │
│  │    date     │   │    time     │                      │
│  │  日期类      │   │  时间类      │                      │
│  │ 年 / 月 / 日 │   │时/分/秒/微秒 │                      │
│  └──────┬──────┘   └──────┬──────┘                     │
│         │                 │                             │
│         └────────┬─────────┘                            │
│                  │                                      │
│          ┌───────▼───────┐                              │
│          │   datetime    │                              │
│          │  日期时间类     │                              │
│          │ 年月日时分秒微秒 │                              │
│          └───────────────┘                              │
│                                                         │
│  ┌──────────────────────────────────────┐               │
│  │            timedelta                 │               │
│  │           时间差/时间段类              │               │
│  │  天数 / 秒数 / 微秒数（用于加减运算）    │               │
│  └──────────────────────────────────────┘               │
└─────────────────────────────────────────────────────────┘
```

| 类名          | 用途         | 典型使用场景                |
|---------------|--------------|---------------------------|
| `date`        | 只有日期      | 生日、纪念日、截止日期        |
| `time`        | 只有时间      | 营业时间、闹钟时间            |
| `datetime`    | 日期 + 时间   | 日志时间戳、订单创建时间       |
| `timedelta`   | 时间段/时间差  | 计算两个日期之差、日期加减      |

#### 示例代码

```python
# 导入方式一：导入整个模块（需要用 datetime.datetime 访问类）
import datetime
d = datetime.date(2024, 1, 15)

# 导入方式二：按需导入（推荐，更简洁）
from datetime import date, time, datetime, timedelta

d = date(2024, 1, 15)         # 只有日期
t = time(14, 30, 0)           # 只有时间：14:30:00
dt = datetime(2024, 1, 15, 14, 30, 0)  # 日期 + 时间
delta = timedelta(days=7)     # 时间差：7 天

print(type(d))      # <class 'datetime.date'>
print(type(t))      # <class 'datetime.time'>
print(type(dt))     # <class 'datetime.datetime'>
print(type(delta))  # <class 'datetime.timedelta'>
```

---

## 第三部分：获取当前日期和时间

### 3.1 获取当前日期时间

#### 概念说明

最常用的操作之一：获取"现在"是什么时间。`datetime` 类提供了 `now()` 方法，`date` 类提供了 `today()` 方法。

类比：这就像按下手表上的"显示当前时间"按钮，系统会自动给你读取当前时刻。

#### 示例代码

```python
from datetime import date, datetime

# 获取今天的日期（只有年月日）
today = date.today()
print(today)               # 例如：2024-01-15
print(type(today))         # <class 'datetime.date'>

# 获取当前日期和时间
now = datetime.now()
print(now)                 # 例如：2024-01-15 14:30:25.123456
print(type(now))           # <class 'datetime.datetime'>

# 分别访问各个部分
print(now.year)            # 2024
print(now.month)           # 1
print(now.day)             # 15
print(now.hour)            # 14
print(now.minute)          # 30
print(now.second)          # 25
print(now.microsecond)     # 123456

# 获取今天是星期几（0=周一, 6=周日）
print(today.weekday())     # 0 表示周一
print(today.isoweekday())  # 1 表示周一（ISO 标准：1=周一, 7=周日）
```

### 3.2 date.today() 与 datetime.now() 的区别

#### 概念说明

```
date.today()            datetime.now()
┌─────────────┐        ┌──────────────────────────┐
│  2024-01-15 │        │  2024-01-15  14:30:25     │
│  只有日期    │        │  日期 + 时间               │
└─────────────┘        └──────────────────────────┘
```

如果你只需要知道"今天是几号"，用 `date.today()`；如果需要精确到时分秒，用 `datetime.now()`。

#### 示例代码

```python
from datetime import date, datetime

# 只需要日期
birthday_check = date.today()
print(f"今天是：{birthday_check}")

# 需要精确时间（如记录日志）
log_time = datetime.now()
print(f"日志记录时间：{log_time}")

# 从 datetime 对象中提取 date 部分
dt = datetime.now()
just_date = dt.date()    # 提取日期部分 -> date 对象
just_time = dt.time()    # 提取时间部分 -> time 对象
print(just_date)         # 2024-01-15
print(just_time)         # 14:30:25.123456
```

---

## 第四部分：创建特定日期时间对象

### 4.1 创建 date 对象

#### 概念说明

除了获取"当前"时间，你经常需要创建一个特定的日期，比如某个活动的截止日期或者用户的生日。

#### 示例代码

```python
from datetime import date

# 创建一个特定日期：date(年, 月, 日)
birthday = date(1990, 7, 20)
print(birthday)           # 1990-07-20

deadline = date(2024, 12, 31)
print(deadline)           # 2024-12-31

# 注意：月份和日期超出范围会报错
# date(2024, 13, 1)   # ValueError: month must be in 1..12
# date(2024, 2, 30)   # ValueError: day is out of range for month
```

### 4.2 创建 datetime 对象

#### 概念说明

`datetime` 对象需要至少提供年、月、日，时分秒可以省略（默认为 0）。

#### 示例代码

```python
from datetime import datetime

# 创建特定日期时间：datetime(年, 月, 日, 时, 分, 秒, 微秒)
# 时、分、秒、微秒 都是可选的，默认值为 0
dt1 = datetime(2024, 1, 15)
print(dt1)   # 2024-01-15 00:00:00

dt2 = datetime(2024, 1, 15, 14, 30)
print(dt2)   # 2024-01-15 14:30:00

dt3 = datetime(2024, 1, 15, 14, 30, 25)
print(dt3)   # 2024-01-15 14:30:25

dt4 = datetime(2024, 1, 15, 14, 30, 25, 500000)
print(dt4)   # 2024-01-15 14:30:25.500000
```

### 4.3 创建 time 对象

#### 示例代码

```python
from datetime import time

# 创建时间对象：time(时, 分, 秒, 微秒)
morning = time(8, 0, 0)
print(morning)    # 08:00:00

closing = time(17, 30)
print(closing)    # 17:30:00

# 访问属性
print(closing.hour)    # 17
print(closing.minute)  # 30
print(closing.second)  # 0
```

---

## 第五部分：格式化输出 strftime()

### 5.1 什么是 strftime

#### 概念说明

默认情况下，日期时间对象打印出来的格式是标准的 ISO 格式（如 `2024-01-15 14:30:25`）。但实际工作中，你可能需要不同的格式，比如：

- 中文格式：`2024年01月15日`
- 斜线格式：`15/01/2024`
- 12小时制：`02:30 PM`

`strftime()` 方法（str + f + time，即"字符串格式化时间"）就是用来将日期时间对象转换成你想要的任意字符串格式的。

类比：这就像把同一个数字用不同语言说出来——数字本身没变，只是表达形式不同。

```
datetime 对象  --strftime()-->  字符串
"2024-01-15"                   "2024年01月15日"
                               "15/01/2024"
                               "January 15, 2024"
                               ...任意格式
```

#### 示例代码

```python
from datetime import datetime

now = datetime(2024, 1, 15, 14, 30, 25)

# 基本格式化
print(now.strftime("%Y-%m-%d"))             # 2024-01-15
print(now.strftime("%Y年%m月%d日"))          # 2024年01月15日
print(now.strftime("%d/%m/%Y"))             # 15/01/2024
print(now.strftime("%Y-%m-%d %H:%M:%S"))    # 2024-01-15 14:30:25

# 12 小时制
print(now.strftime("%I:%M %p"))             # 02:30 PM

# 包含星期
print(now.strftime("%Y-%m-%d %A"))          # 2024-01-15 Monday
print(now.strftime("%Y年%m月%d日 %A"))       # 2024年01月15日 Monday

# 日志时间戳格式
print(now.strftime("[%Y-%m-%d %H:%M:%S]"))  # [2024-01-15 14:30:25]
```

### 5.2 常用格式代码速查表

#### 概念说明

`strftime` 使用以 `%` 开头的格式代码，每个代码代表日期时间的一个部分：

```
strftime / strptime 常用格式代码
┌────────┬────────────────────┬────────────────────────┐
│ 代码   │ 含义               │ 示例值                  │
├────────┼────────────────────┼────────────────────────┤
│  %Y    │ 4位年份            │ 2024                   │
│  %y    │ 2位年份            │ 24                     │
├────────┼────────────────────┼────────────────────────┤
│  %m    │ 月份（补零）        │ 01, 12                 │
│  %B    │ 月份全称（英文）    │ January, December      │
│  %b    │ 月份缩写（英文）    │ Jan, Dec               │
├────────┼────────────────────┼────────────────────────┤
│  %d    │ 日（补零）          │ 01, 31                 │
│  %j    │ 一年中的第几天      │ 001, 365               │
├────────┼────────────────────┼────────────────────────┤
│  %H    │ 24小时制小时（补零）│ 00, 23                 │
│  %I    │ 12小时制小时（补零）│ 01, 12                 │
│  %p    │ AM 或 PM           │ AM, PM                 │
├────────┼────────────────────┼────────────────────────┤
│  %M    │ 分钟（补零）        │ 00, 59                 │
│  %S    │ 秒（补零）          │ 00, 59                 │
│  %f    │ 微秒（6位）         │ 000000, 999999         │
├────────┼────────────────────┼────────────────────────┤
│  %A    │ 星期全称（英文）    │ Monday, Sunday         │
│  %a    │ 星期缩写（英文）    │ Mon, Sun               │
│  %w    │ 星期数字            │ 0(周日)..6(周六)        │
├────────┼────────────────────┼────────────────────────┤
│  %W    │ 一年中第几周（周一起）│ 00, 53               │
│  %U    │ 一年中第几周（周日起）│ 00, 53               │
├────────┼────────────────────┼────────────────────────┤
│  %%    │ 百分号字面量        │ %                      │
└────────┴────────────────────┴────────────────────────┘
```

#### 示例代码

```python
from datetime import datetime

dt = datetime(2024, 1, 15, 9, 5, 3)

# 测试各种格式代码
print(dt.strftime("%Y"))    # 2024
print(dt.strftime("%y"))    # 24
print(dt.strftime("%m"))    # 01
print(dt.strftime("%B"))    # January
print(dt.strftime("%b"))    # Jan
print(dt.strftime("%d"))    # 15
print(dt.strftime("%H"))    # 09（24小时制）
print(dt.strftime("%I"))    # 09（12小时制）
print(dt.strftime("%p"))    # AM
print(dt.strftime("%M"))    # 05
print(dt.strftime("%S"))    # 03
print(dt.strftime("%A"))    # Monday
print(dt.strftime("%a"))    # Mon
print(dt.strftime("%w"))    # 1（0=周日, 1=周一）
print(dt.strftime("%j"))    # 015（一年中第15天）
```

---

## 第六部分：解析字符串 strptime()

### 6.1 什么是 strptime

#### 概念说明

`strftime` 是把日期对象变成字符串，`strptime` 则是反过来：把字符串解析成日期对象。

类比：`strftime` 是"把日期翻译成文字"，`strptime` 是"把文字翻译回日期"。

```
strftime：datetime 对象  -->  字符串
strptime：字符串         -->  datetime 对象
```

记忆技巧：
- `strftime` = str **f**ormat time（格式化时间为字符串）
- `strptime` = str **p**arse time（解析字符串为时间）

使用 `strptime` 时，你需要告诉 Python 字符串是什么格式——这个格式要与实际字符串完全匹配，否则会报错。

#### 示例代码

```python
from datetime import datetime

# 基本用法：datetime.strptime(字符串, 格式)
date_str = "2024-01-15"
dt = datetime.strptime(date_str, "%Y-%m-%d")
print(dt)           # 2024-01-15 00:00:00
print(type(dt))     # <class 'datetime.datetime'>

# 包含时间的字符串
datetime_str = "2024-01-15 14:30:25"
dt2 = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
print(dt2)          # 2024-01-15 14:30:25

# 不同格式的日期字符串
date1 = datetime.strptime("15/01/2024", "%d/%m/%Y")
date2 = datetime.strptime("January 15, 2024", "%B %d, %Y")
date3 = datetime.strptime("2024年01月15日", "%Y年%m月%d日")

print(date1)  # 2024-01-15 00:00:00
print(date2)  # 2024-01-15 00:00:00
print(date3)  # 2024-01-15 00:00:00
```

### 6.2 常见解析错误

#### 概念说明

使用 `strptime` 时，格式字符串必须和输入字符串精确匹配，哪怕多一个空格或少一个字符都会报 `ValueError`。

#### 示例代码

```python
from datetime import datetime

# 错误示例：格式不匹配
try:
    # 字符串是 "2024/01/15"，但格式写成了 "%Y-%m-%d"（用的是连字符）
    dt = datetime.strptime("2024/01/15", "%Y-%m-%d")
except ValueError as e:
    print(f"解析失败：{e}")
    # time data '2024/01/15' does not match format '%Y-%m-%d'

# 正确写法：格式与字符串完全一致
dt = datetime.strptime("2024/01/15", "%Y/%m/%d")
print(dt)  # 2024-01-15 00:00:00

# 实用技巧：用 try-except 处理格式不确定的情况
def safe_parse_date(date_str):
    """尝试多种格式解析日期字符串"""
    formats = [
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d/%m/%Y",
        "%Y年%m月%d日",
        "%B %d, %Y",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"无法解析日期字符串：{date_str}")

print(safe_parse_date("2024-01-15"))       # 2024-01-15 00:00:00
print(safe_parse_date("2024年01月15日"))    # 2024-01-15 00:00:00
```

---

## 第七部分：时间差计算 timedelta

### 7.1 timedelta 的概念

#### 概念说明

`timedelta` 表示一段时间的长度（时间差），而不是某个具体的时间点。它可以是"3天"、"2小时30分钟"、"1周"等。

类比：如果说 `datetime` 是日历上的某个具体日期，那么 `timedelta` 就是"两个日期之间的间隔"或者"日期移动的步长"。

```
时间轴示意图

今天         + 7天             = 下周
┌───────────────────────────────────┐
│  2024-01-15  +  timedelta(days=7) │
│               = 2024-01-22        │
└───────────────────────────────────┘

timedelta 参数：
┌──────────────────────────────────────────┐
│  timedelta(                              │
│      days=0,         # 天数              │
│      seconds=0,      # 秒数              │
│      microseconds=0, # 微秒              │
│      milliseconds=0, # 毫秒（自动转秒）   │
│      minutes=0,      # 分钟（自动转秒）   │
│      hours=0,        # 小时（自动转秒）   │
│      weeks=0         # 周数（自动转天）   │
│  )                                       │
└──────────────────────────────────────────┘
```

#### 示例代码

```python
from datetime import timedelta

# 创建 timedelta 对象
one_week = timedelta(weeks=1)
three_days = timedelta(days=3)
two_hours = timedelta(hours=2)
ninety_minutes = timedelta(minutes=90)
mixed = timedelta(days=1, hours=2, minutes=30)

print(one_week)       # 7 days, 0:00:00
print(three_days)     # 3 days, 0:00:00
print(two_hours)      # 0:00:00  (注意：小时不满一天时显示为 H:MM:SS)
print(ninety_minutes) # 1:30:00
print(mixed)          # 1 day, 2:30:00

# timedelta 的内部存储：只用天、秒、微秒三个单位
td = timedelta(hours=25, minutes=30)
print(td.days)         # 1（25小时 = 1天1小时）
print(td.seconds)      # 5400（1小时30分 = 5400秒）
print(td.total_seconds())  # 91800.0（总秒数）
```

### 7.2 日期加减运算

#### 概念说明

`timedelta` 最常见的用途是对日期进行加减。日期加上时间差得到新的日期，两个日期相减得到时间差。

#### 示例代码

```python
from datetime import date, datetime, timedelta

today = date(2024, 1, 15)

# 日期加减
tomorrow = today + timedelta(days=1)
yesterday = today - timedelta(days=1)
next_week = today + timedelta(weeks=1)
last_month_approx = today - timedelta(days=30)

print(f"今天：{today}")
print(f"明天：{tomorrow}")
print(f"昨天：{yesterday}")
print(f"下周今日：{next_week}")
print(f"约一个月前：{last_month_approx}")

# datetime 对象同样支持加减
now = datetime(2024, 1, 15, 14, 30, 0)
two_hours_later = now + timedelta(hours=2)
half_hour_ago = now - timedelta(minutes=30)

print(f"当前时间：{now}")
print(f"2小时后：{two_hours_later}")
print(f"30分钟前：{half_hour_ago}")

# timedelta 也可以相互运算
three_days = timedelta(days=3)
five_days = timedelta(days=5)
eight_days = three_days + five_days
two_days = five_days - three_days

print(f"3天 + 5天 = {eight_days}")    # 8 days, 0:00:00
print(f"5天 - 3天 = {two_days}")      # 2 days, 0:00:00
```

---

## 第八部分：计算两个日期的差值

### 8.1 日期相减

#### 概念说明

两个 `date` 或 `datetime` 对象直接相减，会得到一个 `timedelta` 对象，表示它们之间的时间差。

#### 示例代码

```python
from datetime import date, datetime

# 两个日期相减
start = date(2024, 1, 1)
end = date(2024, 3, 15)
diff = end - start

print(diff)              # 74 days, 0:00:00
print(diff.days)         # 74
print(type(diff))        # <class 'datetime.timedelta'>

# 注意：早的日期减去晚的日期会得到负数
negative_diff = start - end
print(negative_diff)     # -74 days, 0:00:00
print(negative_diff.days)  # -74

# 使用 abs() 取绝对值
print(abs(negative_diff).days)  # 74

# datetime 对象相减（包含时间精度）
dt1 = datetime(2024, 1, 15, 9, 0, 0)
dt2 = datetime(2024, 1, 15, 14, 30, 25)
diff2 = dt2 - dt1

print(diff2)                    # 5:30:25
print(diff2.seconds)            # 19825（秒数）
print(diff2.total_seconds())    # 19825.0

# 计算距离某个日期还有多少天
deadline = date(2024, 12, 31)
today = date(2024, 1, 15)
days_left = (deadline - today).days
print(f"距离年底还有 {days_left} 天")
```

---

## 第九部分：常用属性和方法

### 9.1 属性总览

#### 概念说明

`date`、`time`、`datetime` 对象提供了丰富的属性，让你可以方便地访问日期时间的各个组成部分。

```
datetime 对象属性一览

                  2024  -  01  -  15    14  :  30  :  25
                  ┌───┐    ┌──┐   ┌──┐  ┌──┐   ┌──┐   ┌──┐
                  │   │    │  │   │  │  │  │   │  │   │  │
                 year  month  day  hour  minute second
```

#### 示例代码

```python
from datetime import date, datetime

dt = datetime(2024, 1, 15, 14, 30, 25, 500000)

# 日期部分属性
print(dt.year)         # 2024
print(dt.month)        # 1
print(dt.day)          # 15

# 时间部分属性
print(dt.hour)         # 14
print(dt.minute)       # 30
print(dt.second)       # 25
print(dt.microsecond)  # 500000

# 星期相关
print(dt.weekday())    # 0 表示周一（0=周一, 6=周日）
print(dt.isoweekday()) # 1 表示周一（1=周一, 7=周日）

# 星期名称（需要格式化）
days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
print(days[dt.weekday()])  # 周一

# 对应的 ISO 格式字符串
print(dt.isoformat())      # 2024-01-15T14:30:25.500000

# 提取日期/时间部分
print(dt.date())  # 2024-01-15（返回 date 对象）
print(dt.time())  # 14:30:25.500000（返回 time 对象）
```

### 9.2 replace() 方法

#### 概念说明

日期时间对象是不可变的（immutable），不能直接修改。但你可以用 `replace()` 方法创建一个修改了某些字段的新对象。

#### 示例代码

```python
from datetime import datetime

dt = datetime(2024, 1, 15, 14, 30, 25)

# replace() 返回新对象，原对象不变
dt_new_year = dt.replace(year=2025)
dt_midnight = dt.replace(hour=0, minute=0, second=0)
dt_first_of_month = dt.replace(day=1)

print(dt)               # 2024-01-15 14:30:25（原对象未变）
print(dt_new_year)      # 2025-01-15 14:30:25
print(dt_midnight)      # 2024-01-15 00:00:00
print(dt_first_of_month) # 2024-01-01 14:30:25
```

---

## 第十部分：综合实例

### 10.1 计算年龄函数

#### 概念说明

计算年龄时，需要注意今年的生日是否已经过了——如果还没到生日，年龄应该是"今年 - 出生年 - 1"。

#### 示例代码

```python
from datetime import date

def calculate_age(birth_date):
    """
    根据生日计算当前年龄。
    
    参数：
        birth_date: date 对象或 (年, 月, 日) 元组
    返回：
        整数年龄
    """
    if isinstance(birth_date, tuple):
        birth_date = date(*birth_date)
    
    today = date.today()
    
    # 计算年份差
    age = today.year - birth_date.year
    
    # 判断今年的生日是否还没到
    # 如果今天的月日 < 生日的月日，说明今年生日还没过，年龄要减 1
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    
    return age

# 测试
birth = date(1990, 7, 20)
print(f"年龄：{calculate_age(birth)} 岁")

# 也可以传入元组
print(f"年龄：{calculate_age((2000, 12, 25))} 岁")

# 验证边界情况
from datetime import date as d
# 假设今天是 2024-01-15
test_birthday_today = date(1990, 1, 15)   # 今天生日
test_birthday_tmr = date(1990, 1, 16)     # 明天生日
test_birthday_ytd = date(1990, 1, 14)     # 昨天生日

print(calculate_age(test_birthday_today))  # 今天生日：34
print(calculate_age(test_birthday_tmr))    # 明天生日：33（还没到）
print(calculate_age(test_birthday_ytd))    # 昨天生日：34（已过）
```

### 10.2 倒计时程序

#### 示例代码

```python
from datetime import date, datetime

def countdown(target_date, event_name="目标日期"):
    """
    计算距离目标日期还有多少天。
    
    参数：
        target_date: date 对象
        event_name:  事件名称（字符串）
    """
    today = date.today()
    diff = target_date - today
    days = diff.days
    
    if days > 0:
        print(f"距离「{event_name}」还有 {days} 天")
    elif days == 0:
        print(f"今天就是「{event_name}」！")
    else:
        print(f"「{event_name}」已经过去 {abs(days)} 天了")

# 示例
new_year = date(2025, 1, 1)
countdown(new_year, "2025年元旦")

spring_festival = date(2025, 1, 29)
countdown(spring_festival, "2025年春节")

past_event = date(2024, 1, 1)
countdown(past_event, "2024年元旦")


def countdown_with_time(target_datetime, event_name="目标时间"):
    """精确到秒的倒计时"""
    now = datetime.now()
    diff = target_datetime - now
    total_seconds = int(diff.total_seconds())
    
    if total_seconds <= 0:
        print(f"「{event_name}」已经过去了！")
        return
    
    days = diff.days
    remaining_seconds = diff.seconds
    hours = remaining_seconds // 3600
    minutes = (remaining_seconds % 3600) // 60
    seconds = remaining_seconds % 60
    
    print(f"距离「{event_name}」还有：{days}天 {hours}小时 {minutes}分 {seconds}秒")

# 示例
target = datetime(2025, 1, 1, 0, 0, 0)
countdown_with_time(target, "2025年元旦零点")
```

### 10.3 判断是否是闰年

#### 概念说明

闰年的规则：能被 4 整除，但不能被 100 整除；或者能被 400 整除。

```
闰年判断逻辑
┌─────────────────────────────────────────┐
│  年份能被 4 整除？                        │
│       ├── 否 --> 平年                    │
│       └── 是                            │
│             年份能被 100 整除？           │
│                  ├── 否 --> 闰年         │
│                  └── 是                 │
│                        年份能被 400 整除？│
│                             ├── 是 --> 闰年│
│                             └── 否 --> 平年│
└─────────────────────────────────────────┘
```

#### 示例代码

```python
import calendar
from datetime import date

# 方法一：使用 calendar 模块（推荐）
def is_leap_year_v1(year):
    return calendar.isleap(year)

# 方法二：手动实现逻辑
def is_leap_year_v2(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

# 方法三：利用 2 月天数来判断（利用 datetime 模块）
def is_leap_year_v3(year):
    # 闰年的 2 月有 29 天
    return date(year, 3, 1) - date(year, 2, 1) == __import__('datetime').timedelta(days=29)

# 测试
test_years = [1900, 2000, 2024, 2025, 2100]
for y in test_years:
    result = is_leap_year_v1(y)
    print(f"{y} 年：{'闰年' if result else '平年'}")
# 1900 年：平年（能被100整除但不能被400整除）
# 2000 年：闰年（能被400整除）
# 2024 年：闰年（能被4整除，不能被100整除）
# 2025 年：平年
# 2100 年：平年（能被100整除但不能被400整除）
```

### 10.4 工作日计算（跳过周末）

#### 概念说明

在商业场景中，经常需要计算"N 个工作日后"是哪天——需要跳过周六和周日。

#### 示例代码

```python
from datetime import date, timedelta

def add_business_days(start_date, n):
    """
    从 start_date 开始，向后推 n 个工作日（跳过周末）。
    
    参数：
        start_date: date 对象，起始日期
        n: 整数，工作日数量（可以为负数，向前推）
    返回：
        date 对象
    """
    current = start_date
    days_added = 0
    step = 1 if n >= 0 else -1
    
    while days_added < abs(n):
        current += timedelta(days=step)
        # weekday() 返回 0-6，0=周一, 5=周六, 6=周日
        if current.weekday() < 5:  # 0-4 是工作日
            days_added += 1
    
    return current

def count_business_days(start_date, end_date):
    """
    计算两个日期之间的工作日数量（不含起始日，含结束日）。
    """
    count = 0
    current = start_date
    while current < end_date:
        current += timedelta(days=1)
        if current.weekday() < 5:
            count += 1
    return count

# 测试
start = date(2024, 1, 15)  # 周一
print(f"起始日期：{start}（{['周一','周二','周三','周四','周五','周六','周日'][start.weekday()]}）")

result = add_business_days(start, 5)
print(f"5个工作日后：{result}（{['周一','周二','周三','周四','周五','周六','周日'][result.weekday()]}）")

result2 = add_business_days(start, 10)
print(f"10个工作日后：{result2}")

# 计算工作日数量
d1 = date(2024, 1, 1)
d2 = date(2024, 1, 31)
biz_days = count_business_days(d1, d2)
print(f"2024年1月共有 {biz_days} 个工作日")
```

### 10.5 日志时间戳格式化

#### 示例代码

```python
from datetime import datetime

class Logger:
    """带时间戳的简单日志记录器"""
    
    LEVELS = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3}
    
    def __init__(self, min_level="INFO"):
        self.min_level = min_level
    
    def _format_timestamp(self):
        """返回当前时间戳字符串"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def log(self, level, message):
        if self.LEVELS.get(level, 0) >= self.LEVELS.get(self.min_level, 0):
            timestamp = self._format_timestamp()
            print(f"[{timestamp}] [{level}] {message}")
    
    def debug(self, msg):   self.log("DEBUG", msg)
    def info(self, msg):    self.log("INFO", msg)
    def warning(self, msg): self.log("WARNING", msg)
    def error(self, msg):   self.log("ERROR", msg)

# 使用示例
logger = Logger(min_level="INFO")
logger.info("程序启动")
logger.debug("这条不会显示（低于 INFO 级别）")
logger.warning("磁盘空间不足")
logger.error("无法连接数据库")

# 输出示例：
# [2024-01-15 14:30:25] [INFO] 程序启动
# [2024-01-15 14:30:25] [WARNING] 磁盘空间不足
# [2024-01-15 14:30:25] [ERROR] 无法连接数据库


# 生成带日期的日志文件名
def get_log_filename(prefix="app"):
    """生成按日期命名的日志文件名"""
    today = datetime.now().strftime("%Y%m%d")
    return f"{prefix}_{today}.log"

print(get_log_filename())        # app_20240115.log
print(get_log_filename("error")) # error_20240115.log


# 解析日志中的时间戳
def parse_log_timestamp(log_line):
    """从日志行中提取时间戳"""
    # 假设格式：[2024-01-15 14:30:25] [INFO] 消息内容
    try:
        timestamp_str = log_line[1:20]  # 提取 "2024-01-15 14:30:25"
        return datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    except (ValueError, IndexError):
        return None

log_line = "[2024-01-15 14:30:25] [INFO] 用户登录"
ts = parse_log_timestamp(log_line)
if ts:
    print(f"日志时间：{ts}")
    print(f"格式化：{ts.strftime('%Y年%m月%d日 %H:%M')}")
```

---

## 第十一部分：strftime 格式代码完整速查表

### 11.1 完整格式代码参考

#### 概念说明

以下是 `strftime` / `strptime` 支持的所有常用格式代码，按类别整理。

```
完整格式代码速查表
┌──────────────────────────────────────────────────────────────┐
│                       日期相关                                │
├────────┬──────────────────────────┬──────────────────────────┤
│ 代码   │ 描述                     │ 示例                     │
├────────┼──────────────────────────┼──────────────────────────┤
│  %Y    │ 四位年份                 │ 2024                     │
│  %y    │ 两位年份                 │ 24                       │
│  %m    │ 月份，补零               │ 01 ~ 12                  │
│  %d    │ 日，补零                 │ 01 ~ 31                  │
│  %B    │ 月份英文全名             │ January                  │
│  %b    │ 月份英文缩写             │ Jan                      │
│  %A    │ 星期英文全名             │ Monday                   │
│  %a    │ 星期英文缩写             │ Mon                      │
│  %w    │ 星期数字(0=周日)         │ 0 ~ 6                    │
│  %j    │ 一年中的天数             │ 001 ~ 366                │
│  %U    │ 一年中的周数(周日起)     │ 00 ~ 53                  │
│  %W    │ 一年中的周数(周一起)     │ 00 ~ 53                  │
├────────┴──────────────────────────┴──────────────────────────┤
│                       时间相关                                │
├────────┬──────────────────────────┬──────────────────────────┤
│  %H    │ 24小时制小时，补零       │ 00 ~ 23                  │
│  %I    │ 12小时制小时，补零       │ 01 ~ 12                  │
│  %p    │ AM 或 PM                 │ AM / PM                  │
│  %M    │ 分钟，补零               │ 00 ~ 59                  │
│  %S    │ 秒，补零                 │ 00 ~ 59                  │
│  %f    │ 微秒，6位，补零          │ 000000 ~ 999999          │
├────────┴──────────────────────────┴──────────────────────────┤
│                       组合格式                                │
├────────┬──────────────────────────┬──────────────────────────┤
│  %c    │ 本地日期时间表示         │ Mon Jan 15 14:30:25 2024 │
│  %x    │ 本地日期表示             │ 01/15/24                 │
│  %X    │ 本地时间表示             │ 14:30:25                 │
│  %z    │ UTC 时区偏移             │ +0800                    │
│  %Z    │ 时区名称                 │ CST                      │
├────────┴──────────────────────────┴──────────────────────────┤
│                       特殊                                    │
├────────┬──────────────────────────┬──────────────────────────┤
│  %%    │ 百分号字面量             │ %                        │
└────────┴──────────────────────────┴──────────────────────────┘
```

#### 示例代码

```python
from datetime import datetime

dt = datetime(2024, 1, 15, 14, 30, 25)

# 常用组合格式示例
formats = {
    "ISO 标准":         "%Y-%m-%dT%H:%M:%S",
    "中文日期":         "%Y年%m月%d日",
    "中文日期时间":     "%Y年%m月%d日 %H时%M分%S秒",
    "中文含星期":       "%Y年%m月%d日 %A",
    "日志格式":         "[%Y-%m-%d %H:%M:%S]",
    "文件名安全格式":   "%Y%m%d_%H%M%S",
    "斜线日期":         "%d/%m/%Y",
    "点号日期":         "%d.%m.%Y",
    "美式日期":         "%m/%d/%Y",
    "12小时制":         "%I:%M:%S %p",
    "月日年":           "%B %d, %Y",
}

for name, fmt in formats.items():
    print(f"{name:<16}: {dt.strftime(fmt)}")
```

---

## 第十二部分：常见错误和注意事项

### 12.1 模块名与类名的混淆

#### 概念说明

`datetime` 既是模块名，也是其中一个类名，初学者很容易混淆。

#### 示例代码

```python
# 容易引起混淆的导入方式
import datetime

# 访问 datetime 类：需要写两个 datetime
now = datetime.datetime.now()
today = datetime.date.today()
delta = datetime.timedelta(days=7)

# 更清晰的导入方式（推荐）
from datetime import datetime, date, timedelta

now = datetime.now()     # 直接使用类名
today = date.today()
delta = timedelta(days=7)
```

### 12.2 date 和 datetime 不能直接比较

#### 示例代码

```python
from datetime import date, datetime

today_date = date(2024, 1, 15)
today_datetime = datetime(2024, 1, 15)

# 以下操作会报 TypeError
try:
    result = today_date == today_datetime
except TypeError as e:
    print(f"错误：{e}")
    # can't compare datetime.datetime to datetime.date

# 正确做法：统一类型后再比较
# 方法一：把 date 转为 datetime
today_dt = datetime(today_date.year, today_date.month, today_date.day)
print(today_dt == today_datetime)  # True

# 方法二：从 datetime 中提取 date 部分
print(today_date == today_datetime.date())  # True
```

### 12.3 timedelta 不支持月和年

#### 概念说明

`timedelta` 只支持天、秒、微秒（以及可以换算成这些单位的周、小时、分钟、毫秒）。它不支持月和年，因为月和年的天数不固定。

#### 示例代码

```python
from datetime import timedelta

# timedelta 不支持 months 和 years 参数
# timedelta(months=1)  # TypeError: 不存在 months 参数
# timedelta(years=1)   # TypeError: 不存在 years 参数

# 需要加减月/年，用 replace() 方法手动处理
from datetime import date

def add_months(d, months):
    """向日期加上指定月数（近似处理，月末可能有问题）"""
    month = d.month - 1 + months
    year = d.year + month // 12
    month = month % 12 + 1
    # 处理月末日期超出的情况（如 1月31日加1个月）
    import calendar
    max_day = calendar.monthrange(year, month)[1]
    day = min(d.day, max_day)
    return d.replace(year=year, month=month, day=day)

def add_years(d, years):
    """向日期加上指定年数"""
    try:
        return d.replace(year=d.year + years)
    except ValueError:
        # 处理 2月29日加年份的情况
        return d.replace(year=d.year + years, day=28)

# 测试
d = date(2024, 1, 31)
print(add_months(d, 1))   # 2024-02-29（2024是闰年）
print(add_months(d, 2))   # 2024-03-31

d2 = date(2024, 2, 29)  # 闰年2月29日
print(add_years(d2, 1))  # 2025-02-28（2025年无2月29日）
```

### 12.4 字符串解析的格式必须精确匹配

#### 示例代码

```python
from datetime import datetime

# 常见错误：格式与字符串不完全匹配
error_cases = [
    ("2024-1-5",   "%Y-%m-%d"),   # 月和日没有补零
    ("2024-01-15 ", "%Y-%m-%d"),  # 末尾多了空格
    ("01/15/2024",  "%Y/%m/%d"),  # 分隔符不匹配
]

for s, fmt in error_cases:
    try:
        result = datetime.strptime(s, fmt)
        print(f"成功: {result}")
    except ValueError as e:
        print(f"失败 ('{s}', '{fmt}'): {e}")

# 正确写法
correct_cases = [
    ("2024-1-5",   "%Y-%-m-%-d"),  # Linux 上可用，Mac/Windows 可能不支持
    ("2024-01-15", "%Y-%m-%d"),    # 标准写法，月日补零
]
# 最稳妥：先确定输入格式，写对应的格式字符串
```

### 12.5 小结：常见错误一览

```
常见错误总结
┌───────────────────────────────────────────────────────────────┐
│  错误类型          │ 原因               │ 解决方法             │
├───────────────────┼────────────────────┼──────────────────────┤
│ NameError         │ 没有正确导入        │ from datetime import │
│                   │                    │   date, datetime...  │
├───────────────────┼────────────────────┼──────────────────────┤
│ TypeError         │ date 和 datetime   │ 统一类型后再比较      │
│ (比较时)          │ 混用比较            │                      │
├───────────────────┼────────────────────┼──────────────────────┤
│ ValueError        │ strptime 格式不    │ 检查格式字符串是否    │
│ (解析时)          │ 匹配输入字符串      │ 与输入完全一致        │
├───────────────────┼────────────────────┼──────────────────────┤
│ ValueError        │ 日期值不合法        │ 检查月份(1-12)、      │
│ (创建时)          │ 如月份 13、日 32    │ 日期是否在该月范围内  │
├───────────────────┼────────────────────┼──────────────────────┤
│ TypeError         │ timedelta 使用了   │ 用 replace() 代替     │
│ (timedelta时)     │ months/years 参数  │ 手动处理月/年加减     │
└───────────────────┴────────────────────┴──────────────────────┘
```

---

## 附录：知识点总结

```
datetime 模块核心知识点速查
┌─────────────────────────────────────────────────────────────────┐
│  操作                 │ 代码示例                                 │
├───────────────────────┼──────────────────────────────────────────┤
│ 获取今天日期           │ date.today()                            │
│ 获取当前时间           │ datetime.now()                          │
│ 创建日期对象           │ date(2024, 1, 15)                       │
│ 创建日期时间对象        │ datetime(2024, 1, 15, 14, 30)          │
├───────────────────────┼──────────────────────────────────────────┤
│ 格式化为字符串         │ dt.strftime("%Y-%m-%d")                 │
│ 从字符串解析           │ datetime.strptime(s, "%Y-%m-%d")        │
├───────────────────────┼──────────────────────────────────────────┤
│ 加减天数               │ date + timedelta(days=7)               │
│ 加减小时               │ datetime + timedelta(hours=2)          │
│ 计算日期差             │ (date2 - date1).days                   │
├───────────────────────┼──────────────────────────────────────────┤
│ 访问年月日             │ dt.year / dt.month / dt.day            │
│ 访问时分秒             │ dt.hour / dt.minute / dt.second        │
│ 获取星期               │ dt.weekday()  # 0=周一                 │
│ 修改某个字段           │ dt.replace(year=2025)                  │
├───────────────────────┼──────────────────────────────────────────┤
│ 提取日期部分           │ datetime_obj.date()                    │
│ 提取时间部分           │ datetime_obj.time()                    │
│ 转为 ISO 字符串        │ dt.isoformat()                         │
└───────────────────────┴──────────────────────────────────────────┘
```

---

[返回索引](../README.md) | [返回 11-模块与包](../11-模块与包.md)
