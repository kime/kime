from flask import Blueprint, jsonify

from app.extensions import auth
from app.models.user import User
from app.responses import not_implemented, bad_request

blueprint = Blueprint('api', __name__, url_prefix='/api')


@blueprint.route('/')
def index():
    return not_implemented()


@blueprint.route('/users/<int:id>')
@auth.login_required
def get_user(id):
    user = User.query.get(id)
    if not user:
        return bad_request()
    return jsonify({'username': user.username})
