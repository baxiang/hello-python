"""
章节：05 - 流程控制
文档：01-基础入门篇/基础语法/03-流程控制.md
"""

from typing import Any


def example_01_basic() -> str:
    """示例1：流程控制最简用法"""
    age: int = 18
    if age >= 18:
        result = "成年人"
    else:
        result = "未成年人"
    print(result)
    return result


def example_02_level1() -> None:
    """示例2：层级1 - 单一条件"""
    age: int = 18
    if age >= 18:
        print("成年人")


def example_03_level2() -> str:
    """示例3：层级2 - 多条件判断"""
    score: int = 85
    if score >= 90:
        result = "优秀"
    elif score >= 60:
        result = "通过"
    else:
        result = "不及格"
    print(result)
    return result


def example_04_level3() -> None:
    """示例4：层级3 - 嵌套条件"""
    score: int = 85
    has_bonus: bool = True
    if score >= 60:
        if has_bonus:
            print("通过 + 加分")
        else:
            print("通过")


def example_05_level4() -> int:
    """示例5：层级4 - 循环 + 条件"""
    scores: list[int] = [85, 45, 92, 58, 78]
    passed: list[int] = []
    for score in scores:
        if score >= 60:
            passed.append(score)
    print(f"通过人数：{len(passed)}")
    return len(passed)


def example_06_level5() -> str:
    """示例6：层级5 - match 语句应用"""
    action: str = "attack"
    match action:
        case "move":
            result = "移动"
        case "attack":
            result = "攻击"
        case "defend":
            result = "防御"
        case _:
            result = "未知动作"
    print(result)
    return result


def example_practical() -> None:
    """综合应用：自动售货机模拟程序"""
    print("=== 自动售货机 ===")
    balance: float = 4.0
    action: str = "B"

    match action:
        case "I":
            print("投币")
        case "B":
            drink: str = "可乐"
            price_map: dict[str, float] = {"可乐": 5.0, "雪碧": 4.0}
            price: float = price_map.get(drink, 0.0)
            if balance >= price:
                print(f"购买{drink}成功！")
            else:
                print(f"余额不足！{drink}需要{price}元")
        case "Q":
            print("退出")


def main() -> None:
    """主函数：运行所有示例"""
    print("=" * 60)
    print("章节 05 - 流程控制")
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
