from base64 import b64encode

from app import config
from test.test_app import client


def login(client, username, password):
    auth_headers = {
        'Authorization': 'Basic %s' % b64encode(bytes('%s:%s' % (username, password), 'utf-8')).decode("ascii")
    }
    return client.post('/auth/login', headers=auth_headers)


def logout(client, username, password):
    auth_headers = {
        'Authorization': 'Basic %s' % b64encode(bytes('%s:%s' % (username, password), 'utf-8')).decode("ascii")
    }
    return client.post('/auth/logout', headers=auth_headers)


def test_auth(client):
    """Make sure login and logout works."""
    test_username, test_password = config.test_credentials()

    response = login(client, test_username, test_password)
    assert response.status_code == 200

    response = logout(client, test_username, test_password)
    assert response.status_code == 200

    response = login(client, test_username + 'x', test_password)
    assert response.status_code == 401

    response = login(client, test_username, test_password + 'x')
    assert response.status_code == 401
