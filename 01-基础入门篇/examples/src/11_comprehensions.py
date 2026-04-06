"""
章节：11 - 推导式
文档：01-基础入门篇/数据结构/05-推导式.md
"""

from typing import Any


def example_01_basic() -> list[int]:
    """示例1：推导式最简用法"""
    squares: list[int] = [x**2 for x in range(5)]
    print(squares)
    return squares


def example_02_level1() -> list[int]:
    """示例2：层级1 - 基础转换"""
    squares: list[int] = [x**2 for x in range(5)]
    print(squares)
    return squares


def example_03_level2() -> list[int]:
    """示例3：层级2 - 条件过滤"""
    numbers: list[int] = list(range(10))
    evens: list[int] = [x for x in numbers if x % 2 == 0]
    print(evens)
    return evens


def example_04_level3() -> list[tuple[int, int]]:
    """示例4：层级3 - 嵌套循环"""
    points: list[tuple[int, int]] = [(x, y) for x in range(3) for y in range(3)]
    print(points)
    return points


def example_05_level4() -> dict[str, int]:
    """示例5：层级4 - 字典推导式"""
    words: list[str] = ["apple", "banana", "cherry"]
    word_lengths: dict[str, int] = {w: len(w) for w in words}
    print(word_lengths)
    return word_lengths


def example_06_level5() -> int:
    """示例6：层级5 - 生成器表达式"""
    big_data = range(100)
    sum_of_squares: int = sum(x**2 for x in big_data if x % 2 == 0)
    print(sum_of_squares)
    return sum_of_squares


def example_practical() -> dict[str, Any]:
    """综合应用：数据处理管道"""
    students: list[dict[str, Any]] = [
        {"id": 1, "name": "张三", "score": 85, "course": "数学"},
        {"id": 2, "name": "李四", "score": 92, "course": "数学"},
        {"id": 3, "name": "王五", "score": 58, "course": "物理"},
    ]

    # 列表推导式：筛选及格学生
    passed: list[dict[str, Any]] = [s for s in students if s["score"] >= 60]

    # 字典推导式：创建学号-姓名映射
    id_name_map: dict[int, str] = {s["id"]: s["name"] for s in students}

    # 集合推导式：获取唯一课程
    courses: set[str] = {s["course"] for s in students}

    # 生成器表达式：计算平均分
    avg_score: float = sum(s["score"] for s in students) / len(students)

    print(f"及格人数：{len(passed)}")
    print(f"平均分：{avg_score:.1f}")
    print(f"课程：{courses}")
    print(f"学号映射：{id_name_map}")

    return {
        "passed_count": len(passed),
        "average_score": avg_score,
        "courses": courses,
        "id_name_map": id_name_map,
    }


def main() -> None:
    """主函数：运行所有示例"""
    print("=" * 60)
    print("章节 11 - 推导式")
    print("=" * 60)

    example_01_basic()
    example_02_level1()
    example_03_level2()
    example_04_level3()
    example_05_level4()
    example_06_level5()
    example_practical()

    print("=" * 60)
    print("✅ 所有示例运行完成")


if __name__ == "__main__":
    main()
