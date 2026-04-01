# 迭代器与生成器示例

"""
Python 迭代器与生成器示例
包含：迭代器协议、生成器函数、生成器表达式
"""

from typing import Iterator, Generator


# 1. 迭代器协议
class Counter:
    """自定义迭代器"""
    
    def __init__(self, start: int, end: int):
        self.current = start
        self.end = end
    
    def __iter__(self) -> "Counter":
        return self
    
    def __next__(self) -> int:
        if self.current >= self.end:
            raise StopIteration
        value = self.current
        self.current += 1
        return value


# 2. 生成器函数
def countdown(n: int) -> Generator[int, None, None]:
    """倒计时生成器"""
    while n > 0:
        yield n
        n -= 1


def fibonacci_generator(n: int) -> Generator[int, None, None]:
    """斐波那契生成器"""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b


# 3. 生成器表达式
squares = (x ** 2 for x in range(10))


# 4. yield from
def chain(*iterables) -> Generator:
    """连接多个可迭代对象"""
    for iterable in iterables:
        yield from iterable


# 5. 无限生成器
def infinite_counter() -> Generator[int, None, None]:
    """无限计数器"""
    n = 0
    while True:
        yield n
        n += 1


# 6. 协程生成器
def accumulator() -> Generator[int, int, None]:
    """累加器协程"""
    total = 0
    while True:
        value = yield total
        if value is not None:
            total += value


# 7. 管道模式
def read_lines(filename: str) -> Generator[str, None, None]:
    """读取文件行"""
    # 模拟读取
    lines = ["hello world", "python programming", "generator example"]
    for line in lines:
        yield line


def filter_lines(lines: Generator[str, None, None], keyword: str) -> Generator[str, None, None]:
    """过滤行"""
    for line in lines:
        if keyword in line:
            yield line


def to_uppercase(lines: Generator[str, None, None]) -> Generator[str, None, None]:
    """转大写"""
    for line in lines:
        yield line.upper()


if __name__ == "__main__":
    print("=" * 40)
    print("迭代器与生成器示例")
    print("=" * 40)
    
    # 迭代器
    print("\n【自定义迭代器】")
    print(f"Counter(1, 5): {list(Counter(1, 5))}")
    
    # 生成器函数
    print("\n【生成器函数】")
    print(f"countdown(5): {list(countdown(5))}")
    print(f"fibonacci(10): {list(fibonacci_generator(10))}")
    
    # 生成器表达式
    print("\n【生成器表达式】")
    print(f"平方数: {list(squares)}")
    
    # yield from
    print("\n【yield from】")
    print(f"chain([1,2], [3,4], [5,6]): {list(chain([1, 2], [3, 4], [5, 6]))}")
    
    # 无限生成器
    print("\n【无限生成器】")
    counter = infinite_counter()
    print(f"前5个数: {[next(counter) for _ in range(5)]}")
    
    # 协程
    print("\n【协程生成器】")
    acc = accumulator()
    next(acc)  # 启动
    print(f"send(10): {acc.send(10)}")
    print(f"send(20): {acc.send(20)}")
    print(f"send(30): {acc.send(30)}")
    
    # 管道
    print("\n【管道模式】")
    lines = read_lines("example.txt")
    filtered = filter_lines(lines, "python")
    upper = to_uppercase(filtered)
    print(f"结果: {list(upper)}")