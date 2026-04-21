from urllib.parse import urlparse

import validators


def standardize_url(url: str) -> str | None:
    parts = urlparse(url)
    if not parts.scheme:
        url = f"https://{url}"
    parts = urlparse(url)
    if not validators.url(url):
        return None
    return url
