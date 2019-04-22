import pytest

from app import kime

from test import test_image


@pytest.fixture
def client():
    kime.app.config['TESTING'] = True
    client = kime.app.test_client()

    with kime.app.app_context():
        kime.init_db()

    return client


if __name__ == '__main__':
    test_image.test_upload(client)
