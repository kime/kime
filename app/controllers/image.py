from app.models.image import OriginalImage, EnhancedImage
from app.models.user import User
from app.services.storage import azure
from app.util.io import bytes_to_image
import uuid


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


def upload(image_bytes, image_name, user_id):
    image = bytes_to_image(image_bytes)
    user = User.query.get(user_id)
    blob_name = str(uuid.uuid4()) + '.png'

    azure.upload_image(image, 'originalimages', blob_name)
    blob_url = azure.get_blob_url('originalimages', blob_name)
    image = OriginalImage.add_image(blob_url, image_name, user)

    return {
        'id': image.id,
        'name': image.name,
        'uploaded': None,
        'image': {
            'original': {
                'url': image.url,
                'width': None,
                'height': None,
            }
        }
    }


def enhance():
    return None


def delete():
    # TODO: Implement delete logic
    return None
