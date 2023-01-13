import re
import pytest
import requests
from src.modules.funny_img import get_image_url


@pytest.fixture
def target_url():
    return 'https://api.thecatapi.com/v1/images/search'


@pytest.fixture
def image_field():
    return 'url'


@pytest.fixture
def url_regex():
    regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}'
        r'[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE
    )
    return regex


def test_returns_str(target_url, image_field):
    image_url = get_image_url(target_url=target_url,
                              image_field=image_field)
    assert isinstance(image_url, str)


def test_str_is_url(target_url, image_field, url_regex):
    image_url = get_image_url(target_url=target_url,
                              image_field=image_field)
    assert re.match(url_regex, image_url) is not None


def test_url_is_reachable(target_url, image_field):
    image_url = get_image_url(target_url=target_url,
                              image_field=image_field)
    second_response = requests.get(image_url)
    assert second_response.status_code == 200
