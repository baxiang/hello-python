# builtin_demo - 数据分析管道

Python 内置模块精讲示例项目，通过数据分析管道场景演示5章核心内置模块。

## 项目结构

```
builtin_demo/
├── app/
│   ├── core/
│   │   ├── containers.py    # ch01: collections容器
│   │   ├── iterators.py     # ch02: itertools迭代器
│   │   ├── functional.py    # ch03: functools函数式
│   │   ├── algorithms.py    # ch04: heapq/bisect算法
│   │   ├── weak_ref.py      # ch07: weakref弱引用
│   │   ├── pipeline.py      # 数据管道核心
│   │   └── data.py          # 数据模型
│   └── utils/
│       ├── helpers.py       # 辅助函数
│       └── transformers.py  # 数据转换器
├── tests/                   # pytest测试套件
└── sample_data/             # 示例数据
```

## 知识点覆盖

### ch01 collections - 容器
- Counter: 词频统计、most_common
- defaultdict: 分组聚合
- namedtuple: 数据记录、方法扩展
- deque: 双端队列、rotate
- OrderedDict: 有序字典、move_to_end
- ChainMap: 链式映射、配置合并

### ch02 itertools - 迭代器
- chain: 链式迭代
- combinations/permutations: 组合排列
- product: 笛卡尔积
- cycle/repeat: 无限迭代
- islice/takewhile/dropwhile: 条件切片
- accumulate: 累计计算
- zip_longest: 不等长合并

### ch03 functools - 函数式
- lru_cache: 缓存装饰器、cache_info/clear
- partial: 偏函数
- reduce: 归约操作
- wraps: 装饰器保留信息
- total_ordering: 自动比较
- singledispatch: 多类型处理
- cached_property: 延迟属性

### ch04 heapq/bisect - 算法
- heappush/heappop: 堆操作
- heapify/nsmallest/nlargest: Top N
- heapq.merge: 合并有序序列
- bisect_left/right: 二分查找
- bisect.insort: 有序插入
- PriorityQueue: 优先队列实现
- TaskScheduler: 任务调度

### ch07 weakref - 弱引用
- weakref.ref: 弱引用创建
- WeakValueDictionary: 弱引用值字典
- WeakKeyDictionary: 弱引用键字典
- weakref.finalize: 资源清理
- 循环引用解决演示

## 快速开始

```bash
cd 03-高级语法篇/04-内置模块精讲/builtin_demo
uv sync --group dev
uv run pytest           # 运行测试
uv run ruff check .     # 代码检查
```

## 使用示例

```python
from app import DataPipeline, create_record

# 创建数据管道
records = [create_record(1, "a", "cat1", 100, "2024-01-01")]
pipeline = DataPipeline.from_list(records)

# 链式操作
result = (
    pipeline.filter(lambda r: r.value > 50)
    .sort_by("value", reverse=True)
    .execute()
)
```

## 测试统计

- test_containers.py: 17 tests
- test_iterators.py: 22 tests
- test_functional.py: 16 tests
- test_algorithms.py: 15 tests
- test_weak_ref.py: 11 tests
- test_data.py: 12 tests

**总计: 81 tests**