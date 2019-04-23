import pytest

from app.__main__ import app as kime


@pytest.fixture
def client():
    kime.config['TESTING'] = True
    client = kime.test_client()

    return client
