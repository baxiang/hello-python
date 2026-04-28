"""函数示例项目 — 交互式 CLI 演示

运行方式:
    cd functions_demo
    uv run python -m app

学习者可以按章节选择演示，逐步探索函数概念。
每章演示结束后按 Enter 返回菜单，可反复运行感兴趣的章节。
"""

from __future__ import annotations

# ============================================================================
# 第 1 章：函数基础
# ============================================================================

def demo_ch01() -> None:
    """函数基础 — letter_grade / calculate_average / merge_sort"""
    from app.core.functions import calculate_average, letter_grade, merge_sort

    print("\n" + "=" * 50)
    print("  第 1 章：函数基础")
    print("=" * 50)

    print("\n📌 函数定义与调用 — 最简单的代码复用方式\n")

    # letter_grade
    print("letter_grade(score) — 百分制转等级:")
    for score in [95, 85, 72, 60, 45]:
        print(f"  letter_grade({score}) = {letter_grade(score)!r}")

    # calculate_average
    print("\ncalculate_average(scores) — 计算平均分:")
    scores = [80, 90, 70, 85, 95]
    print(f"  scores = {scores}")
    print(f"  calculate_average(scores) = {calculate_average(scores):.2f}")
    print(f"  calculate_average([]) = {calculate_average([]):.2f}")

    # merge_sort
    print("\nmerge_sort(items) — 归并排序（递归）:")
    unsorted = [38, 27, 43, 3, 9, 82, 10]
    print(f"  输入: {unsorted}")
    print(f"  输出: {merge_sort(unsorted)}")
    print(f"  原列表不变: {unsorted}")


# ============================================================================
# 第 2 章：函数参数
# ============================================================================

def demo_ch02() -> None:
    """函数参数详解 — create_student / summarize"""
    from app.core.functions import create_student, summarize

    print("\n" + "=" * 50)
    print("  第 2 章：函数参数详解")
    print("=" * 50)

    print("\n📌 位置参数 / 默认参数 / *args / **kwargs / keyword-only\n")

    # 基础调用
    print("create_student — 演示所有参数类型:")
    s1 = create_student("张三", 85)
    print(f"  最简调用: {s1}")

    s2 = create_student("李四", 92, "英语")
    print(f"  指定 subject: {s2}")

    s3 = create_student("王五", 78, "物理", "努力", "进步大", comment="表现优秀", rank=3)
    print(f"  完整调用: {s3}")

    # summarize
    print("\nsummarize(**kwargs) — 任意数量的键值对:")
    result = summarize(数学=90, 英语=85, 物理=78, 化学=92)
    print("  summarize(数学=90, 英语=85, 物理=78, 化学=92)")
    print(f"  = {result}")


# ============================================================================
# 第 3 章：变量作用域
# ============================================================================

def demo_ch03() -> None:
    """变量作用域 — global / nonlocal / LEGB / 闭包陷阱"""
    from app.core.scope import (
        make_grade_checkers_buggy,
        make_grade_checkers_fixed,
        make_score_accumulator,
        record_call,
        reset_call_count,
        show_legb,
    )

    print("\n" + "=" * 50)
    print("  第 3 章：变量作用域")
    print("=" * 50)

    # global
    print("\n📌 global — 修改全局变量\n")
    reset_call_count()
    print(f"  record_call() 第 1 次 = {record_call()}")
    print(f"  record_call() 第 2 次 = {record_call()}")
    print(f"  record_call() 第 3 次 = {record_call()}")

    # nonlocal — 闭包状态机
    print("\n📌 nonlocal — 闭包共享状态\n")
    add, average, reset = make_score_accumulator()
    print(f"  add(80) = {add(80)}")
    print(f"  add(90) = {add(90)}")
    print(f"  add(70) = {add(70)}")
    print(f"  average() = {average()}")
    reset()
    print(f"  reset() 后 average() = {average()}")

    # 闭包陷阱
    print(f"\n📌 闭包陷阱 — 循环中捕获变量\n")
    thresholds = [60, 70, 80, 90]
    buggy_checkers = make_grade_checkers_buggy(thresholds)
    print(f"  错误写法: thresholds = {thresholds}")
    for i, checker in enumerate(buggy_checkers):
        print(f"    checker[{i}](85) = {checker(85)}  ← 都用最后一个阈值 {thresholds[-1]}")

    fixed_checkers = make_grade_checkers_fixed(thresholds)
    print(f"  正确写法（默认参数固定值）:")
    for i, checker in enumerate(fixed_checkers):
        print(f"    checker[{i}](85) = {checker(85)}  ← 各用各的阈值 {thresholds[i]}")

    # LEGB
    print(f"\n📌 LEGB 规则 — 四个作用域层级:")
    legb_result = show_legb(75)
    print(f"  show_legb(75) = {legb_result}")


