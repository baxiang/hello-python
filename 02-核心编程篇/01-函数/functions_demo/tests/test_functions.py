"""函数篇测试套件 — 学生成绩统计系统，覆盖第01-05章"""

import pytest

from app.core.builtins import (
    all_passed,
    any_excellent,
    clamp_score,
    classify_items,
    filter_passing,
    pair_name_score,
    rank_students,
    scale_scores,
    score_stats,
    sort_by_name,
    sort_students,
    top_n,
    total_score,
)
from app.core.functions import (
    apply_to_all,
    calculate_average,
    create_student,
    letter_grade,
    make_threshold_checker,
    merge_sort,
    summarize,
)
from app.core.scope import (
    get_call_count,
    make_grade_checkers_fixed,
    make_score_accumulator,
    record_call,
    reset_call_count,
    show_legb,
)
from app.utils.helpers import format_rank_list, format_student


# ===========================================================================
# ch01: 函数基础
# ===========================================================================
class TestFunctionBasics:
    """ch01: 基础函数、高阶函数、函数作为返回值、递归"""

    def test_letter_grade_boundaries(self):
        assert letter_grade(95) == "A"
        assert letter_grade(90) == "A"
        assert letter_grade(89) == "B"
        assert letter_grade(80) == "B"
        assert letter_grade(79) == "C"
        assert letter_grade(70) == "C"
        assert letter_grade(69) == "D"
        assert letter_grade(60) == "D"
        assert letter_grade(59) == "F"

    def test_calculate_average(self):
        assert calculate_average([80.0, 90.0, 70.0]) == 80.0

    def test_calculate_average_empty(self):
        assert calculate_average([]) == 0.0

    def test_apply_to_all_higher_order(self):
        """高阶函数：函数作为参数"""
        scores = [60.0, 70.0, 80.0]
        result = apply_to_all(scores, lambda s: s + 5)
        assert result == [65.0, 75.0, 85.0]

    def test_make_threshold_checker_returns_function(self):
        """函数作为返回值"""
        is_passing = make_threshold_checker(60.0)
        assert callable(is_passing)
        assert is_passing(75.0) is True
        assert is_passing(55.0) is False

    def test_merge_sort_recursion(self):
        """递归：归并排序"""
        assert merge_sort([3.0, 1.0, 4.0, 1.0, 5.0]) == [1.0, 1.0, 3.0, 4.0, 5.0]

    def test_merge_sort_empty(self):
        assert merge_sort([]) == []

    def test_merge_sort_single(self):
        assert merge_sort([42.0]) == [42.0]


# ===========================================================================
# ch02: 函数参数详解
# ===========================================================================
class TestFunctionParameters:
    """ch02: 位置/默认/*args/**kwargs/keyword-only/positional-only"""

    def test_positional_only_args(self):
        r = create_student("张三", 85.0)
        assert r["name"] == "张三"
        assert r["score"] == 85.0
        assert r["subject"] == "数学"   # 默认值

    def test_positional_only_with_default_subject(self):
        r = create_student("李四", 92.0, "英语")
        assert r["subject"] == "英语"

    def test_positional_only_cannot_be_keyword(self):
        """positional-only 参数不允许以关键字形式传入"""
        with pytest.raises(TypeError):
            create_student(name="张三", score=85.0)  # type: ignore[call-arg]

    def test_args_collected(self):
        r = create_student("王五", 78.0, "语文", "勤奋", "进步大")
        assert r["tags"] == ("勤奋", "进步大")

    def test_keyword_only_args(self):
        r = create_student("赵六", 65.0, comment="需努力", rank=10)
        assert r["comment"] == "需努力"
        assert r["rank"] == 10

    def test_kwargs_summarize(self):
        """**kwargs 场景"""
        result = summarize(数学=90.0, 英语=85.0, 物理=78.0)
        assert result["数学"] == 90.0
        assert result["英语"] == 85.0
        assert len(result) == 3


# ===========================================================================
# ch03: 变量作用域
# ===========================================================================
class TestScope:
    """ch03: global / nonlocal / LEGB / 闭包陷阱"""

    def setup_method(self):
        reset_call_count()

    def test_global_statement(self):
        """global 修改全局变量"""
        assert get_call_count() == 0
        record_call()
        record_call()
        assert get_call_count() == 2

    def test_global_reset(self):
        record_call()
        reset_call_count()
        assert get_call_count() == 0

    def test_nonlocal_accumulator(self):
        """nonlocal 维护闭包状态"""
        add, average, reset = make_score_accumulator()
        add(80.0)
        add(90.0)
        add(70.0)
        assert average() == 80.0

    def test_nonlocal_reset(self):
        add, average, reset = make_score_accumulator(50.0)
        add(100.0)
        reset()
        assert average() == 0.0   # count 变为 0，返回 0

    def test_nonlocal_independent_closures(self):
        """两个 accumulator 互相独立（各自有独立的 total/count）"""
        add1, avg1, _ = make_score_accumulator()
        add2, avg2, _ = make_score_accumulator()
        add1(100.0)
        add2(60.0)
        assert avg1() == 100.0
        assert avg2() == 60.0

    def test_closure_trap_fixed(self):
        """闭包陷阱修复：用默认参数固定捕获值"""
        thresholds = [60.0, 70.0, 80.0]
        checkers = make_grade_checkers_fixed(thresholds)
        assert checkers[0](65.0) is True    # >= 60
        assert checkers[1](65.0) is False   # >= 70
        assert checkers[2](65.0) is False   # >= 80

    def test_legb_rule(self):
        """LEGB 四层作用域"""
        result = show_legb(75.0)
        assert result["local_result"] is True        # L
        assert result["enclosing_label"] == "及格线"  # E
        assert result["global_scale"] == 100          # G
        assert result["builtin_abs"] == 75.0          # B


