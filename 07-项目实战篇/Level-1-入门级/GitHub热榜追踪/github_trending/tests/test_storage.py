import pytest
import json
import csv
from pathlib import Path
from tempfile import TemporaryDirectory
from app.models import TrendingRepo
from app.storage import save_json, save_csv, format_terminal


@pytest.fixture
def sample_repos():
    return [
        TrendingRepo(
            name="microsoft/vscode",
            description="Visual Studio Code",
            language="TypeScript",
            stars=150000,
            forks=22000,
            stars_today=1234,
            url="https://github.com/microsoft/vscode",
        ),
        TrendingRepo(
            name="python/cpython",
            description="Python interpreter",
            language="Python",
            stars=60000,
            forks=15000,
            stars_today=500,
            url="https://github.com/python/cpython",
        ),
    ]


def test_save_json(sample_repos):
    with TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "trending.json"
        save_json(sample_repos, filepath)

        assert filepath.exists()

        with open(filepath) as f:
            data = json.load(f)

        assert len(data) == 2
        assert data[0]["name"] == "microsoft/vscode"


def test_save_csv(sample_repos):
    with TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "trending.csv"
        save_csv(sample_repos, filepath)

        assert filepath.exists()

        with open(filepath, newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        assert len(rows) == 2
        assert rows[0]["name"] == "microsoft/vscode"
        assert rows[0]["stars"] == "150000"


def test_format_terminal(sample_repos):
    output = format_terminal(sample_repos)

    assert "microsoft/vscode" in output
    assert "python/cpython" in output
    assert "150,000" in output


def test_format_terminal_empty():
    output = format_terminal([])
    assert output == "暂无热门项目数据"


def test_save_json_empty():
    with TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "empty.json"
        save_json([], filepath)

        with open(filepath) as f:
            data = json.load(f)

        assert data == []
