from flask import Blueprint, session, url_for, g, jsonify
from flask import redirect, request

from app.extensions import db, auth
from app.models.user import User
from app.responses import bad_request

blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@blueprint.route('/signup', methods=('GET', 'POST'))
def signup():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        return bad_request()
    if User.query.filter_by(username=username).first() is not None:
        return bad_request('Username Exists')

    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify(
        {'username': user.username,
         'url': url_for('api.get_user', id=user.id, _external=True)
         }), 201


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
    g.user = user
    return True


@blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home.index'))


@blueprint.route('/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})


@blueprint.before_app_request
def get_current_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter_by(id=user_id).first()
