import re
from bs4 import BeautifulSoup
from app.models import TrendingRepo


def parse_trending_page(html: str, limit: int | None = None) -> list[TrendingRepo]:
    """
    解析 GitHub Trending 页面 HTML

    Args:
        html: 页面 HTML 内容
        limit: 返回项目数量限制

    Returns:
        TrendingRepo 列表
    """
    soup = BeautifulSoup(html, "html.parser")
    articles = soup.select("article.Box-row")

    repos = []
    articles_to_process = articles[:limit] if limit else articles

    for article in articles_to_process:
        repo = _parse_repo_article(article)
        if repo:
            repos.append(repo)

    return repos


def _parse_repo_article(article) -> TrendingRepo | None:
    """解析单个项目 article 元素"""
    try:
        name = _extract_name(article)
        description = _extract_description(article)
        language = _extract_language(article)
        stars = _extract_stars(article)
        forks = _extract_forks(article)
        stars_today = _extract_stars_today(article)
        url = _extract_url(article)

        return TrendingRepo(
            name=name,
            description=description,
            language=language,
            stars=stars,
            forks=forks,
            stars_today=stars_today,
            url=url,
        )
    except Exception:
        return None


def _extract_name(article) -> str:
    """提取项目名称"""
    h2 = article.select_one("h2.h3.lh-condensed")
    if not h2:
        return ""

    link = h2.select_one("a")
    if not link:
        return ""

    href = link.get("href", "")
    return href.strip("/")


def _extract_description(article) -> str:
    """提取项目描述"""
    p = article.select_one("p.col-9")
    if not p:
        return ""
    return p.get_text(strip=True)


def _extract_language(article) -> str:
    """提取编程语言"""
    span = article.select_one("span[itemprop='programmingLanguage']")
    if not span:
        return ""
    return span.get_text(strip=True)


def _extract_stars(article) -> int:
    """提取总星标数"""
    link = article.select_one("a[href*='stargazers']")
    if not link:
        return 0
    text = link.get_text(strip=True)
    return _parse_number(text)


def _extract_forks(article) -> int:
    """提取 Fork 数"""
    link = article.select_one("a[href*='network']")
    if not link:
        return 0
    text = link.get_text(strip=True)
    return _parse_number(text)


def _extract_stars_today(article) -> int:
    """提取今日新增星标数"""
    span = article.select_one("span.float-sm-right")
    if not span:
        return 0
    text = span.get_text(strip=True)
    match = re.search(r"(\d+(?:,\d+)?)\s*stars", text)
    if match:
        return _parse_number(match.group(1))
    return 0


def _extract_url(article) -> str:
    """提取项目链接"""
    h2 = article.select_one("h2.h3.lh-condensed")
    if not h2:
        return ""

    link = h2.select_one("a")
    if not link:
        return ""

    href = link.get("href", "")
    return f"https://github.com{href}"


def _parse_number(text: str) -> int:
    """解析数字字符串（如 '1,234' -> 1234）"""
    text = text.replace(",", "").strip()
    try:
        return int(text)
    except ValueError:
        return 0
