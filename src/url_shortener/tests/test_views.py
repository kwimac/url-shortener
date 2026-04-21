from unittest.mock import patch
import uuid

import pytest
from rest_framework.response import Response
from rest_framework.test import APIClient
from rest_framework import status

from src.url_shortener.models import ShortURL
from src.url_shortener.tests.factories import ShortURLFactory


VALID_URL = "https://google.com"


@pytest.mark.parametrize(
    ("url"),
    [
        pytest.param(VALID_URL, id="valid http URL"),
        pytest.param("ftp://file.txt", id="other protocol"),
    ],
)
@pytest.mark.django_db
def test_URLShortenerView__success(
    api_client: APIClient,
    url: str,
) -> None:

    response: Response = api_client.post(
        "/shrt/",
        data={
            "url": url,
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert "hash" in response.json()


@pytest.mark.django_db
def test_URLShortenerView__success_without_hash_collision(
    api_client: APIClient,
) -> None:
    hash_ = "abcde12345"
    other_hash = "abcde67890"
    ShortURLFactory(hash=hash_)

    with patch("src.url_shortener.models.ShortURL.generate_hash", side_effect=[
        (uuid.uuid4(), hash_),
        (uuid.uuid4(), other_hash)
    ]):
        response: Response = api_client.post(
            "/shrt/",
            data={
                "url": VALID_URL,
            },
        )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["hash"] == other_hash


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        pytest.param(
            "google.com",
            {"url": ["Enter a valid URL."]},
            id="no protocol",
        ),
        pytest.param(
            "not_a_link",
            {"url": ["Enter a valid URL."]},
            id="invalid url",
        ),
    ],
)
@pytest.mark.django_db
def test_URLShortenerView__failure_invalid_url(
    api_client: APIClient,
    url: str,
    expected: dict,
) -> None:

    response: Response = api_client.post(
        "/shrt/",
        data={
            "url": url,
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert expected == response.json()


@pytest.mark.django_db
def test_URLShortenerView__failure_url_already_in_db(
    api_client: APIClient,
) -> None:
    url = "https://google.com"
    ShortURLFactory(original_url=url)
    expected = {
        "url": ["URL arleady in DB"],
    }

    response: Response = api_client.post(
        "/shrt/",
        data={
            "url": url,
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert expected == response.json()

@pytest.mark.django_db
def test_ShortURLView__success(
    api_client: APIClient,
) -> None:
    short_url_orm: ShortURL = ShortURLFactory()
    
    response: Response = api_client.get(
        f"/shrt/{short_url_orm.hash}",
        follow=False,
    )

    assert response.status_code == status.HTTP_302_FOUND

@pytest.mark.django_db
def test_ShortURLView__failure(
    api_client: APIClient,
) -> None:    
    response: Response = api_client.get(
        f"/shrt/a",
        follow=False,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.django_db
def test_ShortURLView__failure_invalid_url(
    api_client: APIClient,
) -> None:
    short_url_orm: ShortURL = ShortURLFactory()
    
    response: Response = api_client.get(
        f"/shrt/{short_url_orm.hash}/",
        follow=False,
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND