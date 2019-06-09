from flask_login import login_required, logout_user, current_user
from quart import Blueprint, jsonify
from quart import request
from werkzeug.http import parse_authorization_header

from app.extensions import auth
from app.models.user import User
from app.responses import bad_request, ok, created

blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@auth.user_loader
def user_loader(user_id):
    return User.query.filter_by(id=user_id).first()


@auth.request_loader
def request_loader(request):
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

# @auth.verify_password
# def verify_password(auth_token, password):
#     """
#
#     :param auth_token:
#     :param password:
#     :return:
#     """
#     # Check if auth_token is valid
#     user = User.verify_auth_token(auth_token)
#
#     if not user:
#         # Authenticate with username and password
#         user = User.query.filter_by(username=auth_token).first()
#         if not user or not user.verify_password(password):
#             return False
#
#     # Set Flask global user
#     session['user_id'] = user.id
#     g.user = user
#     return True


# @blueprint.before_app_request
# def get_current_user():
#     user_id = session.get('user_id')
#     if user_id is None:
#         g.user = None
#     else:
#         g.user = User.query.filter_by(id=user_id).one()


@blueprint.route('/signup', methods=['POST'])
async def signup():
    user_context = await request.get_json()
    username = user_context.get('username')
    password = user_context.get('password')

    if username is None or password is None:
        return bad_request()

    if User.query.filter_by(username=username).first() is not None:
        # TODO: Remove redundant check for duplicate username
        return bad_request('Username Exists')

    user = User.add_user(username, password)
    return jsonify({'username': user.username}), created()


@blueprint.route('/login', methods=['POST', 'GET'])
@login_required
async def login():
    token = current_user.generate_auth_token(7200)
    return jsonify({'username': current_user.username,
                    'token': token.decode('ascii'),
                    'duration': 7200})


@blueprint.route('/logout', methods=['POST'])
@login_required
async def logout():
    logout_user()
    response = {
        'username': current_user.username,
        'message': 'You were logged out.'
    }
    return jsonify(response), ok()
