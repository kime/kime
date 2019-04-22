from flask import Blueprint, session, url_for, g, jsonify
from flask import redirect, request

from app.extensions import auth
from app.models.user import User
from app.responses import bad_request

blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@auth.verify_password
def verify_password(auth_token, password):
    """

    :param auth_token:
    :param password:
    :return:
    """
    # Check if auth_token is valid
    user = User.verify_auth_token(auth_token)

    if not user:
        # Authenticate with username and password
        user = User.query.filter_by(username=auth_token).first()
        if not user or not user.verify_password(password):
            return False

    # Set Flask global user
    session['user_id'] = user.id
    g.user = user
    return True


@blueprint.before_app_request
def get_current_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).one()


@blueprint.route('/signup', methods=['POST'])
def signup():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        return bad_request()
    if User.query.filter_by(username=username).first() is not None:
        # TODO: Remove redundant check for duplicate username
        return bad_request('Username Exists')

    user = User.add_user(username, password)

    return jsonify({'username': user.username}), 201


@blueprint.route('/login', methods=['POST', 'GET'])
@auth.login_required
def login():
    token = g.user.generate_auth_token(600)
    return jsonify({'username': g.user.username,
                    'token': token.decode('ascii'),
                    'duration': 600})


@blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home.index'))
