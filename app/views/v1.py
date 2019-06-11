from flask_login import login_required, current_user
from quart import Blueprint, jsonify, request

from app.controllers import image
from app.responses import bad_request

__version__ = 'v1'
blueprint = Blueprint('api', __name__, url_prefix='/api/%s' % __version__)


@blueprint.route('/images/<id>', methods=['GET'])
@login_required
async def get_image(id):
    return jsonify(image.get(id, current_user))


@blueprint.route('/images', methods=['GET'])
@login_required
async def get_images():
    return jsonify(image.get_all(current_user))


@blueprint.route('/images/<id>', methods=['DELETE'])
@login_required
async def delete_image(id):
    return jsonify(image.delete(id, current_user))


@blueprint.route('/images/upload', methods=['POST'])
@login_required
async def upload_image():
    request_files = await request.files

    if 'image' not in request_files or 'name' not in request.args:
        return bad_request()

    return jsonify(image.upload(request_files['image'].read(), request.args.get('name'), current_user))


@blueprint.route('/images/enhance', methods=['POST'])
@login_required
async def enhance_image():
    request_context = await request.get_json()
    return jsonify(await image.enhance(request_context, current_user))


@blueprint.after_app_request
async def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'

    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
        headers = (await request.headers).get('Access-Control-Request-Headers')

        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers

    return response