# ===========================================================================
# ch04: Lambda 匿名函数
# ===========================================================================
class TestLambda:
    """ch04: lambda 语法、lambda 作为 key/filter/map/reduce"""

    def setup_method(self):
        self.students = [
            {"name": "张三", "score": 85.0},
            {"name": "李四", "score": 92.0},
            {"name": "王五", "score": 60.0},
            {"name": "赵六", "score": 55.0},
        ]

    def test_sort_by_score_ascending(self):
        result = sort_students(self.students)
        assert result[0]["score"] == 55.0
        assert result[-1]["score"] == 92.0

    def test_sort_by_score_descending(self):
        result = sort_students(self.students, reverse=True)
        assert result[0]["score"] == 92.0

    def test_sort_by_name(self):
        """lambda key=name"""
        result = sort_by_name(self.students)
        names = [s["name"] for s in result]
        assert names == sorted(names)

    def test_filter_passing_lambda(self):
        """filter + lambda"""
        result = filter_passing(self.students, threshold=60.0)
        assert all(s["score"] >= 60.0 for s in result)
        assert len(result) == 3

    def test_scale_scores_map_lambda(self):
        """map + lambda"""
        result = scale_scores([{"score": 80.0}, {"score": 60.0}], factor=1.1)
        assert result[0] == pytest.approx(88.0)

    def test_total_score_reduce_lambda(self):
        """reduce + lambda"""
        assert total_score([80.0, 90.0, 70.0]) == pytest.approx(240.0)

    def test_total_score_empty(self):
        assert total_score([]) == 0.0


# ===========================================================================
# ch05: Python 内置函数
# ===========================================================================
class TestBuiltins:
    """ch05: map/filter/sorted/enumerate/zip/any/all/min/max/sum/isinstance"""

    def setup_method(self):
        self.students = [
            {"name": "张三", "score": 85.0},
            {"name": "李四", "score": 92.0},
            {"name": "王五", "score": 58.0},
        ]

    def test_score_stats_min_max_sum(self):
        stats = score_stats([80.0, 90.0, 70.0])
        assert stats["min"] == 70.0
        assert stats["max"] == 90.0
        assert stats["total"] == pytest.approx(240.0)
        assert stats["average"] == pytest.approx(80.0)

    def test_score_stats_empty(self):
        assert score_stats([]) == {}

    def test_all_passed(self):
        """all()"""
        passed = [{"name": "A", "score": 70.0}, {"name": "B", "score": 80.0}]
        assert all_passed(passed) is True
        assert all_passed(self.students) is False

    def test_any_excellent(self):
        """any()"""
        assert any_excellent(self.students, threshold=90.0) is True
        assert any_excellent(self.students, threshold=95.0) is False

    def test_rank_students_enumerate(self):
        """enumerate()"""
        ranked = rank_students(self.students)
        assert ranked[0][0] == 1                  # 第1名
        assert ranked[0][1]["score"] == 92.0      # 最高分
        assert len(ranked) == len(self.students)

    def test_pair_name_score_zip(self):
        """zip()"""
        names = ["张三", "李四"]
        scores = [85.0, 92.0]
        result = pair_name_score(names, scores)
        assert result[0] == {"name": "张三", "score": 85.0}
        assert result[1] == {"name": "李四", "score": 92.0}

    def test_clamp_score(self):
        """min/max 组合"""
        assert clamp_score(110.0) == 100.0
        assert clamp_score(-5.0) == 0.0
        assert clamp_score(75.0) == 75.0

    def test_classify_items_isinstance(self):
        """isinstance()"""
        items = [1, 2.0, "hello", True, [1, 2]]
        result = classify_items(items)
        assert 1 in result["int"]
        assert 2.0 in result["float"]
        assert "hello" in result["str"]
        assert True in result["other"]   # bool 先于 int 被识别

    def test_top_n(self):
        """sorted + 切片"""
        top = top_n(self.students, 2)
        assert len(top) == 2
        assert top[0]["score"] == 92.0


# ===========================================================================
# helpers
# ===========================================================================
class TestHelpers:
    def test_format_student(self):
        r = {"name": "张三", "score": 85.5, "subject": "数学"}
        assert "张三" in format_student(r)
        assert "85.5" in format_student(r)

    def test_format_rank_list_empty(self):
        assert format_rank_list([]) == "（暂无数据）"

    def test_format_rank_list(self):
        ranked = [(1, {"name": "李四", "score": 92.0, "subject": "英语"})]
        result = format_rank_list(ranked)
        assert "第1名" in result
        assert "李四" in result
