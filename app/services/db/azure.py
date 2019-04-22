from app import config
from app.models import user
from app.models import image


def init_app(app, db):
    """

    :param app:
    :param db:
    :return:
    """
    app.config['SQLALCHEMY_DATABASE_URI'] = config.azure_db()
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    with app.app_context():
        db.create_all()
