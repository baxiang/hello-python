"""迭代器与生成器示例 — 覆盖第01-06章

场景：日志流处理系统

章节对应：
  ch01  for 循环原理、iter() / next()；可迭代对象 vs 迭代器区别
  ch02  自定义迭代器：__iter__ / __next__ / StopIteration
        可迭代类（__iter__ 返回独立迭代器对象，支持多次迭代）
  ch03  生成器函数（yield）；生成器表达式
  ch04  send() 双向通信；throw() 注入异常；yield from 委托
  ch05  itertools：islice / chain / takewhile / groupby / count
  ch06  异步生成器（async def + yield）
"""

from __future__ import annotations

import itertools
from typing import Generator, Iterator


# ---------------------------------------------------------------------------
# ch01: 迭代基础 — iter() / next() / 可迭代对象
# ---------------------------------------------------------------------------

def manual_iterate(iterable: object) -> list:
    """用 iter()/next() 手动迭代（ch01：迭代协议底层）"""
    it = iter(iterable)      # type: ignore[call-overload]
    result = []
    while True:
        try:
            result.append(next(it))
        except StopIteration:
            break
    return result


# ---------------------------------------------------------------------------
# ch02: 自定义迭代器
# ---------------------------------------------------------------------------

class LogEntry:
    """单条日志"""

    def __init__(self, level: str, message: str) -> None:
        self.level = level
        self.message = message

    def __repr__(self) -> str:
        return f"LogEntry({self.level!r}, {self.message!r})"


class LogIterator:
    """日志迭代器（ch02：__iter__ + __next__ + StopIteration）

    迭代器本身：__iter__ 返回 self（不可重置，只能遍历一次）。
    """

    def __init__(self, entries: list[LogEntry]) -> None:
        self._entries = entries
        self._index: int = 0

    def __iter__(self) -> "LogIterator":
        return self

    def __next__(self) -> LogEntry:
        if self._index >= len(self._entries):
            raise StopIteration
        entry = self._entries[self._index]
        self._index += 1
        return entry


class LogCollection:
    """日志集合（ch02：可迭代类——每次 iter() 返回新的独立迭代器，支持多次遍历）"""

    def __init__(self, entries: list[LogEntry]) -> None:
        self._entries = entries

    def __iter__(self) -> LogIterator:
        """每次调用都新建一个 LogIterator，互不干扰"""
        return LogIterator(list(self._entries))

    def __len__(self) -> int:
        return len(self._entries)

    def add(self, entry: LogEntry) -> None:
        self._entries.append(entry)


# ---------------------------------------------------------------------------
# ch03: 生成器基础 — yield / 生成器表达式
# ---------------------------------------------------------------------------

def log_generator(entries: list[LogEntry]) -> Generator[LogEntry, None, None]:
    """逐条产出日志（ch03：生成器函数，惰性求值）"""
    for entry in entries:
        yield entry


def filter_by_level(
    entries: list[LogEntry], level: str
) -> Generator[LogEntry, None, None]:
    """只产出指定级别的日志（ch03：带条件的生成器）"""
    for entry in entries:
        if entry.level == level:
            yield entry


def fibonacci() -> Generator[int, None, None]:
    """无限斐波那契生成器（ch03：无限序列 + 生成器表达式配合 itertools.islice 截取）"""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def message_lengths(entries: list[LogEntry]) -> list[int]:
    """生成器表达式：惰性计算消息长度（ch03：genexpr）"""
    return list(len(e.message) for e in entries)


# ---------------------------------------------------------------------------
# ch04: 生成器高级特性 — send / throw / yield from
# ---------------------------------------------------------------------------

def log_accumulator() -> Generator[int, LogEntry | None, str]:
    """双向生成器（ch04：send() 向生成器传值）

    协议：
        gen = log_accumulator()
        next(gen)           → 启动，产出 0（当前计数）
        gen.send(entry)     → 传入一条日志，产出新计数
        gen.close()         → 结束
    """
    count = 0
    while True:
        entry = yield count
        if entry is not None:
            count += 1


def safe_log_reader(
    entries: list[LogEntry],
) -> Generator[LogEntry | str, type[Exception] | None, None]:
    """支持 throw() 注入异常（ch04：throw() 向生成器注入异常）

    gen.throw(ValueError) → 生成器捕获后产出错误消息，继续运行
    """
    for entry in entries:
        try:
            yield entry
        except ValueError:
            yield f"[跳过无效条目]"


def merge_logs(
    *sources: list[LogEntry],
) -> Generator[LogEntry, None, None]:
    """合并多个日志源（ch04：yield from 委托子生成器）"""
    for source in sources:
        yield from log_generator(source)


# ---------------------------------------------------------------------------
# ch05: itertools 模块
# ---------------------------------------------------------------------------

def take_first_n(entries: list[LogEntry], n: int) -> list[LogEntry]:
    """取前 n 条（ch05：itertools.islice）"""
    return list(itertools.islice(entries, n))


def chain_logs(*sources: list[LogEntry]) -> list[LogEntry]:
    """连接多个列表（ch05：itertools.chain）"""
    return list(itertools.chain(*sources))


def take_while_level(
    entries: list[LogEntry], level: str
) -> list[LogEntry]:
    """持续取出直到遇到非指定级别（ch05：itertools.takewhile）"""
    return list(itertools.takewhile(lambda e: e.level == level, entries))


def group_by_level(
    entries: list[LogEntry],
) -> dict[str, list[LogEntry]]:
    """按日志级别分组（ch05：itertools.groupby，需先排序）"""
    sorted_entries = sorted(entries, key=lambda e: e.level)
    result: dict[str, list[LogEntry]] = {}
    for level, group in itertools.groupby(sorted_entries, key=lambda e: e.level):
        result[level] = list(group)
    return result


def generate_ids(start: int = 1, count: int = 5) -> list[int]:
    """生成连续 ID（ch05：itertools.count + islice）"""
    return list(itertools.islice(itertools.count(start), count))


# ---------------------------------------------------------------------------
# ch06: 异步生成器
# ---------------------------------------------------------------------------

async def async_log_stream(
    entries: list[LogEntry], delay: float = 0.0
) -> None:
    """异步生成器示例（ch06：async def + yield）

    实际使用：
        async for entry in async_log_stream(entries):
            process(entry)
    """
    import asyncio
    for entry in entries:
        if delay > 0:
            await asyncio.sleep(delay)
        yield entry   # type: ignore[misc]  # async generator yield


async def collect_async(entries: list[LogEntry]) -> list[LogEntry]:
    """收集异步生成器的所有条目（ch06：async for）"""
    result = []
    async for entry in async_log_stream(entries):   # type: ignore[misc]
        result.append(entry)
    return result