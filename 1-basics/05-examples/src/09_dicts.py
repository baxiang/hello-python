"""
章节：09 - 字典
文档：01-基础入门篇/数据结构/03-字典.md
"""

from typing import Any


def example_01_basic() -> dict[str, str | int]:
    """示例1：字典最简用法"""
    student: dict[str, str | int] = {"name": "张三", "age": 18}
    print(student["name"])
    student["age"] = 19
    student["city"] = "北京"
    print(student)
    return student


def example_02_level1() -> dict[str, int]:
    """示例2：层级1 - 基础操作"""
    scores: dict[str, int] = {"math": 90, "english": 85}
    scores["science"] = 92
    print(scores)
    return scores


def example_03_level2() -> None:
    """示例3：层级2 - 遍历字典"""
    student: dict[str, str | int] = {"name": "张三", "age": 18, "city": "北京"}
    for key, value in student.items():
        print(f"{key}: {value}")


def example_04_level3() -> str:
    """示例4：层级3 - get 方法"""
    student: dict[str, str | int] = {"name": "张三", "age": 18}
    email: str | int | None = student.get("email", "未设置")
    print(f"邮箱：{email}")
    return str(email)


def example_05_level4() -> None:
    """示例5：层级4 - 嵌套字典"""
    school: dict[str, dict[str, int]] = {
        "class1": {"张三": 85, "李四": 92},
        "class2": {"王五": 78, "赵六": 88},
    }
    print(school["class1"]["张三"])


def example_06_level5() -> dict[str, int]:
    """示例6：层级5 - 字典推导式"""
    words: list[str] = ["apple", "banana", "cherry"]
    word_lengths: dict[str, int] = {w: len(w) for w in words}
    print(word_lengths)
    return word_lengths


def example_practical() -> dict[str, Any]:
    """综合应用：学生成绩查询系统"""
    students: dict[str, dict[str, int]] = {
        "001": {"name": "张三", "score": 85},
        "002": {"name": "李四", "score": 92},
        "003": {"name": "王五", "score": 78},
    }

    student_id: str = "002"
    student = students.get(student_id)
    if student:
        print(f"学号 {student_id}: {student['name']}, 成绩 {student['score']}")

    # 统计平均分
    avg_score: float = sum(s["score"] for s in students.values()) / len(students)
    print(f"平均分：{avg_score:.1f}")

    return {"students": students, "avg_score": avg_score}


def main() -> None:
    """主函数：运行所有示例"""
    print("=" * 60)
    print("章节 09 - 字典")
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
