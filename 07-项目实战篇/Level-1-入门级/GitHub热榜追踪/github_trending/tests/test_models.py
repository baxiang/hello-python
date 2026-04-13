import pytest
from app.models import TrendingRepo


def test_trending_repo_creation():
    repo = TrendingRepo(
        name="microsoft/vscode",
        description="Visual Studio Code",
        language="TypeScript",
        stars=150000,
        forks=22000,
        stars_today=50,
        url="https://github.com/microsoft/vscode",
    )
    assert repo.name == "microsoft/vscode"
    assert repo.stars == 150000


def test_trending_repo_defaults():
    repo = TrendingRepo(
        name="test/repo",
        description="",
        language="",
        stars=0,
        forks=0,
        stars_today=0,
        url="https://github.com/test/repo",
    )
    assert repo.name == "test/repo"


def test_trending_repo_to_dict():
    repo = TrendingRepo(
        name="python/cpython",
        description="Python interpreter",
        language="Python",
        stars=60000,
        forks=15000,
        stars_today=100,
        url="https://github.com/python/cpython",
    )
    result = repo.to_dict()
    assert result["name"] == "python/cpython"
    assert result["stars"] == 60000
