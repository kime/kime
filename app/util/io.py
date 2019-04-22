import io

from PIL import Image


def load_image(path):
    """
    Load image to memory from the filesystem
    :param path: path to image file
    :return: a PIL Image object
    """
    img = Image.open(path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    return img


def image_to_bytes(image, format='PNG'):
    """
    Converts a PIL Image object into a bytestream
    :param image: a PIL Image object
    :param format: optional format override for file extension
    :return: a Bytes array of the image
    """
    image_bytes = io.BytesIO()
    image.save(image_bytes, format=format)
    return image_bytes.getvalue()


def bytes_to_image(image_bytes):
    """
    Converts a bytestream into a PIL Image object
    :param image_bytes: a Bytes array of the image
    :return: a PIL Image object
    """
    img = Image.open(io.BytesIO(image_bytes))
    return img.convert('RGB') if img.mode != 'RGB' else img
