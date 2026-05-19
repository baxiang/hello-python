"""
章节：03 - 变量与数据类型
文档：01-基础入门篇/基础语法/01-变量与数据类型.md
"""

from typing import Any


def example_01_basic() -> dict[str, Any]:
    """示例1：变量最简用法"""
    name: str = "Python"
    age: int = 33
    print(f"名称：{name}")
    print(f"年龄：{age}")
    return {"name": name, "age": age}


def example_02_level1() -> str:
    """示例2：层级1 - 单个变量"""
    name: str = "Python"
    print(name)
    return name


def example_03_level2() -> dict[str, Any]:
    """示例3：层级2 - 多个变量"""
    name: str = "张三"
    age: int = 18
    score: float = 85.5
    print(f"{name}, {age}岁, {score}分")
    return {"name": name, "age": age, "score": score}


def example_04_level3() -> tuple[int, int]:
    """示例4：层级3 - 变量交换"""
    a: int = 10
    b: int = 20
    a, b = b, a
    print(f"交换后：a={a}, b={b}")
    return a, b


def example_05_level4() -> str:
    """示例5：层级4 - 动态变量"""
    x: int | str = 10
    x = "现在是字符串"
    print(f"x: {x}")
    return x


def example_06_level5() -> float:
    """示例6：层级5 - 变量与运算"""
    price: float = 99.9
    quantity: int = 3
    total: float = price * quantity
    print(f"总价：{total:.2f}")
    return total


def example_practical() -> list[dict[str, Any]]:
    """综合应用：学生信息管理示例"""
    students: list[dict[str, Any]] = [
        {"name": "张三", "age": 18, "scores": [85, 90, 78]},
        {"name": "李四", "age": 19, "scores": [92, 88, 95]},
        {"name": "王五", "age": 17, "scores": [78, 82, 88]},
    ]

    for student in students:
        name: str = student["name"]
        scores: list[int] = student["scores"]
        average: float = sum(scores) / len(scores)
        passed: bool = average >= 60
        print(f"{name}: 平均分 {average:.1f} - {'通过' if passed else '未通过'}")

    return students


def main() -> None:
    """主函数：运行所有示例"""
    print("=" * 60)
    print("章节 03 - 变量与数据类型")
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
