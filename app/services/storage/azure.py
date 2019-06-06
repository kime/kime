from azure.storage.blob import BlockBlobService

from app import config
from app.util.io import image_to_bytes, bytes_to_image


def download_image(container, blob_name):
    """
    Downloads a blob as an array of bytes, and returns a
    PIL image object initialized using those bytes
    :param container: name of an existing storage container
    :param blob_name: name of the blob containing the image
    :return: a PIL Image object
    """
    account_name, access_key = config.azure_storage()
    blob_service = BlockBlobService(account_name, access_key)
    blob = blob_service.get_blob_to_bytes(container, blob_name)
    return bytes_to_image(blob.content)


def upload_image(image, container, blob_name):
    """
    Converts a PIL Image object into a bytestream and uploads it
    to the given container in Azure Blob Storage
    :param image: a PIL Image object
    :param container: name of an existing storage container
    :param blob_name: name of the blob to save the image as
    :return: ETag and last modified properties for the Block Blob
    """
    account_name, access_key = config.azure_storage()
    blob_service = BlockBlobService(account_name, access_key)
    return blob_service.create_blob_from_bytes(container, blob_name, image_to_bytes(image))


def get_blob_name(blob_url):
    """

    :param blob_url:
    :return:
    """
    return blob_url.split('/')[-1]


def get_blob_url(container, blob_name):
    """

    :param container:
    :param blob_name:
    :return:
    """
    return 'https://kimeimagestore.blob.core.windows.net/%s/%s' % (container, blob_name)
