import requests

BASE_URL = "https://github.com/trending"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}


def fetch_trending_page(
    language: str | None = None,
    time_range: str = "daily",
) -> str:
    """
    获取 GitHub Trending 页面 HTML

    Args:
        language: 编程语言过滤（如 python, javascript）
        time_range: 时间范围（daily, weekly, monthly）

    Returns:
        页面 HTML 内容

    Raises:
        requests.RequestException: 网络请求失败
    """
    url = BASE_URL

    if language:
        url = f"{BASE_URL}/{language}"

    params = {}
    if time_range != "daily":
        params["since"] = time_range

    response = requests.get(url, headers=HEADERS, params=params, timeout=30)
    response.raise_for_status()

    return response.text
