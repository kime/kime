from flask_login import login_required, logout_user, current_user
from quart import Blueprint, jsonify
from quart import request
from werkzeug.http import parse_authorization_header

from app.extensions import auth
from app.models.user import User
from app.responses import bad_request, ok, created, no_content

blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@auth.user_loader
def user_loader(user_id):
    """

    :param user_id:
    :return:
    """
    return User.query.filter_by(id=user_id).first()


@auth.request_loader
def request_loader(request):
    """

    :param request:
    :return:
    """
    authorization = parse_authorization_header(request.headers.get('Authorization'))

    # Check if auth_token is valid
    user = User.verify_auth_token(authorization.username)
    if user:
        user.is_authenticated = True
        return user

    # Authenticate with username and password
    user = User.query.filter_by(username=authorization.username).first()
    if user and user.verify_password(authorization.password):
        user.is_authenticated = True
        return user

    return None


@blueprint.route('/user', methods=['GET'])
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


@blueprint.route('/user', methods=['PATCH'])
async def change_password():
    user_context = await request.get_json()
    old_password = user_context.get('oldPassword')
    new_password = user_context.get('newPassword')

    if old_password is None or new_password is None:
        return bad_request()

    current_user.change_password(old_password, new_password)
    return no_content()


@blueprint.route('/user', methods=['POST'])
async def signup():
    user_context = await request.get_json()
    username = user_context.get('username')
    password = user_context.get('password')

    if username is None or password is None:
        return bad_request()

    if User.query.filter_by(username=username).first() is not None:
        return bad_request('Username Exists')

    user = User.add_user(username, password)
    return jsonify({'username': user.username}), created()


@blueprint.route('/login', methods=['GET', 'POST'])
@login_required
async def login():
    token = current_user.generate_auth_token(7200)
    return jsonify({'username': current_user.username,
                    'token': token.decode('ascii'),
                    'duration': 7200})


@blueprint.route('/logout', methods=['GET', 'POST'])
@login_required
async def logout():
    logout_user()
    response = {
        'username': current_user.username,
        'message': 'You were logged out.'
    }
    return jsonify(response), ok()
