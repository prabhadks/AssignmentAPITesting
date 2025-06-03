import pytest
import urllib.parse

import config

@pytest.fixture
def get_currencies_endpoint():
    return urllib.parse.urljoin(config.BASE_URL, config.GET_CURRENCIES)

@pytest.fixture
def get_latest_endpoint():
    return urllib.parse.urljoin(config.BASE_URL, config.GET_LATEST)

@pytest.fixture
def get_convert_endpoint():
    return urllib.parse.urljoin(config.BASE_URL, config.GET_CONVERT)