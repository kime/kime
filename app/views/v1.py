from flask import Blueprint, jsonify, request, session, g

from app.extensions import auth
from app.models.user import User
from app.controllers import image
from app.responses import not_implemented, bad_request

__version__ = 'v1'
blueprint = Blueprint('api', __name__, url_prefix='/api/%s' % __version__)


@blueprint.route('/')
def index():
    return not_implemented()


@blueprint.route('/user')
@auth.login_required
def get_user():
    user = g.user
    if not user:
        return bad_request()
    return jsonify({'id': user.id,
                    'username': user.username,
                    'created_at': None,
                    'email': None,
                    'plan_balance': None,
                    'file_size_limit': None,
                    'resolution_limit': None,
                    'upload_limit': None,
                    'subscription': None
                    })


@blueprint.route('/images')
@auth.login_required
def get_images():
    user_id = session.get('user_id')
    return jsonify(image.list_all(user_id))


@blueprint.route('/images/upload', methods=['POST'])
@auth.login_required
def upload_image():
    if 'image' not in request.files or 'name' not in request.args:
        return bad_request()
    return jsonify(image.upload(request.files['image'].read(), request.args.get('name'), g.user))


@blueprint.route('/images/enhance', methods=['POST'])
@auth.login_required
def enhance_image():
    return jsonify(image.enhance(request.json, g.user))


@blueprint.route('/images/delete')
@auth.login_required
def delete_image():
    return jsonify(image.delete(g.user))


@blueprint.after_app_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    return response
