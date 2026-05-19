"""
章节：08 - 元组
文档：01-基础入门篇/数据结构/02-元组.md
"""

from collections import namedtuple
from typing import Any


def example_01_basic() -> tuple[int, int]:
    """示例1：元组最简用法"""
    point: tuple[int, int] = (10, 20)
    print(point[0])
    x, y = point
    print(f"x={x}, y={y}")
    return point


def example_02_level1() -> tuple[str, str, str]:
    """示例2：层级1 - 创建和访问"""
    colors: tuple[str, str, str] = ("red", "green", "blue")
    print(colors[0])
    return colors


def example_03_level2() -> tuple[int, int, int]:
    """示例3：层级2 - 解包"""
    rgb: tuple[int, int, int] = (255, 128, 0)
    r, g, b = rgb
    print(f"R:{r}, G:{g}, B:{b}")
    return rgb


def example_04_level3() -> float:
    """示例4：层级3 - 作为字典键"""
    distances: dict[tuple[int, int], float] = {(0, 0): 0.0, (1, 0): 1.0, (1, 1): 1.414}
    result = distances[(1, 1)]
    print(result)
    return result


def example_05_level4() -> Any:
    """示例5：层级4 - 命名元组"""
    Point = namedtuple("Point", ["x", "y"])
    p = Point(3, 4)
    print(f"Point({p.x}, {p.y})")
    return p


def example_06_level5() -> tuple[int, int, float]:
    """示例6：层级5 - 函数返回多个值"""

    def get_stats(numbers: list[int]) -> tuple[int, int, float]:
        return min(numbers), max(numbers), sum(numbers) / len(numbers)

    minimum, maximum, average = get_stats([1, 2, 3, 4, 5])
    print(f"最小值：{minimum}, 最大值：{maximum}, 平均值：{average}")
    return minimum, maximum, average


def example_practical() -> Any:
    """综合应用：配置管理系统"""
    DatabaseConfig = namedtuple("DatabaseConfig", ["host", "port", "database"])

    db_config: DatabaseConfig = DatabaseConfig(
        host="localhost", port=3306, database="myapp"
    )

    print(f"数据库：{db_config.host}:{db_config.port}/{db_config.database}")
    return db_config


def main() -> None:
    """主函数：运行所有示例"""
    print("=" * 60)
    print("章节 08 - 元组")
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
