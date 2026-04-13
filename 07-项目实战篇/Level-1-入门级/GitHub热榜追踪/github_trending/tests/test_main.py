import pytest
from unittest.mock import patch, Mock
from pathlib import Path
from tempfile import TemporaryDirectory
from app.main import main, parse_args


def test_parse_args_defaults():
    args = parse_args([])
    assert args.language is None
    assert args.range == "daily"
    assert args.output == "terminal"
    assert args.limit == 25


def test_parse_args_with_options():
    args = parse_args(["--language", "python", "--range", "weekly", "--output", "json"])
    assert args.language == "python"
    assert args.range == "weekly"
    assert args.output == "json"


def test_parse_args_limit():
    args = parse_args(["--limit", "10"])
    assert args.limit == 10


def test_main_terminal_output():
    with patch("app.main.fetch_trending_page") as mock_fetch:
        with patch("app.main.parse_trending_page") as mock_parse:
            mock_fetch.return_value = "<html></html>"
            mock_parse.return_value = []

            result = main(["--output", "terminal"])
            assert "暂无热门项目数据" in result


def test_main_json_output():
    with TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "output.json"

        with patch("app.main.fetch_trending_page") as mock_fetch:
            with patch("app.main.parse_trending_page") as mock_parse:
                from app.models import TrendingRepo

                mock_fetch.return_value = "<html></html>"
                mock_parse.return_value = [
                    TrendingRepo(
                        name="test/repo",
                        description="Test",
                        language="Python",
                        stars=1000,
                        forks=100,
                        stars_today=50,
                        url="https://github.com/test/repo",
                    )
                ]

                result = main(["--output", "json", "--file", str(filepath)])
                assert filepath.exists()
