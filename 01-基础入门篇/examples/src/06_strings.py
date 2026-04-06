"""
章节：06 - 字符串
文档：01-基础入门篇/字符串/01-字符串基础.md
"""


def example_01_basic() -> str:
    """示例1：字符串最简用法"""
    name: str = "Python"
    print(name[0])
    version: float = 3.11
    result = f"{name} {version}"
    print(result)
    return result


def example_02_level1() -> None:
    """示例2：层级1 - 基础操作"""
    text: str = "Hello, Python!"
    print(text[0])
    print(text[7:13])


def example_03_level2() -> None:
    """示例3：层级2 - 常用方法"""
    text: str = "  hello world  "
    print(text.strip())
    print(text.upper())
    print(text.replace("world", "Python"))


def example_04_level3() -> None:
    """示例4：层级3 - 格式化输出"""
    name: str = "张三"
    age: int = 25
    score: float = 85.5
    print(f"姓名：{name}")
    print(f"年龄：{age}岁")
    print(f"成绩：{score:.1f}分")


def example_05_level4() -> None:
    """示例5：层级4 - 分割与连接"""
    csv_line: str = "张三,25,85.5"
    fields: list[str] = csv_line.split(",")
    new_line: str = " | ".join(fields)
    print(new_line)


def example_06_level5() -> int:
    """示例6：层级5 - 文本处理"""
    log: str = """ERROR Connection failed
INFO Retry successful
WARNING High memory usage"""
    lines: list[str] = log.split("\n")
    error_count: int = sum(1 for line in lines if "ERROR" in line)
    print(f"错误数量：{error_count}")
    return error_count


def example_practical() -> dict[str, Any]:
    """综合应用：日志分析程序"""
    log_data: str = """
[2024-01-15 10:30:45] ERROR: Connection failed
[2024-01-15 10:31:20] INFO: Retry successful
[2024-01-15 10:32:00] WARNING: High memory usage
"""

    lines: list[str] = log_data.strip().split("\n")

    levels: list[str] = []
    for line in lines:
        if " ERROR " in line:
            levels.append("ERROR")
        elif " WARNING " in line:
            levels.append("WARNING")
        elif " INFO " in line:
            levels.append("INFO")

    from collections import Counter

    level_counts: dict[str, int] = dict(Counter(levels))

    print(f"总行数：{len(lines)}")
    print(f"级别统计：{level_counts}")

    return {"total_lines": len(lines), "level_counts": level_counts}


def main() -> None:
    """主函数：运行所有示例"""
    print("=" * 60)
    print("章节 06 - 字符串")
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
