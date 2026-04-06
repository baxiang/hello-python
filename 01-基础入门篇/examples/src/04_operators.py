"""
章节：04 - 运算符
文档：01-基础入门篇/基础语法/02-运算符.md
"""

from typing import Any


def example_01_basic() -> dict[str, float]:
    """示例1：运算符最简用法"""
    print(f"加法：{10 + 5}")
    print(f"减法：{10 - 5}")
    print(f"乘法：{10 * 5}")
    print(f"除法：{10 / 5}")
    return {"add": 15, "sub": 5, "mul": 50, "div": 2.0}


def example_02_level1() -> dict[str, int]:
    """示例2：层级1 - 基础计算"""
    a: int = 10
    b: int = 3
    print(f"加：{a + b}")
    print(f"减：{a - b}")
    return {"a": a, "b": b}


def example_03_level2() -> dict[str, int]:
    """示例3：层级2 - 高级算术"""
    a: int = 10
    b: int = 3
    print(f"整除：{a // b}")
    print(f"取模：{a % b}")
    print(f"幂运算：{a**b}")
    return {"floor": a // b, "mod": a % b, "power": a**b}


def example_04_level3() -> dict[str, bool]:
    """示例4：层级3 - 比较判断"""
    num: int = 7
    is_odd: bool = num % 2 != 0
    print(f"{num}是奇数：{is_odd}")
    return {"is_odd": is_odd}


def example_05_level4() -> dict[str, bool]:
    """示例5：层级4 - 逻辑组合"""
    age: int = 25
    has_license: bool = True
    can_drive: bool = age >= 18 and has_license
    print(f"可以驾驶：{can_drive}")
    return {"can_drive": can_drive}


def example_06_level5() -> float:
    """示例6：层级5 - 复合运算"""
    prices: list[float] = [29.9, 15.5, 8.0]
    quantities: list[int] = [2, 1, 3]
    total: float = sum(p * q for p, q in zip(prices, quantities))
    discount: float = 20.0 if total >= 100 else 0.0
    final: float = total - discount
    print(f"总价：{total:.1f}元，优惠：{discount:.1f}元")
    return final


def example_practical() -> dict[str, float]:
    """综合应用：购物车结算程序"""
    cart: list[dict[str, Any]] = [
        {"name": "Python书籍", "price": 59.9, "quantity": 2},
        {"name": "编程键盘", "price": 199.0, "quantity": 1},
    ]

    subtotal: float = sum(item["price"] * item["quantity"] for item in cart)
    discount: float = 30.0 if subtotal >= 200 else 0.0
    final: float = subtotal - discount

    print(f"商品总价：{subtotal:.2f}元")
    print(f"满减优惠：{discount:.2f}元")
    print(f"实付金额：{final:.2f}元")

    return {"subtotal": subtotal, "discount": discount, "final": final}


def main() -> None:
    """主函数：运行所有示例"""
    print("=" * 60)
    print("章节 04 - 运算符")
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
