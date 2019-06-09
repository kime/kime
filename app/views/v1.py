from flask_login import login_required, current_user
from quart import Blueprint, jsonify, request

from app.controllers import image
from app.responses import not_implemented, bad_request

__version__ = 'v1'
blueprint = Blueprint('api', __name__, url_prefix='/api/%s' % __version__)


@blueprint.route('/')
async def index():
    return not_implemented()


@blueprint.route('/user')
@login_required
async def get_user():
    if not current_user:
        return bad_request()

    return jsonify({'id': current_user.id,
                    'username': current_user.username,
                    'created_at': None,
                    'email': None,
                    'plan_balance': None,
                    'file_size_limit': None,
                    'resolution_limit': None,
                    'upload_limit': None,
                    'subscription': None
                    })


@blueprint.route('/images')
@login_required
async def get_images():
    return jsonify(image.list_all(current_user))


@blueprint.route('/images/upload', methods=['POST'])
@login_required
async def upload_image():
    request_files = await request.files
    request_args = await request.args

    if 'image' not in request_files or 'name' not in request_args:
        return bad_request()

    return jsonify(image.upload(request_files['image'].read(), request_args.get('name'), current_user))


@blueprint.route('/images/delete')
@login_required
async def delete_image():
    request_args = await request.args
    if 'id' not in request_args:
        return bad_request()

    return jsonify(request_args.get('id'), image.delete(current_user))


@blueprint.route('/images/enhance', methods=['POST'])
@login_required
async def enhance_image():
    request_context = await request.get_json()
    return jsonify(image.enhance(request_context, current_user))


@blueprint.after_app_request
async def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
        headers = (await request.headers).get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    return response
