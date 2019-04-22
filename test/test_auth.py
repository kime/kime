from app import config


def login(client, username, password):
    return client.post('/auth/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/auth/logout', follow_redirects=True)


def test_auth(client):
    """Make sure login and logout works."""
    test_username, test_password = config.test_credentials()

    rv = login(client, test_username, test_password)
    assert b'You were logged in' in rv.data

    rv = logout(client)
    assert b'You were logged out' in rv.data

    rv = login(client, test_username + 'x', test_password)
    assert b'Invalid username' in rv.data

    rv = login(client, test_username, test_password + 'x')
    assert b'Invalid password' in rv.data
