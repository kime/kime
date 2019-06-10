import uuid

import aiohttp
from aiohttp import BasicAuth

from app import config
from app.models.image import OriginalImage, EnhancedImage
from app.services.storage import azure
from app.util.io import bytes_to_image
from app.extensions import db
from app.responses import forbidden, ok, not_found


def get(image_id, user):
    """

    :param image_id:
    :param user:
    :return:
    """
    original_image = OriginalImage.query.filter_by(id=image_id).one()

    if not original_image:
        # Check if the image exists
        return not_found()
    elif original_image.user_id != user.id:
        # Check if the user has access to the image
        return forbidden()

    enhanced_image = EnhancedImage.query.filter_by(original_id=image_id).one()

    if enhanced_image:
        enhanced_image_context = {
            'width': None,
            'height': None,
            'multiplier': None,
            'fixArtifacts': None,
            'url': enhanced_image.url
        }
    else:
        enhanced_image_context = None

    return {
        'id': original_image.id,
        'name': original_image.name,
        'uploaded': None,
        'originalImage': {
            'width': None,
            'height': None,
            'url': original_image.url
        },
        'enhancedImage': enhanced_image_context
    }


def get_all(user):
    """

    :param user_id:
    :return:
    """
    image_join_result = db.session.query(OriginalImage.id,
                                         OriginalImage.name,
                                         OriginalImage.url.label('original_url'),
                                         EnhancedImage.url.label('enhanced_url')) \
        .filter(OriginalImage.user_id == user.id) \
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


def delete(image_id, user):
    """

    :param image_id:
    :param user:
    :return:
    """
    original_image = OriginalImage.query.filter_by(id=image_id).one()

    if not original_image:
        # Check if the image exists
        return not_found()
    elif original_image.user_id != user.id:
        # Check if the user has access to the image
        return forbidden()

    # Remove entry in EnhancedImage if it exists
    enhanced_image = EnhancedImage.query.filter_by(original_id=image_id).one()
    if enhanced_image:
        EnhancedImage.remove_image(enhanced_image.id)

    # Remove entry in OriginalImage
    OriginalImage.remove_image(original_image.id)
    return ok()


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


async def enhance(request, user):
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

    async with aiohttp.ClientSession() as session:
        async with session.post(config.engine_url(),
                                auth=BasicAuth(*config.engine_credentials()),
                                json=engine_payload) as engine_request:
            engine_response = await engine_request.json()

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
