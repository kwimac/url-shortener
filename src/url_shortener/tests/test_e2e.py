import pytest
from rest_framework.response import Response
from rest_framework.test import APIClient
from rest_framework import status


@pytest.mark.django_db
def test_url_shortener(
    api_client: APIClient,
) -> None:
    url = "https://google.com"

    response: Response = api_client.post(
        "/shrt/",
        data={
            "url": url,
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    url_hash = response.json()["hash"]
    
    response: Response = api_client.get(
        f"/shrt/{url_hash}",
        follow=False,
    )

    assert response.status_code == status.HTTP_302_FOUND
    assert response.url == url
