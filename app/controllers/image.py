import uuid

import requests

from app import config
from app.models.image import OriginalImage, EnhancedImage
from app.services.storage import azure
from app.util.io import bytes_to_image


def list_all(user_id):
    """

    :param user_id:
    :return:
    """
    raw_images = OriginalImage.query(OriginalImage.id,
                                     OriginalImage.name,
                                     OriginalImage.url.label('original_url'),
                                     EnhancedImage.url.label('enhanced_url')) \
        .filter(OriginalImage.user_id == user_id) \
        .join(EnhancedImage, OriginalImage.id == EnhancedImage.original_id) \
        .all()

    images = list()
    for row in raw_images:
        images.append({
            'id': row.id,
            'name': row.name,
            'uploaded': None,
            'image': {
                'original': {
                    'url': row.original_url,
                    'width': None,
                    'height': None,
                },
                'enhanced': {
                    'url': row.enhanced_url,
                    'width': None,
                    'height': None,
                    'multiplier': None,
                    'fixArtifacts': None
                }
            }
        })


def upload(image_bytes, image_name, user):
    image = bytes_to_image(image_bytes)
    blob_name = str(uuid.uuid4()) + '.png'

    azure.upload_image(image, 'originalimages', blob_name)
    blob_url = azure.get_blob_url('originalimages', blob_name)
    image = OriginalImage.add_image(blob_url, image_name, user)

    return {
        'id': image.id,
        'name': image_name,
        'uploaded': None,
        'image': {
            'original': {
                'url': blob_url,
                'blob_name': blob_name,
                'width': None,
                'height': None,
            }
        }
    }


def enhance(request, user):
    engine_payload = {
        'id': request['id'],
        'multiplier': request['multiplier'],
        'fix_artifacts': request['fix_artifacts'],
        'image': {
            'original': request['image']['original']
        },
    }

    engine_response = requests.post(config.engine_url(), json=engine_payload).json()
    blob_url = azure.get_blob_url('enhancedimages', engine_response['image']['enhanced']['blob_name'])
    original_image = OriginalImage.query.filter_by(id=request['id']).one()
    EnhancedImage.add_image(blob_url, user, original_image)

    return {
        'id': request['id'],
        'name': request['name'],
        'uploaded': None,
        'image': {
            'original': request['image']['original'],
            'enhanced': {
                'url': blob_url,
                'blob_name': engine_response['image']['enhanced']['blob_name'],
                'width': engine_response['image']['enhanced']['width'],
                'height': engine_response['image']['enhanced']['height'],
                'multiplier': request['multiplier'],
                'fix_artifacts': request['fix_artifacts'],
            }
        }
    }


def delete(user):
    # TODO: Implement delete logic
    return None
