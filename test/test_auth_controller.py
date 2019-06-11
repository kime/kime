from flask import json
from six import BytesIO

from test import BaseTestCase


class TestAuthController(BaseTestCase):
    """AuthController integration test stubs"""

    def test_get_user(self):
        """Test case for get_user

        get the current session's user
        """
        response = self.client.open(
            '/v1/auth/user',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_login(self):
        """Test case for login

        logs user into the application
        """
        headers = [('username', 'username_example'),
                   ('password', 'password_example')]
        response = self.client.open(
            '/v1/auth/login',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_logout(self):
        """Test case for logout

        logs out the current user from the session
        """
        response = self.client.open(
            '/v1/auth/logout',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_signup(self):
        """Test case for signup

        create a new user
        """
        user = NewUserRequest()
        response = self.client.open(
            '/v1/auth/user',
            method='POST',
            data=json.dumps(user),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_password(self):
        """Test case for update_password

        update the current user's password
        """
        body = UpdateUserRequest()
        response = self.client.open(
            '/v1/auth/user',
            method='PATCH',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
