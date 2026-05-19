"""迭代器与生成器测试套件 — 日志流处理系统，覆盖第01-06章"""

import asyncio
import itertools

import pytest

from app.core.iterators import (
    LogCollection,
    LogEntry,
    LogIterator,
    async_log_stream,
    chain_logs,
    collect_async,
    fibonacci,
    filter_by_level,
    generate_ids,
    group_by_level,
    log_accumulator,
    log_generator,
    manual_iterate,
    merge_logs,
    message_lengths,
    safe_log_reader,
    take_first_n,
    take_while_level,
)


def make_entries(*pairs: tuple[str, str]) -> list[LogEntry]:
    return [LogEntry(level, msg) for level, msg in pairs]


# ===========================================================================
# ch01: 迭代基础 — iter() / next()
# ===========================================================================
class TestIterationBasics:
    """ch01: iter()/next() 手动迭代；StopIteration 的触发"""

    def test_manual_iterate_list(self):
        result = manual_iterate([10, 20, 30])
        assert result == [10, 20, 30]

    def test_manual_iterate_empty(self):
        assert manual_iterate([]) == []

    def test_manual_iterate_string(self):
        result = manual_iterate("abc")
        assert result == ["a", "b", "c"]

    def test_iterator_exhausted_raises_stop_iteration(self):
        it = iter([1])
        next(it)
        with pytest.raises(StopIteration):
            next(it)


# ===========================================================================
# ch02: 自定义迭代器 — __iter__ / __next__ / 可迭代类
# ===========================================================================
class TestCustomIterator:
    """ch02: LogIterator（只能遍历一次）；LogCollection（可多次遍历）"""

    def setup_method(self):
        self.entries = make_entries(
            ("INFO", "启动"), ("WARN", "内存高"), ("ERROR", "连接失败")
        )

    def test_log_iterator_yields_all_entries(self):
        it = LogIterator(self.entries)
        result = list(it)
        assert len(result) == 3
        assert result[0].message == "启动"

    def test_log_iterator_exhausted_after_one_pass(self):
        """迭代器只能遍历一次——__iter__ 返回 self"""
        it = LogIterator(self.entries)
        list(it)                    # 第一次遍历
        assert list(it) == []       # 已耗尽

    def test_log_collection_supports_multiple_iterations(self):
        """可迭代类：每次 iter() 返回新迭代器，支持多次遍历"""
        col = LogCollection(self.entries)
        first = list(col)
        second = list(col)
        assert first == second
        assert len(first) == 3

    def test_log_collection_two_iterators_independent(self):
        """两个迭代器互相独立，不共享状态"""
        col = LogCollection(self.entries)
        it1 = iter(col)
        it2 = iter(col)
        next(it1)
        next(it1)
        # it2 仍从头开始
        assert next(it2).message == "启动"

    def test_log_iterator_for_loop(self):
        it = LogIterator(self.entries)
        levels = [e.level for e in it]
        assert levels == ["INFO", "WARN", "ERROR"]


# ===========================================================================
# ch03: 生成器基础 — yield / 生成器表达式
# ===========================================================================
class TestGeneratorBasics:
    """ch03: yield 生成器函数；惰性求值；生成器表达式"""

    def setup_method(self):
        self.entries = make_entries(
            ("INFO", "ok"), ("ERROR", "fail"), ("INFO", "ok2")
        )

    def test_log_generator_lazy(self):
        gen = log_generator(self.entries)
        assert next(gen).level == "INFO"
        assert next(gen).level == "ERROR"

    def test_filter_by_level(self):
        result = list(filter_by_level(self.entries, "INFO"))
        assert len(result) == 2
        assert all(e.level == "INFO" for e in result)

    def test_fibonacci_first_ten(self):
        """无限生成器 + islice 截取"""
        result = list(itertools.islice(fibonacci(), 10))
        assert result == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

    def test_message_lengths_genexpr(self):
        """生成器表达式"""
        lengths = message_lengths(self.entries)
        assert lengths == [2, 4, 3]   # "ok", "fail", "ok2"

    def test_generator_is_lazy_not_list(self):
        """生成器是惰性的，不是列表"""
        gen = log_generator(self.entries)
        assert hasattr(gen, "__next__")


