"""第 2 章测试 — 闭包与作用域链"""

from app.decorators.ch02_closures import (
    create_multipliers_correct,
    create_multipliers_wrong,
    inspect_closure,
    make_counter,
    make_counter_with_ops,
    make_multiplier,
    outer_enclosed,
)


class TestClosures:
    """测试闭包的核心概念"""

    def test_closure_captures_variable(self):
        """闭包捕获外层变量"""
        double = make_multiplier(2)
        triple = make_multiplier(3)
        assert double(5) == 10
        assert triple(5) == 15

    def test_closure_independence(self):
        """每次调用工厂函数创建独立的闭包"""
        double = make_multiplier(2)
        double2 = make_multiplier(2)
        assert double is not double2

    def test_counter_increments(self):
        """计数器递增"""
        counter = make_counter(0)
        assert counter() == 1
        assert counter() == 2
        assert counter() == 3

    def test_counter_initial_value(self):
        """计数器初始值"""
        counter = make_counter(10)
        assert counter() == 11

    def test_two_counters_independent(self):
        """两个计数器互不影响"""
        a = make_counter(0)
        b = make_counter(0)
        a()
        a()
        assert b() == 1

    def test_counter_with_ops(self):
        """带多种操作的计数器"""
        ops = make_counter_with_ops(10)
        assert ops["increment"]() == 11
        assert ops["decrement"]() == 10
        assert ops["get"]() == 10
        assert ops["reset"]() == 0
        assert ops["get"]() == 0

    def test_closure_loop_trap_wrong(self):
        """循环变量陷阱 — 所有函数使用最后的 i=4"""
        multipliers = create_multipliers_wrong()
        assert multipliers[0](2) == 8  # 2*4=8，不是 2*0=0
        assert multipliers[1](2) == 8

    def test_closure_loop_trap_correct(self):
        """用默认参数修复循环陷阱"""
        multipliers = create_multipliers_correct()
        assert multipliers[0](2) == 0  # 2*0=0
        assert multipliers[1](2) == 2  # 2*1=2
        assert multipliers[4](2) == 8  # 2*4=8

    def test_inspect_closure(self):
        """检查闭包的自由变量"""
        double = make_multiplier(2)
        info = inspect_closure(double)
        assert "factor" in info["freevars"]
        assert 2 in info["cell_contents"]

    def test_legb_lookup(self):
        """LEGB 查找 — 找到 E 层"""
        inner = outer_enclosed()
        assert inner() == "enclosed"
