import argparse
from pathlib import Path
from app.fetcher import fetch_trending_page
from app.parser import parse_trending_page
from app.storage import save_json, save_csv, format_terminal


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    """
    解析命令行参数

    Args:
        args: 参数列表（None 时从 sys.argv 读取）

    Returns:
        解析后的参数对象
    """
    parser = argparse.ArgumentParser(
        description="GitHub Trending 热榜追踪工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--language",
        type=str,
        default=None,
        help="按编程语言过滤（如 python, javascript, go）",
    )

    parser.add_argument(
        "--range",
        type=str,
        choices=["daily", "weekly", "monthly"],
        default="daily",
        help="时间范围：daily（今日）、weekly（本周）、monthly（本月）",
    )

    parser.add_argument(
        "--output",
        type=str,
        choices=["terminal", "json", "csv"],
        default="terminal",
        help="输出格式：terminal（终端）、json、csv",
    )

    parser.add_argument(
        "--file",
        type=str,
        default=None,
        help="输出文件路径（json/csv 格式时使用）",
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=25,
        help="显示项目数量限制",
    )

    return parser.parse_args(args)


def main(args: list[str] | None = None) -> str:
    """
    主函数

    Args:
        args: 命令行参数

    Returns:
        输出内容（terminal 格式）或文件路径
    """
    parsed = parse_args(args)

    try:
        html = fetch_trending_page(language=parsed.language, time_range=parsed.range)
        repos = parse_trending_page(html, limit=parsed.limit)

        if parsed.output == "terminal":
            output = format_terminal(repos)
            print(output)
            return output

        elif parsed.output == "json":
            filepath = Path(parsed.file) if parsed.file else Path("trending.json")
            save_json(repos, filepath)
            print(f"已保存到: {filepath}")
            return str(filepath)

        elif parsed.output == "csv":
            filepath = Path(parsed.file) if parsed.file else Path("trending.csv")
            save_csv(repos, filepath)
            print(f"已保存到: {filepath}")
            return str(filepath)

    except Exception as e:
        print(f"错误: {e}")
        raise


if __name__ == "__main__":
    main()
