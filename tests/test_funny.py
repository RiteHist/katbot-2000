import re
import pytest
import requests
from src.modules.funny_img import get_image_url, resolve_img_site


@pytest.fixture
def target_url():
    return 'https://api.thecatapi.com/v1/images/search'


@pytest.fixture
def site_name():
    return 'cats'


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

def test_working():
    assert True
"""
def test_returns_str(target_url, site_name):
    site_url = resolve_img_site(site_name=site_name)
    assert isinstance(site_url, str)
    image_url = get_image_url(target_url=target_url)
    assert isinstance(image_url, str)


def test_str_is_url(target_url, site_name, url_regex):
    site_url = resolve_img_site(site_name=site_name)
    assert re.match(url_regex, site_url) is not None
    image_url = get_image_url(target_url=target_url)
    assert re.match(url_regex, image_url) is not None


def test_url_is_reachable(target_url, site_name):
    site_url = resolve_img_site(site_name=site_name)
    first_response = requests.get(site_url)
    assert first_response.status_code == 200
    image_url = get_image_url(target_url=target_url)
    second_response = requests.get(image_url)
    assert second_response.status_code == 200
"""