# ============================================================================
# 第 4 章：Lambda
# ============================================================================

def demo_ch04() -> None:
    """Lambda 匿名函数 — sort_students / filter_passing / scale_scores"""
    from app.core.builtins import filter_passing, scale_scores, sort_students

    print("\n" + "=" * 50)
    print("  第 4 章：Lambda 匿名函数")
    print("=" * 50)

    print("\n📌 lambda — 简洁的匿名函数，常用于 sorted/filter/map\n")

    students = [
        {"name": "张三", "score": 85},
        {"name": "李四", "score": 92},
        {"name": "王五", "score": 58},
        {"name": "赵六", "score": 76},
    ]
    print(f"原始数据: {students}")

    # sort_students
    print(f"\nsort_students — lambda 作为 sorted key:")
    print(f"  升序: {[s['name'] for s in sort_students(students)]}")
    print(f"  降序: {[s['name'] for s in sort_students(students, reverse=True)]}")

    # filter_passing
    print(f"\nfilter_passing — lambda + filter:")
    passed = filter_passing(students)
    print(f"  及格学生: {[s['name'] for s in passed]}")

    # scale_scores
    print(f"\nscale_scores — lambda + map:")
    scaled = scale_scores(students, factor=1.1)
    print(f"  缩放 1.1 倍: {scaled}")


# ============================================================================
# 第 5 章：内置函数
# ============================================================================

def demo_ch05() -> None:
    """内置函数 — score_stats / all_passed / rank_students"""
    from app.core.builtins import all_passed, rank_students, score_stats

    print("\n" + "=" * 50)
    print("  第 5 章：内置函数")
    print("=" * 50)

    print("\n📌 Python 内置函数 — min/max/sum/len/all/any/enumerate/zip\n")

    # score_stats
    print("score_stats — min/max/sum/len 组合:")
    scores = [80, 90, 70, 85, 95]
    stats = score_stats(scores)
    print(f"  scores = {scores}")
    for key, value in stats.items():
        print(f"    {key}: {value}")

    # all_passed
    print(f"\nall_passed / any_excellent — 聚合判断:")
    students = [
        {"name": "张三", "score": 85},
        {"name": "李四", "score": 92},
        {"name": "王五", "score": 58},
    ]
    print(f"  students = {[s['name'] + ':' + str(s['score']) for s in students]}")
    print(f"  all_passed(students) = {all_passed(students)}")
    print(f"  all_passed(students, threshold=50) = {all_passed(students, threshold=50)}")

    # rank_students
    print(f"\nrank_students — enumerate 生成名次:")
    ranked = rank_students(students)
    for rank, student in ranked:
        print(f"  第 {rank} 名: {student['name']} ({student['score']} 分)")


# ============================================================================
# 主菜单
# ============================================================================

def _clear_screen() -> None:
    """清屏"""
    print("\033[H\033[J", end="")


def _print_menu() -> None:
    """打印菜单"""
    print("=" * 50)
    print("  📚 函数示例项目 — 交互式函数演示")
    print("=" * 50)
    print()
    print("  1.  函数基础（定义、调用、高阶函数、递归）")
    print("  2.  函数参数（位置/默认/*args/**kwargs/keyword-only）")
    print("  3.  变量作用域（global/nonlocal/LEGB/闭包陷阱）")
    print("  4.  Lambda 匿名函数（sorted/filter/map）")
    print("  5.  内置函数（min/max/sum/len/all/any/enumerate）")
    print()
    print("  0.  退出")
    print()


def main() -> None:
    """交互式 CLI 菜单"""
    demos = {
        "1": ("函数基础", demo_ch01),
        "2": ("函数参数", demo_ch02),
        "3": ("变量作用域", demo_ch03),
        "4": ("Lambda 匿名函数", demo_ch04),
        "5": ("内置函数", demo_ch05),
    }

    while True:
        _print_menu()
        choice = input("请选择章节 (0-5): ").strip()

        if choice == "0":
            print("\n👋 再见！")
            break

        if choice in demos:
            name, demo_fn = demos[choice]
            print(f"\n▶ 演示: 第 {choice} 章 — {name}")
            try:
                demo_fn()
            except Exception as e:
                print(f"\n❌ 演示出错: {e}")
            print("\n" + "-" * 50)
            input("按 Enter 返回菜单...")
            _clear_screen()
        else:
            print(f"\n❌ 无效选择: {choice!r}，请输入 0-5")
            input("按 Enter 重试...")
            _clear_screen()


if __name__ == "__main__":
    main()
