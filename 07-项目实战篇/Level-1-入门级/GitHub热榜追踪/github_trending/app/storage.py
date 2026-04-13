import json
import csv
from pathlib import Path
from app.models import TrendingRepo


def save_json(repos: list[TrendingRepo], filepath: Path) -> None:
    """
    保存为 JSON 文件

    Args:
        repos: TrendingRepo 列表
        filepath: 输出文件路径
    """
    data = [repo.to_dict() for repo in repos]

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_csv(repos: list[TrendingRepo], filepath: Path) -> None:
    """
    保存为 CSV 文件

    Args:
        repos: TrendingRepo 列表
        filepath: 输出文件路径
    """
    if not repos:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("")
        return

    fieldnames = [
        "name",
        "description",
        "language",
        "stars",
        "forks",
        "stars_today",
        "url",
    ]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for repo in repos:
            writer.writerow(repo.to_dict())


def format_terminal(repos: list[TrendingRepo]) -> str:
    """
    格式化为终端输出

    Args:
        repos: TrendingRepo 列表

    Returns:
        格式化的文本字符串
    """
    if not repos:
        return "暂无热门项目数据"

    lines = []
    for i, repo in enumerate(repos, 1):
        stars_formatted = _format_number(repo.stars)
        stars_today_formatted = _format_number(repo.stars_today)

        line = f"{i}. {repo.name}"
        if repo.language:
            line += f" ({repo.language})"
        line += f" - ⭐ {stars_formatted}"
        if repo.stars_today > 0:
            line += f" (+{stars_today_formatted} today)"
        lines.append(line)

        if repo.description:
            lines.append(f"   {repo.description}")
        lines.append(f"   {repo.url}")
        lines.append("")

    return "\n".join(lines)


def _format_number(n: int) -> str:
    """格式化数字，添加千位分隔符"""
    return f"{n:,}"
