import pytest

from src.url_shortener.utils import standardize_url


@pytest.mark.parametrize(
    ("url, expected"),
    [
        pytest.param("google.com", "https://google.com", id="no protocol"),
        pytest.param("http://google.com", "http://google.com", id="with protocol"),
        pytest.param("pl.example.com", "https://pl.example.com", id="with subdomain"),
        pytest.param("ftp://file.txt", "ftp://file.txt", id="not http"),
        pytest.param("not_a_link", None, id="invalid url"),
    ]
)
def test_standardize_url(url: str, expected: str | None) -> None:
    actual = standardize_url(url)
    assert actual == expected
