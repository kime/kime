from flask import json
from six import BytesIO

from app.models.image import EnhancedImage
from test import BaseTestCase


class TestImagesController(BaseTestCase):
    """ImagesController integration test stubs"""

    def test_delete_image(self):
        """Test case for delete_image

        Deletes the image with the given id
        """
        response = self.client.open(
            '/v1/images/{imageId}'.format(imageId=789),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_enhance_image(self):
        """Test case for enhance_image

        Enhance an image from the gallery
        """
        imageId = EnhancedImage()
        response = self.client.open(
            '/v1/images/enhance',
            method='POST',
            data=json.dumps(imageId),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_image(self):
        """Test case for get_image

        Gets the image with the given id
        """
        response = self.client.open(
            '/v1/images/{imageId}'.format(imageId=789),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_images(self):
        """Test case for get_images

        Get all images in the gallery
        """
        response = self.client.open(
            '/v1/images',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_upload_image(self):
        """Test case for upload_image

        Add a new image to the gallery
        """
        headers = [('name', 'file.png')]
        data = dict(image=(BytesIO(b'some random data'), 'file.png'))
        response = self.client.open(
            '/v1/images/upload',
            method='POST',
            headers=headers,
            data=data,
            content_type='multipart/form-data')
        self.assert500(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        image_file = open('data/images/fuji.jpg', 'rb')
        data = {'image': image_file}
        response = self.client.open(
            '/v1/images/upload',
            method='POST',
            headers=headers,
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
