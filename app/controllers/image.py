import uuid

import requests
from requests.auth import HTTPBasicAuth

from app import config
from app.models.image import OriginalImage, EnhancedImage
from app.services.storage import azure
from app.util.io import bytes_to_image
from app.extensions import db


def list_all(user_id):
    """

    :param user_id:
    :return:
    """
    image_join_result = db.session.query(OriginalImage.id,
                                         OriginalImage.name,
                                         OriginalImage.url.label('original_url'),
                                         EnhancedImage.url.label('enhanced_url')) \
        .filter(OriginalImage.user_id == user_id) \
        .join(EnhancedImage, OriginalImage.id == EnhancedImage.original_id) \
        .all()

    image_contexts = list()
    for row in image_join_result:
        image_contexts.append({
            'id': row.id,
            'name': row.name,
            'uploaded': None,
            'originalImage': {
                'width': None,
                'height': None,
                'url': row.original_url
            },
            'enhancedImage': {
                'width': None,
                'height': None,
                'multiplier': None,
                'fixArtifacts': None,
                'url': row.enhanced_url
            }
        })

    return image_contexts


def upload(image_bytes, image_name, user):
    """

    :param image_bytes:
    :param image_name:
    :param user:
    :return:
    """
    image = bytes_to_image(image_bytes)
    blob_name = str(uuid.uuid4()) + '.png'

    azure.upload_image(image, 'originalimages', blob_name)
    blob_url = azure.get_blob_url('originalimages', blob_name)
    image_row = OriginalImage.add_image(blob_url, image_name, user)

    return {
        'id': image_row.id,
        'name': image_name,
        'uploaded': None,
        'originalImage': {
            'width': image.size[0],
            'height': image.size[1],
            'url': blob_url
        }
    }


def enhance(request, user):
    """

    :param request:
    :param user:
    :return:
    """
    engine_payload = {
        'id': request['id'],
        'multiplier': request['multiplier'],
        'fixArtifacts': request['fixArtifacts'],
        'originalImage': {
            'blobName': azure.get_blob_name(request['originalImage']['url'])
        }
    }

    engine_response = requests.post(config.engine_url(),
                                    json=engine_payload,
                                    auth=HTTPBasicAuth(*config.engine_credentials())).json()

    blob_url = azure.get_blob_url('enhancedimages', engine_response['enhancedImage']['blobName'])
    original_image = OriginalImage.query.filter_by(id=request['id']).one()
    EnhancedImage.add_image(blob_url, user, original_image)

    return {
        'id': request['id'],
        'name': request['name'],
        'uploaded': None,
        'originalImage': request['originalImage'],
        'enhancedImage': {
            'url': blob_url,
            'multiplier': request['multiplier'],
            'fixArtifacts': request['fixArtifacts'],
            'width': engine_response['enhancedImage']['width'],
            'height': engine_response['enhancedImage']['height']
        }
    }


def delete(user):
    # TODO: Implement delete logic
    return None
