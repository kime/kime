import requests
from requests.auth import HTTPBasicAuth

from app import config


def test_upload(client):
    test_username, test_password = config.test_credentials()
    response = requests.get('http://0.0.0.0:3780/auth/login', auth=HTTPBasicAuth(test_username, test_password))
    auth_headers = {'Content-Type': 'application/json',
                    'Authorization': response.json()['token']}

    image_file = open('data/images/fuji.jpg', 'rb')
    files = {'image': image_file}
    requests.post('http://0.0.0.0:3780/api/v1/images/upload',
                  params={'name': 'fuji'}, files=files,
                  auth=(response.json()['token'], ''))
    image_file.close()
