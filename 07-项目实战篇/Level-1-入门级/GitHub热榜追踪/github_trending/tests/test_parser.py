import pytest
from pathlib import Path
from app.parser import parse_trending_page
from app.models import TrendingRepo


@pytest.fixture
def sample_html():
    return Path("tests/fixtures/sample.html").read_text()


def test_parse_trending_page_returns_list(sample_html):
    result = parse_trending_page(sample_html)
    assert isinstance(result, list)


def test_parse_trending_page_extract_repos(sample_html):
    result = parse_trending_page(sample_html)
    assert len(result) == 2


def test_parse_trending_page_repo_data(sample_html):
    result = parse_trending_page(sample_html)
    repo = result[0]

    assert isinstance(repo, TrendingRepo)
    assert repo.name == "microsoft/vscode"
    assert "Visual Studio Code" in repo.description
    assert repo.language == "TypeScript"


def test_parse_trending_page_stars(sample_html):
    result = parse_trending_page(sample_html)
    repo = result[0]

    assert repo.stars == 150000
    assert repo.stars_today == 1234


def test_parse_trending_page_url(sample_html):
    result = parse_trending_page(sample_html)
    repo = result[0]

    assert repo.url == "https://github.com/microsoft/vscode"


def test_parse_empty_page():
    result = parse_trending_page("<html><body></body></html>")
    assert result == []


def test_parse_limit(sample_html):
    result = parse_trending_page(sample_html, limit=1)
    assert len(result) == 1
