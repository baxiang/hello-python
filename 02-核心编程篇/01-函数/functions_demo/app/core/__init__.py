"""核心模块 — 学生成绩统计系统，覆盖函数篇第01-05章"""

from app.core.builtins import (
    all_passed,
    any_excellent,
    classify_items,
    clamp_score,
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

__all__ = [
    # ch01 / ch02
    "letter_grade", "calculate_average", "apply_to_all",
    "make_threshold_checker", "merge_sort",
    "create_student", "summarize",
    # ch03
    "record_call", "get_call_count", "reset_call_count",
    "make_score_accumulator", "make_grade_checkers_fixed", "show_legb",
    # ch04 / ch05
    "sort_students", "sort_by_name", "filter_passing",
    "scale_scores", "total_score", "score_stats",
    "all_passed", "any_excellent", "rank_students",
    "pair_name_score", "clamp_score", "classify_items", "top_n",
]