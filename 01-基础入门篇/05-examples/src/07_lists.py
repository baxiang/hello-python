"""
章节：07 - 列表
文档：01-基础入门篇/数据结构/01-列表.md
"""

from typing import Any


def example_01_basic() -> list[str]:
    """示例1：列表最简用法"""
    fruits: list[str] = ["苹果", "香蕉", "橘子"]
    print(fruits[0])
    fruits[0] = "西瓜"
    print(fruits)
    return fruits


def example_02_level1() -> list[str]:
    """示例2：层级1 - 基础操作"""
    shopping: list[str] = ["牛奶", "面包", "鸡蛋"]
    shopping.append("苹果")
    print(shopping)
    return shopping


def example_03_level2() -> None:
    """示例3：层级2 - 遍历列表"""
    shopping: list[str] = ["牛奶", "面包", "鸡蛋"]
    for item in shopping:
        print(f"- {item}")


def example_04_level3() -> None:
    """示例4：层级3 - 嵌套列表"""
    weekly_shopping: list[list[str]] = [
        ["牛奶", "面包"],
        ["鸡蛋", "蔬菜"],
        ["水果", "零食"],
    ]
    print(weekly_shopping[0][0])


def example_05_level4() -> list[int]:
    """示例5：层级4 - 列表推导式"""
    prices: list[int] = [5, 15, 8, 20, 12]
    expensive: list[int] = [p for p in prices if p > 10]
    print(expensive)
    return expensive


def example_06_level5() -> None:
    """示例6：层级5 - 列表方法"""
    numbers: list[int] = [3, 1, 4, 1, 5, 9, 2, 6]
    numbers.sort()
    print(f"排序后：{numbers}")
    numbers.reverse()
    print(f"反转后：{numbers}")


def example_practical() -> dict[str, Any]:
    """综合应用：学生成绩管理"""
    students: list[dict[str, Any]] = [
        {"name": "张三", "scores": [85, 90, 78]},
        {"name": "李四", "scores": [92, 88, 95]},
        {"name": "王五", "scores": [78, 82, 88]},
    ]

    for student in students:
        name: str = student["name"]
        scores: list[int] = student["scores"]
        avg: float = sum(scores) / len(scores)
        max_score: int = max(scores)
        print(f"{name}: 平均分 {avg:.1f}, 最高分 {max_score}")

    return students


def main() -> None:
    """主函数：运行所有示例"""
    print("=" * 60)
    print("章节 07 - 列表")
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