# ===========================================================================
# ch04: 生成器高级特性 — send / throw / yield from
# ===========================================================================
class TestAdvancedGenerator:
    """ch04: send() 双向通信；throw() 注入异常；yield from 委托"""

    def setup_method(self):
        self.entries = make_entries(
            ("INFO", "a"), ("WARN", "b"), ("ERROR", "c")
        )

    def test_send_accumulates_count(self):
        """send() 向生成器传值"""
        gen = log_accumulator()
        count0 = next(gen)        # 启动
        assert count0 == 0
        count1 = gen.send(LogEntry("INFO", "x"))
        assert count1 == 1
        count2 = gen.send(LogEntry("ERROR", "y"))
        assert count2 == 2
        gen.close()

    def test_send_none_does_not_increment(self):
        gen = log_accumulator()
        next(gen)
        count = gen.send(None)   # send(None) 等同于 next()
        assert count == 0

    def test_throw_skips_entry(self):
        """throw() 向生成器注入异常，生成器内部捕获并继续"""
        gen = safe_log_reader(self.entries)
        first = next(gen)
        assert first.level == "INFO"
        skipped = gen.throw(ValueError)
        assert skipped == "[跳过无效条目]"

    def test_yield_from_merges_sources(self):
        """yield from 委托——两个来源的日志合并"""
        src1 = make_entries(("INFO", "a"), ("INFO", "b"))
        src2 = make_entries(("ERROR", "c"))
        result = list(merge_logs(src1, src2))
        assert len(result) == 3
        assert result[2].level == "ERROR"


# ===========================================================================
# ch05: itertools 模块
# ===========================================================================
class TestItertools:
    """ch05: islice / chain / takewhile / groupby / count"""

    def setup_method(self):
        self.entries = make_entries(
            ("INFO", "1"), ("INFO", "2"), ("WARN", "3"), ("ERROR", "4")
        )

    def test_take_first_n_islice(self):
        result = take_first_n(self.entries, 2)
        assert len(result) == 2
        assert result[-1].message == "2"

    def test_chain_logs(self):
        src1 = make_entries(("INFO", "a"))
        src2 = make_entries(("ERROR", "b"))
        result = chain_logs(src1, src2)
        assert len(result) == 2
        assert result[0].level == "INFO"
        assert result[1].level == "ERROR"

    def test_take_while_level(self):
        """takewhile 遇到非目标级别立即停止"""
        result = take_while_level(self.entries, "INFO")
        assert len(result) == 2
        assert all(e.level == "INFO" for e in result)

    def test_group_by_level(self):
        """groupby 按级别分组"""
        groups = group_by_level(self.entries)
        assert "INFO" in groups
        assert "WARN" in groups
        assert "ERROR" in groups
        assert len(groups["INFO"]) == 2

    def test_generate_ids_count(self):
        """itertools.count + islice"""
        ids = generate_ids(start=10, count=4)
        assert ids == [10, 11, 12, 13]


# ===========================================================================
# ch06: 异步生成器
# ===========================================================================
class TestAsyncGenerator:
    """ch06: async def + yield；async for"""

    def test_collect_async_all_entries(self):
        """async for 收集异步生成器全部条目"""
        entries = make_entries(("INFO", "x"), ("WARN", "y"))
        result = asyncio.run(collect_async(entries))
        assert len(result) == 2
        assert result[0].level == "INFO"
        assert result[1].level == "WARN"

    def test_async_generator_is_async_iterable(self):
        """async_log_stream 返回的是异步生成器"""
        entries = make_entries(("INFO", "x"))
        gen = async_log_stream(entries)
        assert hasattr(gen, "__aiter__")
        assert hasattr(gen, "__anext__")
