import pytest
from unittest.mock import patch, Mock
from app.fetcher import fetch_trending_page


def test_fetch_trending_page_success():
    with patch("app.fetcher.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<html><body>test</body></html>"
        mock_get.return_value = mock_response

        result = fetch_trending_page()
        assert result == "<html><body>test</body></html>"
        mock_get.assert_called_once()


def test_fetch_trending_page_with_language():
    with patch("app.fetcher.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<html>python</html>"
        mock_get.return_value = mock_response

        result = fetch_trending_page(language="python")
        assert result == "<html>python</html>"

        call_args = mock_get.call_args
        assert "python" in call_args[0][0]


def test_fetch_trending_page_with_range():
    with patch("app.fetcher.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<html>weekly</html>"
        mock_get.return_value = mock_response

        result = fetch_trending_page(time_range="weekly")
        assert result == "<html>weekly</html>"

        call_kwargs = mock_get.call_args[1]
        assert "params" in call_kwargs
        assert call_kwargs["params"]["since"] == "weekly"


def test_fetch_trending_page_failure():
    with patch("app.fetcher.requests.get") as mock_get:
        import requests

        mock_get.side_effect = requests.RequestException("Network error")

        with pytest.raises(requests.RequestException):
            fetch_trending_page()


def test_fetch_trending_page_headers():
    with patch("app.fetcher.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<html></html>"
        mock_get.return_value = mock_response

        fetch_trending_page()

        call_kwargs = mock_get.call_args[1]
        assert "headers" in call_kwargs
        assert "User-Agent" in call_kwargs["headers"]
