"""
章节：01 - Python简介
文档：01-基础入门篇/Python入门/01-Python简介.md
"""

import pathlib
from typing import Any


def example_01_basic() -> None:
    """示例1：Python最简用法"""
    print("Hello, World!")
    result = 10 + 20
    print(f"计算结果：{result}")


def example_02_level1() -> None:
    """示例2：层级1 - 单行命令"""
    print("Hello")


def example_03_level2() -> None:
    """示例3：层级2 - 多行脚本"""
    a = 10
    b = 20
    print(f"总和：{a + b}")


def example_04_level3() -> None:
    """示例4：层级3 - 函数封装"""

    def calculate_sum(x: int, y: int) -> int:
        return x + y

    result = calculate_sum(10, 20)
    print(f"函数结果：{result}")


def example_05_level4() -> None:
    """示例5：层级4 - 文件处理"""
    file = pathlib.Path("example.txt")
    print(f"文件路径对象：{file}")


def example_06_level5() -> None:
    """示例6：层级5 - 数据处理"""
    data_dir = pathlib.Path(".")
    py_files = list(data_dir.glob("*.py"))
    print(f"找到 {len(py_files)} 个 Python 文件")


def example_practical() -> None:
    """综合应用：自动化文件整理脚本"""

    def organize_files_demo(source_dir: str) -> dict[str, int]:
        source = pathlib.Path(source_dir)
        stats: dict[str, int] = {}
        for file in source.glob("*.*"):
            if file.is_file():
                ext = file.suffix.lower()
                stats[ext] = stats.get(ext, 0) + 1
        return stats

    result = organize_files_demo(".")
    print(f"文件统计：{result}")


def main() -> None:
    """主函数：运行所有示例"""
    print("=" * 60)
    print("章节 01 - Python简介")
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
